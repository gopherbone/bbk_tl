//! bbkemu: input routes. A route is a JSON-lines file of key events stamped
//! with the frame they apply before:
//!
//!   {"route":1,"gam":"<fnv64 of the .gam>","model":"A4988"}
//!   {"f":1012,"k":"ENTER"}      key_down(ENTER) before frame 1012 runs
//!   {"f":1016,"up":1}           key_up()
//!   {"f":5000,"mark":"chapter 2"}  a note; no effect on emulation
//!   {"f":9000,"end":1}          where a play session stopped
//!
//! The player (bbkplay) and the CLI (input.replay) both apply events with
//! `apply`, at frame boundaries, so a route replays identically in either.

use crate::input::BbkKey;
use crate::Emulator;

#[derive(Clone, Debug, PartialEq, Eq)]
pub enum Action {
    Down(BbkKey),
    Up,
    Mark(String),
    End,
    /// write bytes at a CPU address (cheats); applied like inputs, at a frame start
    Poke(u16, Vec<u8>),
}

#[derive(Clone, Debug, PartialEq, Eq)]
pub struct Event {
    pub frame: u64,
    pub action: Action,
}

/// FNV-1a 64 of the .gam, used to check a route belongs to a game.
pub fn gam_hash(data: &[u8]) -> String {
    let mut h: u64 = 0xcbf2_9ce4_8422_2325;
    for &b in data {
        h = (h ^ b as u64).wrapping_mul(0x0000_0100_0000_01b3);
    }
    format!("{h:016x}")
}

pub fn header(gam: &[u8], model: &str) -> String {
    format!("{{\"route\":1,\"gam\":\"{}\",\"model\":\"{}\"}}", gam_hash(gam), model)
}

pub fn key_by_name(name: &str) -> Option<BbkKey> {
    (0..0x40u8).filter_map(BbkKey::from_code).find(|k| k.name() == name)
}

fn field<'a>(line: &'a str, name: &str) -> Option<&'a str> {
    let pat = format!("\"{name}\":");
    let i = line.find(&pat)? + pat.len();
    let rest = line[i..].trim_start();
    if let Some(s) = rest.strip_prefix('"') {
        let mut end = 0;
        let b = s.as_bytes();
        while end < b.len() && b[end] != b'"' {
            end += if b[end] == b'\\' { 2 } else { 1 };
        }
        Some(&s[..end.min(s.len())])
    } else {
        let end = rest.find([',', '}']).unwrap_or(rest.len());
        Some(rest[..end].trim())
    }
}

/// Header fields (gam hash, model) if `line` is a route header.
pub fn parse_header(line: &str) -> Option<(String, String)> {
    field(line, "route")?;
    Some((field(line, "gam")?.to_string(), field(line, "model").unwrap_or("").to_string()))
}

pub fn parse_line(line: &str) -> Result<Option<Event>, String> {
    let line = line.trim();
    if line.is_empty() || line.starts_with('#') || field(line, "route").is_some() {
        return Ok(None);
    }
    let frame: u64 = field(line, "f")
        .ok_or_else(|| format!("route line without \"f\": {line}"))?
        .parse()
        .map_err(|_| format!("bad frame in {line}"))?;
    let action = if let Some(k) = field(line, "k") {
        Action::Down(key_by_name(k).ok_or_else(|| format!("unknown key {k:?}"))?)
    } else if field(line, "up").is_some() {
        Action::Up
    } else if let Some(m) = field(line, "mark") {
        Action::Mark(m.replace("\\\"", "\"").replace("\\\\", "\\"))
    } else if field(line, "end").is_some() {
        Action::End
    } else if let Some(a) = field(line, "poke") {
        let addr = u16::from_str_radix(a, 16).map_err(|_| format!("bad poke address in {line}"))?;
        let hex = field(line, "data").ok_or_else(|| format!("poke without data: {line}"))?;
        if hex.len() % 2 != 0 {
            return Err(format!("odd poke data in {line}"));
        }
        let data = (0..hex.len() / 2)
            .map(|i| u8::from_str_radix(&hex[2 * i..2 * i + 2], 16))
            .collect::<Result<Vec<u8>, _>>()
            .map_err(|_| format!("bad poke data in {line}"))?;
        Action::Poke(addr, data)
    } else {
        return Err(format!("unknown route event: {line}"));
    };
    Ok(Some(Event { frame, action }))
}

pub fn to_line(e: &Event) -> String {
    match &e.action {
        Action::Down(k) => format!("{{\"f\":{},\"k\":\"{}\"}}", e.frame, k.name()),
        Action::Up => format!("{{\"f\":{},\"up\":1}}", e.frame),
        Action::Mark(m) => format!(
            "{{\"f\":{},\"mark\":\"{}\"}}",
            e.frame,
            m.replace('\\', "\\\\").replace('"', "\\\"")
        ),
        Action::End => format!("{{\"f\":{},\"end\":1}}", e.frame),
        Action::Poke(a, d) => format!(
            "{{\"f\":{},\"poke\":\"{:04x}\",\"data\":\"{}\"}}",
            e.frame,
            a,
            d.iter().map(|b| format!("{b:02x}")).collect::<String>()
        ),
    }
}

/// Apply one event. Call it before the event's frame runs.
pub fn apply(emu: &mut Emulator, e: &Event) {
    match &e.action {
        Action::Down(k) => emu.key_down(*k),
        Action::Up => emu.key_up(),
        Action::Mark(_) | Action::End => {}
        Action::Poke(a, d) => {
            for (i, b) in d.iter().enumerate() {
                emu.cpu.memory_mut().write(a.wrapping_add(i as u16), *b);
            }
        }
    }
}

#[cfg(test)]
mod tests {
    use super::*;

    #[test]
    fn round_trips_lines() {
        for e in [
            Event { frame: 12, action: Action::Down(BbkKey::Enter) },
            Event { frame: 13, action: Action::Up },
            Event { frame: 14, action: Action::Mark("boss \"A\"".into()) },
            Event { frame: 15, action: Action::End },
            Event { frame: 16, action: Action::Poke(0x1826, vec![1, 0, 0xff]) },
        ] {
            assert_eq!(parse_line(&to_line(&e)).unwrap(), Some(e));
        }
        assert_eq!(parse_line(&header(b"x", "A4988")).unwrap(), None);
        assert!(parse_header(&header(b"x", "A4988")).is_some());
    }
}

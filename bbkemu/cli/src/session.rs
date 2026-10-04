//! Emulator session: run control, breakpoints, watchpoints, snapshots,
//! input scheduling, screen capture, memory tools, trace and coverage.

use std::collections::{BTreeMap, HashMap, VecDeque};

use bbkemu_core::input::BbkKey;
use bbkemu_core::memory::BusAccess;
use bbkemu_core::route;
use bbkemu_core::{model, Emulator};
use serde_json::{json, Value};

use crate::archive::Archive;
use crate::disasm;
use crate::png;

pub const VERSION: &str = env!("CARGO_PKG_VERSION");
const FLASH_BASE: u32 = 0x200000;
const GAM_FLASH: u32 = 0x20D000; // physical address of .gam offset 0
const LCD_W: usize = 159;
const LCD_H: usize = 96;

type R<T> = Result<T, String>;

// ---------------------------------------------------------------- params --

fn num(v: &Value) -> R<u64> {
    match v {
        Value::Number(n) => n.as_u64().ok_or_else(|| format!("bad number {n}")),
        Value::String(s) => {
            let t = s.trim();
            let (digits, radix) = if let Some(h) = t.strip_prefix('$') {
                (h, 16)
            } else if let Some(h) = t.strip_prefix("0x").or_else(|| t.strip_prefix("0X")) {
                (h, 16)
            } else {
                (t, 10)
            };
            u64::from_str_radix(digits, radix).map_err(|_| format!("bad number {s:?}"))
        }
        _ => Err(format!("expected a number, got {v}")),
    }
}

fn p_num(p: &Value, k: &str) -> R<Option<u64>> {
    p.get(k).filter(|v| !v.is_null()).map(num).transpose()
}

fn p_req(p: &Value, k: &str) -> R<u64> {
    p_num(p, k)?.ok_or_else(|| format!("missing '{k}'"))
}

fn p_bool(p: &Value, k: &str, d: bool) -> bool {
    p.get(k).and_then(Value::as_bool).unwrap_or(d)
}

fn p_str<'a>(p: &'a Value, k: &str) -> Option<&'a str> {
    p.get(k).and_then(Value::as_str)
}

fn hex(b: &[u8]) -> String {
    b.iter().map(|x| format!("{x:02x}")).collect()
}

fn unhex(s: &str) -> R<Vec<u8>> {
    let s: String = s.chars().filter(|c| !c.is_whitespace()).collect();
    if s.len() % 2 != 0 {
        return Err("hex string has odd length".into());
    }
    (0..s.len() / 2)
        .map(|i| u8::from_str_radix(&s[2 * i..2 * i + 2], 16).map_err(|_| "bad hex".to_string()))
        .collect()
}

fn base64(data: &[u8]) -> String {
    const T: &[u8; 64] = b"ABCDEFGHIJKLMNOPQRSTUVWXYZabcdefghijklmnopqrstuvwxyz0123456789+/";
    let mut s = String::with_capacity(data.len().div_ceil(3) * 4);
    for c in data.chunks(3) {
        let n = (c[0] as u32) << 16 | (*c.get(1).unwrap_or(&0) as u32) << 8 | *c.get(2).unwrap_or(&0) as u32;
        for i in 0..4 {
            if i <= c.len() {
                s.push(T[(n >> (18 - 6 * i) & 63) as usize] as char);
            } else {
                s.push('=');
            }
        }
    }
    s
}

pub fn key_from_name(name: &str) -> R<BbkKey> {
    let up = name.trim().to_ascii_uppercase();
    for code in 0..0x40u8 {
        if let Some(k) = BbkKey::from_code(code) {
            if k.name() == up {
                return Ok(k);
            }
        }
    }
    Err(format!("unknown key {name:?}"))
}

// ----------------------------------------------------------------- state --

#[derive(Clone)]
struct Break {
    id: u64,
    /// CPU address; None = match on physical address alone
    addr: Option<u16>,
    /// physical address the pc must map to (bank-qualified break)
    phys: Option<u32>,
    stop: bool,
    hits: u64,
    /// memory to capture into break.log on each hit
    capture: Vec<Capture>,
}

/// One capture on a breakpoint hit. `deref`: `addr` holds a little-endian
/// pointer and the capture reads from where it points. `cstr`: stop at NUL
/// (`len` is then a maximum). `stack`: capture `len` bytes above the stack
/// pointer instead (return addresses).
#[derive(Clone)]
struct Capture {
    addr: u16,
    len: u16,
    deref: bool,
    cstr: bool,
    stack: bool,
    /// with deref: record the pointer's physical address (6 hex digits) instead of bytes
    phys: bool,
    /// with deref: the pointer at `addr` points at a block; read a second
    /// pointer at block + `ptr_off` and capture from there (C-stack args)
    ptr_off: Option<u16>,
}

#[derive(Clone)]
struct Watch {
    id: u64,
    lo: u32,
    hi: u32,
    /// true: lo/hi are physical addresses; false: CPU addresses
    phys: bool,
    read: bool,
    write: bool,
    value: Option<u8>,
    stop: bool,
    /// append each hit to break.log (with stop:false this is a silent logger)
    log: bool,
    hits: u64,
}

#[derive(Clone)]
struct TraceEnt {
    pc: u16,
    phys: u32,
    bytes: [u8; 3],
    regs: Option<[u8; 5]>,
    mem: Vec<BusAccess>,
}

struct Trace {
    cap: usize,
    ring: VecDeque<TraceEnt>,
    total: u64,
    with_regs: bool,
    with_mem: bool,
}

#[derive(Clone)]
struct Snap {
    emu: Emulator,
    frame_cycles: u32,
    instructions: u64,
    held: Option<BbkKey>,
    /// the recorded route when the snapshot was taken (restored with it, so
    /// loading any snapshot, even from an abandoned branch, keeps the route
    /// consistent with the state)
    rec_events: Option<std::sync::Arc<Vec<route::Event>>>,
}

/// route.record: the inputs actually applied, as a bbkplay route. Loading a
/// snapshot or rewinding truncates it, so it always describes one straight
/// path from boot to the current state.
struct Recorder {
    path: String,
    header: String,
    /// shared with snapshots; copied on the first push after a snapshot
    events: std::sync::Arc<Vec<route::Event>>,
}

impl Recorder {
    fn push(&mut self, e: route::Event) {
        use std::io::Write;
        if let Ok(mut f) = std::fs::OpenOptions::new().append(true).open(&self.path) {
            let _ = writeln!(f, "{}", route::to_line(&e));
        }
        std::sync::Arc::make_mut(&mut self.events).push(e);
    }

    fn rewrite(&self) {
        let mut s = self.header.clone() + "\n";
        for e in self.events.iter() {
            s += &route::to_line(e);
            s.push('\n');
        }
        let _ = std::fs::write(&self.path, s);
    }
}

#[derive(Clone)]
enum InputEv {
    Press(BbkKey),
    Release,
    Poke(u16, Vec<u8>),
}

enum Limit {
    Instructions(u64),
    Frames(u64),
    Until { pc: u16, max: u64 },
}

pub struct Session {
    emu: Option<Emulator>,
    gam: Vec<u8>,
    gam_path: String,
    archive: Option<Archive>,
    frame_cycles: u32,
    instructions: u64,
    held: Option<BbkKey>,
    schedule: BTreeMap<u64, Vec<InputEv>>,
    /// route events from input.replay, applied exactly as bbkplay applies them
    replay: BTreeMap<u64, Vec<route::Event>>,
    rec: Option<Recorder>,
    breaks: Vec<Break>,
    watches: Vec<Watch>,
    next_id: u64,
    skip_break_at: Option<u16>,
    break_log: VecDeque<Value>,
    snapshots: HashMap<String, Snap>,
    rewind: VecDeque<Snap>,
    rewind_cap: usize,
    trace: Option<Trace>,
    coverage: Option<Vec<u8>>, // one bit per flash byte, instruction starts
    search: Option<Vec<(u16, u8)>>,
}

impl Session {
    pub fn new() -> Self {
        Session {
            emu: None,
            gam: Vec::new(),
            gam_path: String::new(),
            archive: None,
            frame_cycles: 0,
            instructions: 0,
            held: None,
            schedule: BTreeMap::new(),
            replay: BTreeMap::new(),
            rec: None,
            breaks: Vec::new(),
            watches: Vec::new(),
            next_id: 1,
            skip_break_at: None,
            break_log: VecDeque::new(),
            snapshots: HashMap::new(),
            rewind: VecDeque::new(),
            rewind_cap: 0,
            trace: None,
            coverage: None,
            search: None,
        }
    }

    fn emu(&self) -> R<&Emulator> {
        self.emu.as_ref().ok_or_else(|| "no game loaded (load_gam first)".to_string())
    }

    fn emu_mut(&mut self) -> R<&mut Emulator> {
        self.emu.as_mut().ok_or_else(|| "no game loaded (load_gam first)".to_string())
    }

    pub fn dispatch(&mut self, cmd: &str, p: &Value) -> R<Value> {
        match cmd {
            "ping" => Ok(json!({"pong": true, "version": VERSION})),
            "quit" => Ok(json!({"bye": true})),
            "load_gam" | "load_rom" => self.load_gam(p),
            "info" => self.info(),
            "regs.get" => self.regs(),
            "regs.set" => self.regs_set(p),
            "step" => {
                let n = p_num(p, "n")?.unwrap_or(1);
                self.run(Limit::Instructions(n))
            }
            "run.frames" => {
                let n = p_num(p, "n")?.unwrap_or(1);
                self.run(Limit::Frames(n))
            }
            "run.until" => {
                let pc = p_req(p, "addr")? as u16;
                let max = p_num(p, "max_instructions")?.unwrap_or(50_000_000);
                self.run(Limit::Until { pc, max })
            }
            "break.add" => self.break_add(p),
            "break.del" => {
                let id = p_req(p, "id")?;
                let n = self.breaks.len();
                self.breaks.retain(|b| b.id != id);
                Ok(json!({"deleted": n != self.breaks.len()}))
            }
            "break.clear" => {
                self.breaks.clear();
                Ok(json!({"cleared": true}))
            }
            "break.list" => Ok(json!({"breakpoints": self.breaks.iter().map(|b| json!({
                "id": b.id, "addr": b.addr.map(|a| format!("{a:04x}")),
                "phys": b.phys.map(|x| format!("{x:06x}")), "stop": b.stop, "hits": b.hits,
            })).collect::<Vec<_>>()})),
            "break.log" => {
                let clear = p_bool(p, "clear", false);
                let max = p_num(p, "max")?.unwrap_or(1000) as usize;
                let n = self.break_log.len();
                let entries: Vec<Value> = self.break_log.iter().skip(n.saturating_sub(max)).cloned().collect();
                if clear {
                    self.break_log.clear();
                }
                Ok(json!({"total": n, "entries": entries}))
            }
            "watch.add" => self.watch_add(p),
            "watch.del" => {
                let id = p_req(p, "id")?;
                let n = self.watches.len();
                self.watches.retain(|w| w.id != id);
                Ok(json!({"deleted": n != self.watches.len()}))
            }
            "watch.clear" => {
                self.watches.clear();
                Ok(json!({"cleared": true}))
            }
            "watch.list" => Ok(json!({"watchpoints": self.watches.iter().map(|w| json!({
                "id": w.id, "lo": format!("{:x}", w.lo), "hi": format!("{:x}", w.hi), "phys": w.phys,
                "read": w.read, "write": w.write, "stop": w.stop, "hits": w.hits,
            })).collect::<Vec<_>>()})),
            "mem.read" => self.mem_read(p),
            "mem.write" => self.mem_write(p),
            "mem.search" => self.mem_search(p),
            "mem.search.reset" => {
                self.search = None;
                Ok(json!({"reset": true}))
            }
            "rom.search" | "gam.search" => self.gam_search(p),
            "disasm" => self.disasm(p),
            "input.press" => {
                let k = key_from_name(p_str(p, "key").ok_or("missing 'key'")?)?;
                self.press(k)?;
                Ok(json!({"held": k.name()}))
            }
            "input.release" => {
                self.release()?;
                Ok(json!({"held": Value::Null}))
            }
            "input.tap" => self.input_tap(p),
            "input.script" => self.input_script(p),
            "input.replay" => self.input_replay(p),
            "route.record" => self.route_record(p),
            "route.mark" => self.route_mark(p),
            "route.stop" => {
                let frame = self.emu()?.frame_count();
                match self.rec.take() {
                    Some(mut r) => {
                        r.push(route::Event { frame, action: route::Action::End });
                        Ok(json!({"path": r.path, "events": r.events.len(), "frame": frame}))
                    }
                    None => Err("not recording".into()),
                }
            }
            "route.status" => Ok(match &self.rec {
                Some(r) => json!({"recording": true, "path": r.path, "events": r.events.len()}),
                None => json!({"recording": false}),
            }),
            "screen.capture" => self.screen_capture(p),
            "snapshot.save" => self.snapshot_save(p),
            "snapshot.load" => self.snapshot_load(p),
            "snapshot.list" => {
                let mut names: Vec<&String> = self.snapshots.keys().collect();
                names.sort();
                Ok(json!({"snapshots": names}))
            }
            "snapshot.delete" => {
                let name = p_str(p, "name").ok_or("missing 'name'")?;
                Ok(json!({"deleted": self.snapshots.remove(name).is_some()}))
            }
            "rewind.set" => {
                let frames = p_num(p, "frames")?.or(p_num(p, "seconds")?.map(|s| s * 60)).unwrap_or(0);
                self.rewind_cap = frames.min(60 * 60) as usize;
                self.rewind.clear();
                Ok(json!({"frames": self.rewind_cap}))
            }
            "rewind.pop" => self.rewind_pop(p),
            "trace.start" => {
                let cap = p_num(p, "max")?.unwrap_or(65536).min(4 << 20) as usize;
                self.trace = Some(Trace {
                    cap,
                    ring: VecDeque::new(),
                    total: 0,
                    with_regs: p_bool(p, "with_regs", false),
                    with_mem: p_bool(p, "with_mem", false),
                });
                Ok(json!({"tracing": true, "capacity": cap}))
            }
            "trace.stop" => {
                let total = self.trace.as_ref().map_or(0, |t| t.total);
                let held = self.trace.as_ref().map_or(0, |t| t.ring.len());
                if let Some(t) = self.trace.as_mut() {
                    t.cap = 0; // keep the ring for trace.dump, stop recording
                }
                Ok(json!({"tracing": false, "total": total, "held": held}))
            }
            "trace.dump" => self.trace_dump(p),
            "coverage.get" => self.coverage_get(p),
            "coverage.reset" => {
                if let Some(c) = self.coverage.as_mut() {
                    c.iter_mut().for_each(|b| *b = 0);
                }
                Ok(json!({"reset": true}))
            }
            "lib.map" => self.lib_map(p),
            "flash.load_lib" => self.flash_load_lib(p),
            _ => Err(format!("unknown command {cmd:?}")),
        }
    }

    // ------------------------------------------------------------ session --

    fn load_gam(&mut self, p: &Value) -> R<Value> {
        let path = p_str(p, "path").ok_or("missing 'path'")?;
        let data = std::fs::read(path).map_err(|e| format!("{path}: {e}"))?;
        let m = match p_str(p, "model").unwrap_or("4988") {
            "4980" => &model::MODEL_4980,
            "4988" => &model::MODEL_4988,
            other => return Err(format!("unknown model {other:?} (4980 or 4988)")),
        };
        let dir = p_str(p, "rom_dir");
        let rom = |name: &str, key: &str| -> R<Option<Vec<u8>>> {
            let path = match (p_str(p, key), dir) {
                (Some(x), _) => x.to_string(),
                (None, Some(d)) => format!("{d}/{name}"),
                (None, None) => return Ok(None),
            };
            std::fs::read(&path).map(Some).map_err(|e| format!("{path}: {e}"))
        };
        let mut emu = Emulator::new(m);
        if let Some(r8) = rom("8.BIN", "rom8")? {
            emu.load_rom_8(&r8);
        }
        match rom("E.BIN", "rome")? {
            Some(re) => emu.load_rom_e(&re),
            None => return Err("E.BIN is required (pass rome or rom_dir)".into()),
        }
        emu.load_gam(&data).map_err(|e| e.to_string())?;
        self.archive = Archive::parse(&data);
        self.gam = data;
        self.gam_path = path.to_string();
        self.emu = Some(emu);
        self.frame_cycles = 0;
        self.instructions = 0;
        self.held = None;
        self.schedule.clear();
        self.replay.clear();
        self.rec = None;
        self.breaks.clear();
        self.watches.clear();
        self.break_log.clear();
        self.snapshots.clear();
        self.rewind.clear();
        self.trace = None;
        self.coverage = None;
        self.search = None;
        self.skip_break_at = None;
        self.info()
    }

    fn info(&self) -> R<Value> {
        let e = self.emu()?;
        let name_raw = &self.gam[6..0x10];
        let end = name_raw.iter().position(|&b| b == 0).unwrap_or(name_raw.len());
        Ok(json!({
            "path": self.gam_path,
            "size": self.gam.len(),
            "name_hex": hex(&name_raw[..end]),
            "entry": format!("{:04x}", u16::from_le_bytes([self.gam[0x40], self.gam[0x41]])),
            "data_offset": format!("{:x}", u32::from_le_bytes(self.gam[0x42..0x46].try_into().unwrap())),
            "archive": self.archive.as_ref().map(|a| json!({"offset": format!("{:x}", a.base), "size": a.len})),
            "model": e.model().name,
            "frame": e.frame_count(),
            "instructions": self.instructions,
            "running": e.is_running(),
        }))
    }

    fn regs(&self) -> R<Value> {
        let e = self.emu()?;
        let c = &e.cpu;
        let banks: Vec<String> = e.cpu.memory().bank_switch.banks.iter().map(|b| format!("{b:x}")).collect();
        Ok(json!({
            "pc": format!("{:04x}", c.pc()), "a": format!("{:02x}", c.a()), "x": format!("{:02x}", c.x()),
            "y": format!("{:02x}", c.y()), "sp": format!("{:02x}", c.sp()), "p": format!("{:02x}", c.status()),
            "pc_phys": format!("{:06x}", c.memory().physical(c.pc())),
            "banks": banks, "halted": e.is_halted(), "frame": e.frame_count(),
            "frame_cycle": self.frame_cycles, "cycles": c.cycles(), "instructions": self.instructions,
        }))
    }

    fn regs_set(&mut self, p: &Value) -> R<Value> {
        let e = self.emu_mut()?;
        let r = &mut e.cpu.inner.registers;
        if let Some(v) = p_num(p, "pc")? {
            r.program_counter = v as u16;
        }
        if let Some(v) = p_num(p, "a")? {
            r.accumulator = v as u8;
        }
        if let Some(v) = p_num(p, "x")? {
            r.index_x = v as u8;
        }
        if let Some(v) = p_num(p, "y")? {
            r.index_y = v as u8;
        }
        if let Some(v) = p_num(p, "sp")? {
            r.stack_pointer.0 = v as u8;
        }
        self.regs()
    }

    // ---------------------------------------------------------------- run --

    fn needs_accesses(&self) -> bool {
        !self.watches.is_empty() || self.trace.as_ref().is_some_and(|t| t.with_mem && t.cap > 0)
    }

    fn on_frame_start(&mut self) {
        self.on_frame_start_inputs_only();
        let Some(emu) = self.emu.as_mut() else { return };
        emu.begin_frame();
        if self.rewind_cap > 0 {
            let snap = Snap {
                emu: emu.clone(), frame_cycles: 0, instructions: self.instructions, held: self.held,
                rec_events: self.rec.as_ref().map(|r| r.events.clone()),
            };
            self.rewind.push_back(snap);
            while self.rewind.len() > self.rewind_cap {
                self.rewind.pop_front();
            }
        }
    }

    /// Apply the route and input events due at the current frame start.
    fn on_frame_start_inputs_only(&mut self) {
        let Some(emu) = self.emu.as_mut() else { return };
        let f = emu.frame_count();
        let due: Vec<u64> = self.replay.range(..=f).map(|(k, _)| *k).collect();
        for k in due {
            for ev in self.replay.remove(&k).unwrap_or_default() {
                route::apply(emu, &ev);
            }
        }
        // apply every input event due at or before this frame
        let due: Vec<u64> = self.schedule.range(..=f).map(|(k, _)| *k).collect();
        for k in due {
            for ev in self.schedule.remove(&k).unwrap_or_default() {
                let action = match ev {
                    InputEv::Press(key) => {
                        self.held = Some(key);
                        route::Action::Down(key)
                    }
                    InputEv::Release => {
                        self.held = None;
                        route::Action::Up
                    }
                    InputEv::Poke(a, d) => route::Action::Poke(a, d),
                };
                let e = route::Event { frame: f, action };
                route::apply(emu, &e);
                if let Some(r) = self.rec.as_mut() {
                    r.push(e);
                }
            }
        }
    }

    fn run(&mut self, limit: Limit) -> R<Value> {
        self.emu()?;
        let start_instr = self.instructions;
        let start_frame = self.emu()?.frame_count();
        let record = self.needs_accesses();
        let mut stop: Option<(String, Value)> = None;
        let mut frames_done = 0u64;
        let check_breaks = !self.breaks.is_empty();
        let phys_breaks = self.breaks.iter().any(|b| b.addr.is_none());
        let tracing = self.trace.as_ref().is_some_and(|t| t.cap > 0);

        loop {
            if self.frame_cycles == 0 {
                self.on_frame_start();
            }
            let emu = self.emu.as_mut().unwrap();
            if !emu.is_running() {
                stop = Some(match emu.illegal_at {
                    Some(pc) => ("illegal_opcode".into(), json!({"pc": format!("{pc:04x}"),
                        "phys": format!("{:06x}", emu.cpu.memory().physical(pc))})),
                    None => ("exited".into(), json!({})),
                });
                break;
            }
            let halted = emu.is_halted();
            let pc = emu.cpu.pc();

            if !halted {
                if let Limit::Until { pc: target, .. } = limit {
                    if pc == target && self.instructions > start_instr {
                        stop = Some(("until".into(), json!({"pc": format!("{pc:04x}")})));
                        break;
                    }
                }
                if check_breaks && self.skip_break_at != Some(pc)
                    && (phys_breaks || self.breaks.iter().any(|b| b.addr == Some(pc)))
                {
                    let phys = emu.cpu.memory().physical(pc);
                    let mut halt_here = None;
                    for b in self.breaks.iter_mut() {
                        let hit = match b.addr {
                            Some(a) => a == pc && b.phys.is_none_or(|x| x == phys),
                            None => b.phys == Some(phys),
                        };
                        if hit {
                            b.hits += 1;
                            let mut ent = json!({
                                "id": b.id, "pc": format!("{pc:04x}"), "phys": format!("{phys:06x}"),
                                "frame": emu.frame_count(), "a": format!("{:02x}", emu.cpu.a()),
                                "x": format!("{:02x}", emu.cpu.x()), "y": format!("{:02x}", emu.cpu.y()),
                            });
                            if !b.capture.is_empty() {
                                let m = emu.cpu.memory();
                                let caps: Vec<String> = b.capture.iter().map(|c| {
                                    let base = if c.stack {
                                        0x101u16 + emu.cpu.sp() as u16
                                    } else if c.deref {
                                        let p = m.read(c.addr) as u16 | (m.read(c.addr.wrapping_add(1)) as u16) << 8;
                                        match c.ptr_off {
                                            Some(o) => {
                                                let q = p.wrapping_add(o);
                                                m.read(q) as u16 | (m.read(q.wrapping_add(1)) as u16) << 8
                                            }
                                            None => p,
                                        }
                                    } else {
                                        c.addr
                                    };
                                    if c.phys {
                                        return format!("{:06x}", m.physical(base));
                                    }
                                    let mut out = Vec::new();
                                    for i in 0..c.len {
                                        let v = m.read(base.wrapping_add(i));
                                        if c.cstr && v == 0 {
                                            break;
                                        }
                                        out.push(v);
                                    }
                                    hex(&out)
                                }).collect();
                                ent["mem"] = json!(caps);
                            }
                            self.break_log.push_back(ent.clone());
                            if self.break_log.len() > 100_000 {
                                self.break_log.pop_front();
                            }
                            if b.stop && halt_here.is_none() {
                                halt_here = Some(ent);
                            }
                        }
                    }
                    if let Some(ent) = halt_here {
                        self.skip_break_at = Some(pc);
                        stop = Some(("breakpoint".into(), ent));
                        break;
                    }
                }
            }
            self.skip_break_at = None;

            let emu = self.emu.as_mut().unwrap();
            if record {
                emu.cpu.memory_mut().record_accesses = true;
                emu.cpu.memory_mut().accesses.clear();
            }
            let pre_regs = [emu.cpu.a(), emu.cpu.x(), emu.cpu.y(), emu.cpu.sp(), emu.cpu.status()];
            let pc_phys = emu.cpu.memory().physical(pc);
            let bytes = [
                emu.cpu.memory().read(pc),
                emu.cpu.memory().read(pc.wrapping_add(1)),
                emu.cpu.memory().read(pc.wrapping_add(2)),
            ];
            let cycles = emu.step_timed();
            let accesses = if record {
                emu.cpu.memory_mut().record_accesses = false;
                std::mem::take(&mut emu.cpu.memory_mut().accesses)
            } else {
                Vec::new()
            };

            if !halted {
                self.instructions += 1;
                if let Some(cov) = self.coverage.as_mut() {
                    if (FLASH_BASE..FLASH_BASE + 0x200000).contains(&pc_phys) {
                        let i = (pc_phys - FLASH_BASE) as usize;
                        cov[i >> 3] |= 1 << (i & 7);
                    }
                }
                if tracing {
                    let t = self.trace.as_mut().unwrap();
                    let ilen = disasm::length(bytes[0]);
                    let mem = if t.with_mem {
                        accesses.iter().filter(|a| a.write || !(pc..pc.wrapping_add(ilen)).contains(&a.addr))
                            .take(4).copied().collect()
                    } else {
                        Vec::new()
                    };
                    t.ring.push_back(TraceEnt { pc, phys: pc_phys, bytes, regs: t.with_regs.then_some(pre_regs), mem });
                    t.total += 1;
                    while t.ring.len() > t.cap {
                        t.ring.pop_front();
                    }
                }
            }

            if !accesses.is_empty() && !self.watches.is_empty() {
                let ilen = disasm::length(bytes[0]);
                let mut hit = None;
                for a in &accesses {
                    // instruction fetches are not data reads
                    if !a.write && (pc..pc.wrapping_add(ilen)).contains(&a.addr) {
                        continue;
                    }
                    for w in self.watches.iter_mut() {
                        let at = if w.phys { a.paddr } else { a.addr as u32 };
                        if at < w.lo || at > w.hi || !(if a.write { w.write } else { w.read }) {
                            continue;
                        }
                        if a.write && w.value.is_some_and(|v| v != a.value) {
                            continue;
                        }
                        w.hits += 1;
                        if w.stop || w.log {
                            let ent = json!({
                                "id": w.id, "access": if a.write {"w"} else {"r"},
                                "addr": format!("{:04x}", a.addr), "phys": format!("{:06x}", a.paddr),
                                "value": format!("{:02x}", a.value), "pc": format!("{pc:04x}"),
                                "pc_phys": format!("{pc_phys:06x}"),
                            });
                            if w.log {
                                self.break_log.push_back(ent.clone());
                                if self.break_log.len() > 100_000 {
                                    self.break_log.pop_front();
                                }
                            }
                            if w.stop && hit.is_none() {
                                hit = Some(ent);
                            }
                        }
                    }
                }
                if let Some(h) = hit {
                    stop = Some(("watchpoint".into(), h));
                }
            }

            let emu = self.emu.as_mut().unwrap();
            self.frame_cycles += cycles;
            if self.frame_cycles >= emu.frame_cycle_budget() {
                emu.end_frame();
                self.frame_cycles = 0;
                frames_done += 1;
            }
            if stop.is_some() {
                break;
            }
            match limit {
                Limit::Instructions(n) if self.instructions - start_instr >= n => break,
                Limit::Frames(n) if frames_done >= n => break,
                Limit::Until { max, .. } if self.instructions - start_instr >= max => {
                    stop = Some(("max_instructions".into(), json!({})));
                    break;
                }
                _ => {}
            }
        }

        let emu = self.emu()?;
        let mut out = json!({
            "ran_instructions": self.instructions - start_instr,
            "ran_frames": emu.frame_count() - start_frame,
            "pc": format!("{:04x}", emu.cpu.pc()),
            "frame": emu.frame_count(),
            "instructions_total": self.instructions,
            "stopped": stop.is_some(),
        });
        if let Some((reason, detail)) = stop {
            out["reason"] = json!(reason);
            out["detail"] = detail;
        }
        Ok(out)
    }

    // -------------------------------------------------------- breakpoints --

    fn break_add(&mut self, p: &Value) -> R<Value> {
        let addr = p_num(p, "addr")?.map(|a| a as u16);
        let phys = match (p_num(p, "phys")?, p_num(p, "gam")?) {
            (Some(x), _) => Some(x as u32),
            (None, Some(off)) => Some(GAM_FLASH + off as u32),
            _ => None,
        };
        if addr.is_none() && phys.is_none() {
            return Err("break.add needs addr, phys or gam".into());
        }
        let mut capture = Vec::new();
        if let Some(arr) = p.get("capture").and_then(Value::as_array) {
            for c in arr {
                let stack = p_bool(c, "stack", false);
                capture.push(Capture {
                    addr: if stack { 0 } else { p_req(c, "addr")? as u16 },
                    len: p_num(c, "len")?.unwrap_or(16).min(4096) as u16,
                    deref: p_bool(c, "deref", false),
                    cstr: p_bool(c, "cstr", false),
                    stack,
                    phys: p_bool(c, "phys", false),
                    ptr_off: p_num(c, "ptr_off")?.map(|v| v as u16),
                });
            }
        }
        let id = self.next_id;
        self.next_id += 1;
        self.breaks.push(Break { id, addr, phys, stop: p_bool(p, "stop", true), hits: 0, capture });
        Ok(json!({"id": id, "addr": addr.map(|a| format!("{a:04x}")), "phys": phys.map(|x| format!("{x:06x}"))}))
    }

    fn watch_add(&mut self, p: &Value) -> R<Value> {
        let (lo, phys) = if let Some(a) = p_num(p, "addr")? {
            (a as u32, false)
        } else if let Some(a) = p_num(p, "phys")? {
            (a as u32, true)
        } else if let Some(off) = p_num(p, "gam")? {
            (GAM_FLASH + off as u32, true)
        } else {
            return Err("watch.add needs addr, phys or gam".into());
        };
        let hi = match p_num(p, "end")? {
            Some(e) if p.get("gam").is_some() && p.get("phys").is_none() && p.get("addr").is_none() => GAM_FLASH + e as u32,
            Some(e) => e as u32,
            None => lo,
        };
        let access = p_str(p, "access").unwrap_or("w");
        let id = self.next_id;
        self.next_id += 1;
        self.watches.push(Watch {
            id, lo, hi, phys,
            read: access.contains('r'),
            write: access.contains('w'),
            value: p_num(p, "value")?.map(|v| v as u8),
            stop: p_bool(p, "stop", true),
            log: p_bool(p, "log", false),
            hits: 0,
        });
        Ok(json!({"id": id, "lo": format!("{lo:x}"), "hi": format!("{hi:x}"), "phys": phys}))
    }

    // ------------------------------------------------------------- memory --

    /// Resolve an address param set to a reader closure description.
    fn mem_read(&self, p: &Value) -> R<Value> {
        let e = self.emu()?;
        let len = p_num(p, "len")?.unwrap_or(16).min(0x10000) as u32;
        let m = e.cpu.memory();
        if let Some(a) = p_num(p, "addr")? {
            let data: Vec<u8> = (0..len).map(|i| m.read((a as u32 + i) as u16)).collect();
            return Ok(json!({"addr": format!("{a:04x}"), "len": len, "data": hex(&data)}));
        }
        let base = match (p_num(p, "phys")?, p_num(p, "gam")?) {
            (Some(x), _) => x as u32,
            (None, Some(off)) => GAM_FLASH + off as u32,
            _ => return Err("mem.read needs addr, phys or gam".into()),
        };
        let data: Vec<u8> = (0..len).map(|i| m.read_physical(base + i)).collect();
        Ok(json!({"phys": format!("{base:06x}"), "len": len, "data": hex(&data)}))
    }

    fn mem_write(&mut self, p: &Value) -> R<Value> {
        let data = unhex(p_str(p, "data").ok_or("missing 'data'")?)?;
        let addr = p_num(p, "addr")?;
        let phys = match (p_num(p, "phys")?, p_num(p, "gam")?) {
            (Some(x), _) => Some(x as u32),
            (None, Some(off)) => Some(GAM_FLASH + off as u32),
            _ => None,
        };
        if let (Some(a), true) = (addr, self.rec.is_some()) {
            // recording: a CPU write is part of the route (cheats), applied at
            // the next frame start like an input so it replays identically
            let at = self.input_frame()?;
            self.schedule.entry(at).or_default().push(InputEv::Poke(a as u16, data.clone()));
            return Ok(json!({"written": data.len(), "scheduled_frame": at}));
        }
        let e = self.emu_mut()?;
        let m = e.cpu.memory_mut();
        if let Some(a) = addr {
            for (i, b) in data.iter().enumerate() {
                m.write((a as usize + i) as u16, *b);
            }
        } else if let Some(base) = phys {
            for (i, b) in data.iter().enumerate() {
                let pa = base + i as u32;
                if pa < 0x8000 {
                    m.ram[pa as usize] = *b;
                } else if (FLASH_BASE..FLASH_BASE + 0x200000).contains(&pa) {
                    m.flash[bbkemu_core::memory::flash_index(pa - FLASH_BASE)] = *b;
                } else {
                    return Err(format!("{pa:06x} is not RAM or flash"));
                }
            }
        } else {
            return Err("mem.write needs addr, phys or gam".into());
        }
        Ok(json!({"written": data.len()}))
    }

    fn mem_search(&mut self, p: &Value) -> R<Value> {
        let filter = p_str(p, "filter").ok_or("missing 'filter'")?.to_string();
        let max = p_num(p, "max")?.unwrap_or(256) as usize;
        let lo = p_num(p, "lo")?.unwrap_or(0x100) as u16;
        let hi = p_num(p, "hi")?.unwrap_or(0x7fff) as u16;
        let terms = parse_filter(&filter)?;
        let prev_state = self.search.take();
        let e = self.emu()?;
        let ram = &e.cpu.memory().ram;
        let prev: Vec<(u16, u8)> = match prev_state {
            Some(v) => v,
            None => (lo..=hi).map(|a| (a, 0)).collect(),
        };
        let next: Vec<(u16, u8)> = prev
            .into_iter()
            .filter_map(|(a, old)| {
                let new = ram[a as usize];
                terms.iter().all(|t| t.eval(new, old)).then_some((a, new))
            })
            .collect();
        let results: Vec<Value> = next.iter().take(max)
            .map(|(a, v)| json!({"addr": format!("{a:04x}"), "value": v})).collect();
        let count = next.len();
        self.search = Some(next);
        Ok(json!({"count": count, "results": results}))
    }

    fn gam_search(&self, p: &Value) -> R<Value> {
        let needle = unhex(p_str(p, "bytes").ok_or("missing 'bytes'")?)?;
        if needle.is_empty() {
            return Err("empty needle".into());
        }
        let max = p_num(p, "max")?.unwrap_or(512) as usize;
        let mut res = Vec::new();
        let mut count = 0;
        for (i, w) in self.gam.windows(needle.len()).enumerate() {
            if w == needle.as_slice() {
                count += 1;
                if res.len() < max {
                    res.push(json!({"off": format!("{i:x}"), "phys": format!("{:06x}", GAM_FLASH + i as u32)}));
                }
            }
        }
        Ok(json!({"count": count, "results": res}))
    }

    fn disasm(&self, p: &Value) -> R<Value> {
        let e = self.emu()?;
        let mut pc = p_num(p, "addr")?.map_or(e.cpu.pc(), |v| v as u16);
        let n = p_num(p, "n")?.unwrap_or(16).min(512);
        let m = e.cpu.memory();
        let rd = |a: u16| m.read(a);
        let mut lines = Vec::new();
        for _ in 0..n {
            let (text, len) = disasm::format(pc, &rd);
            let bytes: Vec<u8> = (0..len).map(|i| m.read(pc.wrapping_add(i))).collect();
            lines.push(format!("{pc:04x} [{:06x}] {:<8} {text}", m.physical(pc), hex(&bytes)));
            pc = pc.wrapping_add(len);
        }
        Ok(json!({"listing": lines}))
    }

    // -------------------------------------------------------------- input --

    /// Frame at which an input given now takes effect (inputs apply at frame starts).
    fn input_frame(&self) -> R<u64> {
        Ok(self.emu()?.frame_count() + if self.frame_cycles > 0 { 1 } else { 0 })
    }

    fn press(&mut self, k: BbkKey) -> R<()> {
        let at = self.input_frame()?;
        self.schedule.entry(at).or_default().push(InputEv::Press(k));
        Ok(())
    }

    fn release(&mut self) -> R<()> {
        let at = self.input_frame()?;
        self.schedule.entry(at).or_default().push(InputEv::Release);
        Ok(())
    }

    /// route.record: start recording inputs to `path`. If the file exists and
    /// `resume` (default true), it is replayed first (only right after
    /// load_gam) and recording continues after it.
    fn route_record(&mut self, p: &Value) -> R<Value> {
        let path = p_str(p, "path").ok_or("missing 'path'")?.to_string();
        let header = route::header(&self.gam, self.emu()?.model().name);
        let mut events = Vec::new();
        if std::path::Path::new(&path).exists() && p_bool(p, "resume", true) {
            if self.emu()?.frame_count() != 0 || self.instructions != 0 {
                return Err("resuming a route needs a fresh load_gam".into());
            }
            let text = std::fs::read_to_string(&path).map_err(|e| format!("{path}: {e}"))?;
            for (n, line) in text.lines().enumerate() {
                if let Some((hash, _)) = route::parse_header(line) {
                    if hash != route::gam_hash(&self.gam) {
                        return Err(format!("{path} was recorded on a different .gam"));
                    }
                    continue;
                }
                if let Some(e) = route::parse_line(line).map_err(|e| format!("{path}:{}: {e}", n + 1))? {
                    events.push(e);
                }
            }
            // resume where the last session stopped (its End), then drop the End
            let last = events.iter().map(|e| e.frame).max().unwrap_or(0);
            events.retain(|e| e.action != route::Action::End);
            for e in &events {
                self.replay.entry(e.frame).or_default().push(e.clone());
            }
            self.rec = Some(Recorder { path, header, events: std::sync::Arc::new(events) });
            self.rec.as_ref().unwrap().rewrite();
            let n = self.rec.as_ref().unwrap().events.len();
            let r = if last > 0 { self.run(Limit::Frames(last))? } else { json!({}) };
            // events stamped with the last frame are still pending; apply them now
            if self.frame_cycles == 0 {
                self.on_frame_start_inputs_only();
            }
            return Ok(json!({"resumed": n, "frame": self.emu()?.frame_count(), "run": r}));
        }
        let rec = Recorder { path, header, events: std::sync::Arc::new(events) };
        rec.rewrite();
        self.rec = Some(rec);
        Ok(json!({"recording": true, "frame": self.emu()?.frame_count()}))
    }

    fn route_mark(&mut self, p: &Value) -> R<Value> {
        let text = p_str(p, "text").unwrap_or("mark").to_string();
        let frame = self.input_frame()?;
        let r = self.rec.as_mut().ok_or("not recording (route.record first)")?;
        r.push(route::Event { frame, action: route::Action::Mark(text) });
        Ok(json!({"frame": frame, "events": r.events.len()}))
    }

    /// Queue key events relative to the current frame. `steps` items:
    /// {key, hold (frames, default 4), wait (frames after release, default 4)}.
    fn queue(&mut self, steps: &[Value]) -> R<u64> {
        let now = self.emu()?.frame_count();
        let mut at = now + if self.frame_cycles > 0 { 1 } else { 0 };
        for s in steps {
            let hold = p_num(s, "hold")?.unwrap_or(4).max(1);
            let wait = p_num(s, "wait")?.unwrap_or(4);
            match p_str(s, "key") {
                Some(name) => {
                    let k = key_from_name(name)?;
                    self.schedule.entry(at).or_default().push(InputEv::Press(k));
                    self.schedule.entry(at + hold).or_default().push(InputEv::Release);
                    at += hold + wait;
                }
                None => at += wait.max(hold), // pure wait
            }
        }
        Ok(at - now)
    }

    fn input_tap(&mut self, p: &Value) -> R<Value> {
        let frames = self.queue(&[p.clone()])?;
        if p_bool(p, "run", true) {
            let mut r = self.run(Limit::Frames(frames))?;
            r["key"] = json!(p_str(p, "key"));
            return Ok(r);
        }
        Ok(json!({"queued_frames": frames}))
    }

    fn input_script(&mut self, p: &Value) -> R<Value> {
        let steps = p.get("steps").and_then(Value::as_array).ok_or("missing 'steps' array")?.clone();
        let frames = self.queue(&steps)?;
        if p_bool(p, "run", true) {
            return self.run(Limit::Frames(frames));
        }
        Ok(json!({"queued_frames": frames}))
    }

    /// Replay a bbkplay route. Events must not be in the past; normally this
    /// runs right after load_gam. Runs to the route's last frame (or
    /// `until_frame`) unless run:false.
    fn input_replay(&mut self, p: &Value) -> R<Value> {
        let path = p_str(p, "path").ok_or("missing 'path'")?;
        let text = std::fs::read_to_string(path).map_err(|e| format!("{path}: {e}"))?;
        let now = self.emu()?.frame_count();
        let any_gam = p_bool(p, "any_gam", false);
        let mut events = Vec::new();
        let mut marks = Vec::new();
        for (n, line) in text.lines().enumerate() {
            if let Some((hash, _)) = route::parse_header(line) {
                if hash != route::gam_hash(&self.gam) && !any_gam {
                    return Err(format!("{path} was recorded on a different .gam"));
                }
                continue;
            }
            if let Some(e) = route::parse_line(line).map_err(|e| format!("{path}:{}: {e}", n + 1))? {
                if e.frame < now {
                    return Err(format!("{path}:{}: frame {} is already past (now {now})", n + 1, e.frame));
                }
                if let route::Action::Mark(m) = &e.action {
                    marks.push(json!({"frame": e.frame, "mark": m}));
                }
                events.push(e);
            }
        }
        let last = events.iter().map(|e| e.frame).max().unwrap_or(now);
        let n = events.len();
        for e in events {
            if let Some(r) = self.rec.as_mut() {
                if e.action != route::Action::End {
                    r.push(e.clone());
                }
            }
            self.replay.entry(e.frame).or_default().push(e);
        }
        let until = p_num(p, "until_frame")?.unwrap_or(last);
        let mut out = json!({"events": n, "last_frame": last, "marks": marks});
        if p_bool(p, "run", true) && until > now {
            let r = self.run(Limit::Frames(until - now))?;
            out["run"] = r;
        }
        Ok(out)
    }

    // ------------------------------------------------------------- screen --

    fn screen_capture(&mut self, p: &Value) -> R<Value> {
        let scale = p_num(p, "scale")?.unwrap_or(1).clamp(1, 16) as usize;
        let e = self.emu_mut()?;
        let px = e.render_lcd_buffer();
        let mut h: u64 = 0xcbf29ce484222325;
        for &b in px.iter() {
            h = (h ^ b as u64).wrapping_mul(0x100000001b3);
        }
        let (w, ht) = (LCD_W * scale, LCD_H * scale);
        let mut gray = vec![0u8; w * ht];
        for y in 0..ht {
            for x in 0..w {
                gray[y * w + x] = if px[(y / scale) * LCD_W + x / scale] { 0x10 } else { 0xd8 };
            }
        }
        let png = png::encode_gray(w, ht, &gray);
        let mut out = json!({"width": w, "height": ht, "hash": format!("{h:016x}"), "frame": e.frame_count()});
        match p_str(p, "path") {
            Some(path) => {
                std::fs::write(path, &png).map_err(|e| format!("{path}: {e}"))?;
                out["path"] = json!(path);
            }
            None => out["png_base64"] = json!(base64(&png)),
        }
        Ok(out)
    }

    // ---------------------------------------------------------- snapshots --

    fn snap(&self) -> R<Snap> {
        Ok(Snap {
            emu: self.emu()?.clone(), frame_cycles: self.frame_cycles, instructions: self.instructions,
            held: self.held, rec_events: self.rec.as_ref().map(|r| r.events.clone()),
        })
    }

    fn restore(&mut self, s: Snap) {
        if let (Some(r), Some(ev)) = (self.rec.as_mut(), s.rec_events) {
            if !std::sync::Arc::ptr_eq(&r.events, &ev) {
                r.events = ev;
                r.rewrite();
            }
        }
        self.emu = Some(s.emu);
        self.frame_cycles = s.frame_cycles;
        self.instructions = s.instructions;
        self.held = s.held;
        self.schedule.clear();
        self.replay.clear();
        self.skip_break_at = None;
    }

    fn snapshot_save(&mut self, p: &Value) -> R<Value> {
        let name = p_str(p, "name").ok_or("missing 'name' (file snapshots are not supported yet)")?;
        let s = self.snap()?;
        let frame = s.emu.frame_count();
        self.snapshots.insert(name.to_string(), s);
        Ok(json!({"name": name, "frame": frame}))
    }

    fn snapshot_load(&mut self, p: &Value) -> R<Value> {
        let name = p_str(p, "name").ok_or("missing 'name'")?;
        let s = self.snapshots.get(name).cloned().ok_or_else(|| format!("no snapshot {name:?}"))?;
        self.restore(s);
        self.regs()
    }

    fn rewind_pop(&mut self, p: &Value) -> R<Value> {
        let n = p_num(p, "frames")?.unwrap_or(1).max(1) as usize;
        if self.rewind.is_empty() {
            return Err("rewind buffer empty (rewind.set first)".into());
        }
        let keep = self.rewind.len().saturating_sub(n);
        self.rewind.truncate(keep.max(1));
        let s = self.rewind.pop_back().unwrap();
        self.restore(s);
        Ok(json!({"frame": self.emu()?.frame_count()}))
    }

    // ------------------------------------------------------ trace/coverage --

    fn trace_dump(&self, p: &Value) -> R<Value> {
        let t = self.trace.as_ref().ok_or("trace not started")?;
        let limit = p_num(p, "limit")?.unwrap_or(1000).min(100_000) as usize;
        let offset = p_num(p, "offset")?.unwrap_or(0) as usize;
        let tail = p_bool(p, "tail", false);
        let n = t.ring.len();
        let (from, to) = if tail {
            let to = n.saturating_sub(offset);
            (to.saturating_sub(limit), to)
        } else {
            let from = offset.min(n);
            (from, (from + limit).min(n))
        };
        let entries: Vec<Value> = t.ring.range(from..to).map(|e| {
            let rd = |a: u16| e.bytes[(a.wrapping_sub(e.pc)) as usize % 3];
            let (text, _) = disasm::format(e.pc, &rd);
            let mut v = json!({"pc": format!("{:04x}", e.pc), "phys": format!("{:06x}", e.phys), "op": text});
            if let Some(r) = e.regs {
                v["regs"] = json!(format!("a={:02x} x={:02x} y={:02x} sp={:02x} p={:02x}", r[0], r[1], r[2], r[3], r[4]));
            }
            if !e.mem.is_empty() {
                v["mem"] = json!(e.mem.iter().map(|a| json!([if a.write {"w"} else {"r"},
                    format!("{:04x}", a.addr), format!("{:02x}", a.value), format!("{:06x}", a.paddr)])).collect::<Vec<_>>());
            }
            v
        }).collect();
        Ok(json!({"total": t.total, "held": n, "entries": entries}))
    }

    fn coverage_get(&mut self, p: &Value) -> R<Value> {
        if p_bool(p, "arm", false) && self.coverage.is_none() {
            self.coverage = Some(vec![0u8; 0x200000 / 8]);
        }
        let Some(cov) = self.coverage.as_ref() else {
            return Ok(json!({"armed": false}));
        };
        let max_ranges = p_num(p, "max_ranges")?.unwrap_or(256) as usize;
        let bit = |i: usize| cov[i >> 3] & (1 << (i & 7)) != 0;
        let gam_lo = (GAM_FLASH - FLASH_BASE) as usize;
        let gam_hi = gam_lo + self.gam.len();
        let mut ranges = Vec::new();
        let mut count = 0usize;
        let mut i = gam_lo;
        while i < gam_hi.min(0x200000) {
            if bit(i) {
                let s = i;
                let mut last = i;
                // instruction starts are at most 3 bytes apart inside a run
                while i < gam_hi && (bit(i) || i - last < 3) {
                    if bit(i) {
                        last = i;
                        count += 1;
                    }
                    i += 1;
                }
                if ranges.len() < max_ranges {
                    ranges.push(json!([format!("{:x}", s - gam_lo), format!("{:x}", last - gam_lo)]));
                }
            } else {
                i += 1;
            }
        }
        Ok(json!({"armed": true, "instructions_in_gam": count, "ranges_gam": ranges}))
    }

    // ----------------------------------------------------------- archive --

    fn lib_map(&self, p: &Value) -> R<Value> {
        let a = self.archive.as_ref().ok_or("this .gam has no BBKRPG archive")?;
        let gam_off = if let Some(off) = p_num(p, "gam")? {
            off as u32
        } else if let Some(x) = p_num(p, "phys")? {
            (x as u32).checked_sub(GAM_FLASH).ok_or("phys is below the game's flash image")?
        } else if let Some(x) = p_num(p, "addr")? {
            let ph = self.emu()?.cpu.memory().physical(x as u16);
            ph.checked_sub(GAM_FLASH).ok_or_else(|| format!("{x:04x} maps to {ph:06x}, outside the game"))?
        } else if let Some(x) = p_num(p, "lib")? {
            a.base + x as u32
        } else {
            return Err("lib.map needs addr, phys, gam or lib".into());
        };
        let mut out = json!({"gam": format!("{gam_off:x}"), "phys": format!("{:06x}", GAM_FLASH + gam_off)});
        if gam_off < a.base || gam_off >= a.base + a.len {
            out["region"] = json!(if gam_off < 0x46 { "header" } else if gam_off < a.base { "engine" } else { "past archive" });
            return Ok(out);
        }
        let lib_off = gam_off - a.base;
        out["region"] = json!("archive");
        out["lib"] = json!(format!("{lib_off:x}"));
        if let Some(h) = a.locate(lib_off) {
            out["resource"] = json!(format!("{}/{}", Archive::type_name(h.key), Archive::key_str(h.key)));
            out["offset"] = json!(h.res_offset);
            out["res_lib"] = json!(format!("{:x}", h.res_start));
            if h.key[0] == 1 && h.res_offset >= 0x18 {
                // script address: counted from offset 0x18 (bbkrpg/gut.py)
                out["script_addr"] = json!(format!("{:04x}", h.res_offset - 0x18));
            }
        }
        Ok(out)
    }

    fn flash_load_lib(&mut self, p: &Value) -> R<Value> {
        let path = p_str(p, "path").ok_or("missing 'path'")?;
        let lib = std::fs::read(path).map_err(|e| format!("{path}: {e}"))?;
        let base = self.archive.as_ref().ok_or("this .gam has no BBKRPG archive")?.base as usize;
        let mut gam = self.gam[..base].to_vec();
        gam.extend_from_slice(&lib);
        if gam.len() > 0x1E0000 {
            return Err(format!("game would be {} bytes; the loader's limit is {}", gam.len(), 0x1E0000));
        }
        let old_len = self.gam.len();
        let e = self.emu_mut()?;
        let flash = &mut e.cpu.memory_mut().flash;
        let fi = bbkemu_core::memory::flash_index;
        let start = GAM_FLASH - FLASH_BASE;
        for a in start + base as u32..start + old_len.max(gam.len()) as u32 {
            flash[fi(a)] = 0xff;
        }
        for (i, b) in lib.iter().enumerate() {
            flash[fi(start + (base + i) as u32)] = *b;
        }
        // game size in the flash game header (flash address 0x10 + 12)
        let size = gam.len();
        flash[fi(0x10 + 12)] = size as u8;
        flash[fi(0x10 + 13)] = (size >> 8) as u8;
        flash[fi(0x10 + 14)] = (size >> 16) as u8;
        self.archive = Archive::parse(&gam);
        self.gam = gam;
        Ok(json!({"archive_bytes": lib.len(), "gam_bytes": size}))
    }
}

// ------------------------------------------------------------ mem.search --

enum Operand {
    New,
    Old(i64),
    Lit(i64),
}

struct Term {
    lhs: Operand,
    op: String,
    rhs: Operand,
}

impl Term {
    fn eval(&self, new: u8, old: u8) -> bool {
        let v = |o: &Operand| match o {
            Operand::New => new as i64,
            Operand::Old(d) => old as i64 + d,
            Operand::Lit(x) => *x,
        };
        let (a, b) = (v(&self.lhs), v(&self.rhs));
        match self.op.as_str() {
            "==" => a == b,
            "!=" => a != b,
            "<" => a < b,
            "<=" => a <= b,
            ">" => a > b,
            ">=" => a >= b,
            _ => false,
        }
    }
}

fn parse_operand(s: &str) -> R<Operand> {
    let s = s.replace(' ', "");
    if s == "new" {
        return Ok(Operand::New);
    }
    if let Some(rest) = s.strip_prefix("old") {
        if rest.is_empty() {
            return Ok(Operand::Old(0));
        }
        let d: i64 = rest.parse().map_err(|_| format!("bad operand {s:?}"))?;
        return Ok(Operand::Old(d));
    }
    Ok(Operand::Lit(num(&Value::String(s.clone()))? as i64))
}

fn parse_filter(f: &str) -> R<Vec<Term>> {
    f.split("&&")
        .map(|t| {
            for op in ["==", "!=", "<=", ">=", "<", ">"] {
                if let Some(i) = t.find(op) {
                    return Ok(Term {
                        lhs: parse_operand(t[..i].trim())?,
                        op: op.to_string(),
                        rhs: parse_operand(t[i + op.len()..].trim())?,
                    });
                }
            }
            Err(format!("bad filter term {t:?}"))
        })
        .collect()
}

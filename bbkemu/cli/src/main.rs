//! bbkemu: headless BBK A-series emulator driven by JSON lines on stdin.
//!
//! One request per line, one response per line on stdout; logs go to stderr.
//! The envelope and command names follow gbemu-cli (see PROTOCOL.md).

mod archive;
mod disasm;
mod png;
mod session;

use std::io::{self, BufRead, Write};

use serde_json::{json, Value};

fn main() {
    env_logger::Builder::from_env(env_logger::Env::default().default_filter_or("warn"))
        .target(env_logger::Target::Stderr)
        .init();

    let args: Vec<String> = std::env::args().collect();
    let script = match args.iter().position(|a| a == "--script") {
        Some(i) => match args.get(i + 1) {
            Some(p) => Some(p.clone()),
            None => {
                eprintln!("--script needs a path");
                std::process::exit(2);
            }
        },
        None => None,
    };

    let mut s = session::Session::new();
    let stdout = io::stdout();
    let mut out = stdout.lock();

    let lines: Box<dyn Iterator<Item = io::Result<String>>> = match &script {
        Some(p) => match std::fs::File::open(p) {
            Ok(f) => Box::new(io::BufReader::new(f).lines()),
            Err(e) => {
                eprintln!("cannot open {p}: {e}");
                std::process::exit(2);
            }
        },
        None => Box::new(io::stdin().lock().lines()),
    };

    for line in lines {
        let Ok(line) = line else { break };
        let line = line.trim();
        if line.is_empty() || line.starts_with('#') {
            continue;
        }
        let (resp, quit) = match serde_json::from_str::<Value>(line) {
            Ok(req) => {
                let id = req.get("id").cloned().unwrap_or(Value::Null);
                let cmd = req.get("cmd").and_then(Value::as_str).unwrap_or("").to_string();
                let params = req.get("params").cloned().unwrap_or_else(|| json!({}));
                match s.dispatch(&cmd, &params) {
                    Ok(result) => (json!({"id": id, "ok": true, "result": result}), cmd == "quit"),
                    Err(e) => (json!({"id": id, "ok": false, "error": e}), false),
                }
            }
            Err(e) => (json!({"id": null, "ok": false, "error": format!("bad json: {e}")}), false),
        };
        let _ = writeln!(out, "{resp}");
        let _ = out.flush();
        if quit {
            break;
        }
    }
}

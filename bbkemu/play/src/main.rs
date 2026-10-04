//! bbkplay: play a BBK game in a window while recording a route.
//!
//!   bbkplay <game.gam> --roms <dir with 8.BIN and E.BIN> --route <route.jsonl>
//!
//! Every key press and release is appended to the route file as it happens,
//! stamped with the frame it applies before. Restarting with the same route
//! replays it at full speed and carries on recording, so a route can be built
//! over many sessions. `bbkemu`'s input.replay plays a route back identically.
//!
//! Keys: arrows, Enter, Backspace (= EXIT/back), Space, PageUp/PageDown,
//! letters and digits. Hold Tab to fast-forward (4x). F2 adds a numbered
//! marker to the route (to flag a spot, e.g. a bug, for later). F12 saves a
//! screenshot. Esc or closing the window quits.

use std::fs::{self, File, OpenOptions};
use std::io::{BufRead, BufReader, Write};
use std::num::NonZeroU32;
use std::path::PathBuf;
use std::rc::Rc;
use std::time::{Duration, Instant};

use bbkemu_core::input::BbkKey;
use bbkemu_core::route::{self, Action, Event};
use bbkemu_core::{model, Emulator};
use softbuffer::{Context, Surface};
use winit::application::ApplicationHandler;
use winit::dpi::LogicalSize;
use winit::event::{ElementState, WindowEvent};
use winit::event_loop::{ActiveEventLoop, ControlFlow, EventLoop};
use winit::keyboard::{KeyCode, PhysicalKey};
use winit::window::{Window, WindowId};

const USAGE: &str = "usage: bbkplay <game.gam> --roms <dir> --route <route.jsonl> [--model 4988|4980] [--scale N]";

struct Args {
    game: PathBuf,
    roms: PathBuf,
    route: PathBuf,
    model: String,
    scale: u32,
    /// replay the route headless, print frame + screen hash, exit
    verify: bool,
}

fn parse_args() -> Result<Args, String> {
    let mut it = std::env::args().skip(1);
    let (mut game, mut roms, mut route, mut model, mut scale) = (None, None, None, "4988".to_string(), 5);
    let mut verify = false;
    while let Some(a) = it.next() {
        match a.as_str() {
            "--roms" => roms = it.next().map(PathBuf::from),
            "--route" => route = it.next().map(PathBuf::from),
            "--model" => model = it.next().ok_or("--model needs a value")?,
            "--scale" => scale = it.next().and_then(|s| s.parse().ok()).ok_or("--scale needs a number")?,
            "--verify" => verify = true,
            "-h" | "--help" => return Err(USAGE.into()),
            _ if game.is_none() => game = Some(PathBuf::from(a)),
            _ => return Err(format!("unexpected argument {a:?}\n{USAGE}")),
        }
    }
    Ok(Args {
        game: game.ok_or(USAGE)?,
        roms: roms.ok_or(USAGE)?,
        route: route.ok_or(USAGE)?,
        model,
        scale,
        verify,
    })
}

fn map_key(code: KeyCode) -> Option<BbkKey> {
    Some(match code {
        KeyCode::ArrowUp => BbkKey::Up,
        KeyCode::ArrowDown => BbkKey::Down,
        KeyCode::ArrowLeft => BbkKey::Left,
        KeyCode::ArrowRight => BbkKey::Right,
        KeyCode::Enter => BbkKey::Enter,
        KeyCode::Backspace => BbkKey::Exit,
        KeyCode::Delete => BbkKey::Del,
        KeyCode::Space => BbkKey::Space,
        KeyCode::PageUp => BbkKey::PgUp,
        KeyCode::PageDown => BbkKey::PgDn,
        KeyCode::Digit0 => BbkKey::Key0,
        KeyCode::Digit1 => BbkKey::Key1,
        KeyCode::Digit2 => BbkKey::Key2,
        KeyCode::Digit3 => BbkKey::Key3,
        KeyCode::Digit4 => BbkKey::Key4,
        KeyCode::Digit5 => BbkKey::Key5,
        KeyCode::Digit6 => BbkKey::Key6,
        KeyCode::Digit7 => BbkKey::Key7,
        KeyCode::Digit8 => BbkKey::Key8,
        KeyCode::Digit9 => BbkKey::Key9,
        KeyCode::KeyQ => BbkKey::Q,
        KeyCode::KeyW => BbkKey::W,
        KeyCode::KeyE => BbkKey::E,
        KeyCode::KeyR => BbkKey::R,
        KeyCode::KeyT => BbkKey::T,
        KeyCode::KeyY => BbkKey::Y,
        KeyCode::KeyU => BbkKey::U,
        KeyCode::KeyI => BbkKey::I,
        KeyCode::KeyO => BbkKey::O,
        KeyCode::KeyP => BbkKey::P,
        KeyCode::KeyA => BbkKey::A,
        KeyCode::KeyS => BbkKey::S,
        KeyCode::KeyD => BbkKey::D,
        KeyCode::KeyF => BbkKey::F,
        KeyCode::KeyG => BbkKey::G,
        KeyCode::KeyH => BbkKey::H,
        KeyCode::KeyJ => BbkKey::J,
        KeyCode::KeyK => BbkKey::K,
        KeyCode::KeyL => BbkKey::L,
        KeyCode::KeyZ => BbkKey::Z,
        KeyCode::KeyX => BbkKey::X,
        KeyCode::KeyC => BbkKey::C,
        KeyCode::KeyV => BbkKey::V,
        KeyCode::KeyB => BbkKey::B,
        KeyCode::KeyN => BbkKey::N,
        KeyCode::KeyM => BbkKey::M,
        _ => return None,
    })
}

struct App {
    emu: Emulator,
    scale: u32,
    route: File,
    marks: u32,
    fast: bool,
    window: Option<Rc<Window>>,
    context: Option<Context<Rc<Window>>>,
    surface: Option<Surface<Rc<Window>, Rc<Window>>>,
    next_frame: Instant,
    last_title: Instant,
}

impl App {
    fn record(&mut self, action: Action) {
        let e = Event { frame: self.emu.frame_count(), action };
        route::apply(&mut self.emu, &e);
        // written and flushed immediately, so a crash loses nothing
        let _ = writeln!(self.route, "{}", route::to_line(&e));
        let _ = self.route.flush();
    }

    fn draw(&mut self) -> Result<(), String> {
        let window = self.window.as_ref().expect("window");
        let surface = self.surface.as_mut().expect("surface");
        let size = window.inner_size();
        let (w, h) = (size.width.max(1), size.height.max(1));
        surface
            .resize(NonZeroU32::new(w).unwrap(), NonZeroU32::new(h).unwrap())
            .map_err(|e| e.to_string())?;
        let px = self.emu.render_lcd_buffer();
        let mut buf = surface.buffer_mut().map_err(|e| e.to_string())?;
        for y in 0..h as usize {
            for x in 0..w as usize {
                let (sx, sy) = (x * 159 / w as usize, y * 96 / h as usize);
                buf[y * w as usize + x] = if px[sy * 159 + sx] { 0x0014_1814 } else { 0x00a8_b8a0 };
            }
        }
        buf.present().map_err(|e| e.to_string())
    }

    fn update_title(&mut self) {
        if let Some(w) = &self.window {
            let secs = self.emu.frame_count() / 60;
            w.set_title(&format!(
                "bbkplay  {}:{:02}:{:02}  frame {}{}  (recording)",
                secs / 3600, secs / 60 % 60, secs % 60, self.emu.frame_count(),
                if self.fast { "  FAST" } else { "" }
            ));
        }
    }
}

impl ApplicationHandler for App {
    fn resumed(&mut self, el: &ActiveEventLoop) {
        if self.window.is_some() {
            return;
        }
        let attrs = Window::default_attributes()
            .with_title("bbkplay")
            .with_inner_size(LogicalSize::new((159 * self.scale) as f64, (96 * self.scale) as f64))
            .with_min_inner_size(LogicalSize::new(159.0, 96.0));
        let window = match el.create_window(attrs) {
            Ok(w) => Rc::new(w),
            Err(e) => {
                eprintln!("cannot create window: {e}");
                el.exit();
                return;
            }
        };
        let context = Context::new(window.clone()).expect("display context");
        let surface = Surface::new(&context, window.clone()).expect("display surface");
        self.window = Some(window);
        self.context = Some(context);
        self.surface = Some(surface);
        self.next_frame = Instant::now();
        self.update_title();
    }

    fn window_event(&mut self, el: &ActiveEventLoop, _id: WindowId, event: WindowEvent) {
        match event {
            WindowEvent::CloseRequested => {
                self.record(Action::End);
                el.exit();
            }
            WindowEvent::RedrawRequested => {
                if let Err(e) = self.draw() {
                    eprintln!("render failed: {e}");
                    el.exit();
                }
            }
            WindowEvent::KeyboardInput { event, .. } => {
                let PhysicalKey::Code(code) = event.physical_key else { return };
                let pressed = event.state == ElementState::Pressed;
                match code {
                    KeyCode::Escape if pressed => {
                        self.record(Action::End);
                        el.exit();
                    }
                    KeyCode::Tab => {
                        self.fast = pressed;
                        self.update_title();
                    }
                    KeyCode::F2 if pressed && !event.repeat => {
                        self.marks += 1;
                        let n = self.marks;
                        self.record(Action::Mark(format!("mark {n}")));
                        println!("marker {n} at frame {}", self.emu.frame_count());
                    }
                    KeyCode::F12 if pressed && !event.repeat => {
                        let path = format!("bbkplay-{}.pgm", self.emu.frame_count());
                        let px = self.emu.render_lcd_buffer();
                        let mut out = format!("P5 159 96 255\n").into_bytes();
                        out.extend(px.iter().map(|&p| if p { 0x10 } else { 0xd8 }));
                        match fs::write(&path, out) {
                            Ok(()) => println!("screenshot {path}"),
                            Err(e) => eprintln!("screenshot failed: {e}"),
                        }
                    }
                    _ => {
                        if let Some(k) = map_key(code) {
                            // same calls as BBKEmu's frontend, OS key repeats included
                            self.record(if pressed { Action::Down(k) } else { Action::Up });
                        }
                    }
                }
            }
            _ => {}
        }
    }

    fn about_to_wait(&mut self, el: &ActiveEventLoop) {
        let now = Instant::now();
        if now >= self.next_frame {
            for _ in 0..if self.fast { 4 } else { 1 } {
                self.emu.run_frame();
            }
            if let Some(w) = &self.window {
                w.request_redraw();
            }
            self.next_frame = now + Duration::from_micros(16_667);
            if now.duration_since(self.last_title) > Duration::from_secs(1) {
                self.last_title = now;
                self.update_title();
            }
        }
        if !self.emu.is_running() {
            println!("the game exited (frame {})", self.emu.frame_count());
            self.record(Action::End);
            el.exit();
            return;
        }
        el.set_control_flow(ControlFlow::WaitUntil(self.next_frame));
    }
}

fn main() {
    let args = match parse_args() {
        Ok(a) => a,
        Err(e) => {
            eprintln!("{e}");
            std::process::exit(2);
        }
    };
    let fail = |msg: String| -> ! {
        eprintln!("{msg}");
        std::process::exit(1);
    };
    let read = |p: PathBuf| fs::read(&p).unwrap_or_else(|e| fail(format!("{}: {e}", p.display())));
    let m = match args.model.as_str() {
        "4980" => &model::MODEL_4980,
        "4988" => &model::MODEL_4988,
        other => fail(format!("unknown model {other}")),
    };
    let gam = read(args.game.clone());

    // Boot exactly as bbkemu's load_gam does.
    let mut emu = Emulator::new(m);
    emu.load_rom_8(&read(args.roms.join("8.BIN")));
    emu.load_rom_e(&read(args.roms.join("E.BIN")));
    if let Err(e) = emu.load_gam(&gam) {
        fail(format!("cannot load game: {e}"));
    }

    // Resume: replay the existing route, then keep appending to it.
    let mut marks = 0;
    if args.route.exists() {
        let f = File::open(&args.route).unwrap_or_else(|e| fail(format!("{}: {e}", args.route.display())));
        let mut events = Vec::new();
        for (n, line) in BufReader::new(f).lines().enumerate() {
            let line = line.unwrap_or_default();
            if let Some((hash, _)) = route::parse_header(&line) {
                if hash != route::gam_hash(&gam) {
                    fail(format!("{} was recorded on a different .gam", args.route.display()));
                }
                continue;
            }
            match route::parse_line(&line) {
                Ok(Some(e)) => events.push(e),
                Ok(None) => {}
                Err(e) => fail(format!("{}:{}: {e}", args.route.display(), n + 1)),
            }
        }
        marks = events.iter().filter(|e| matches!(e.action, Action::Mark(_))).count() as u32;
        let last = events.iter().map(|e| e.frame).max().unwrap_or(0);
        println!("resuming: replaying {} events up to frame {last} ...", events.len());
        let t0 = Instant::now();
        let mut i = 0;
        while emu.frame_count() < last {
            while i < events.len() && events[i].frame <= emu.frame_count() {
                route::apply(&mut emu, &events[i]);
                i += 1;
            }
            emu.run_frame();
            if emu.frame_count() % 36_000 == 0 {
                println!("  {} min of play replayed", emu.frame_count() / 3600);
            }
        }
        while i < events.len() {
            route::apply(&mut emu, &events[i]);
            i += 1;
        }
        println!("resumed at frame {} in {:.1}s", emu.frame_count(), t0.elapsed().as_secs_f32());
    } else if args.verify {
        fail(format!("{} does not exist", args.route.display()));
    } else {
        fs::write(&args.route, route::header(&gam, emu.model().name) + "\n")
            .unwrap_or_else(|e| fail(format!("{}: {e}", args.route.display())));
        println!("new route {}", args.route.display());
    }
    if args.verify {
        let px = emu.render_lcd_buffer();
        let mut h: u64 = 0xcbf29ce484222325;
        for &b in px.iter() {
            h = (h ^ b as u64).wrapping_mul(0x100000001b3);
        }
        println!("verify frame={} hash={h:016x}", emu.frame_count());
        return;
    }
    let file = OpenOptions::new().append(true).open(&args.route)
        .unwrap_or_else(|e| fail(format!("{}: {e}", args.route.display())));

    println!("keys: arrows, Enter, Backspace = back/exit, Space; hold Tab = fast-forward;");
    println!("      F2 = drop a numbered marker (note what happened, e.g. a bug); F12 = screenshot; Esc = quit");

    let el = EventLoop::new().unwrap_or_else(|e| fail(format!("event loop: {e}")));
    let mut app = App {
        emu,
        scale: args.scale,
        route: file,
        marks,
        fast: false,
        window: None,
        context: None,
        surface: None,
        next_frame: Instant::now(),
        last_title: Instant::now(),
    };
    if let Err(e) = el.run_app(&mut app) {
        fail(format!("{e}"));
    }
    println!("route saved: {} (frame {})", args.route.display(), app.emu.frame_count());
}

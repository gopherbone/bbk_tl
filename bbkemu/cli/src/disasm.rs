//! NMOS 6502 disassembler (official opcodes; anything else prints as `.db`).

#[derive(Clone, Copy, PartialEq, Eq)]
pub enum Mode {
    Imp,
    Acc,
    Imm,
    Zp,
    Zpx,
    Zpy,
    Abs,
    Abx,
    Aby,
    Ind,
    Izx,
    Izy,
    Rel,
}

impl Mode {
    pub fn len(self) -> u16 {
        match self {
            Mode::Imp | Mode::Acc => 1,
            Mode::Abs | Mode::Abx | Mode::Aby | Mode::Ind => 3,
            _ => 2,
        }
    }
}

pub fn decode(op: u8) -> Option<(&'static str, Mode)> {
    use Mode::*;
    let r = match op {
        0x00 => ("brk", Imp), 0x01 => ("ora", Izx), 0x05 => ("ora", Zp), 0x06 => ("asl", Zp),
        0x08 => ("php", Imp), 0x09 => ("ora", Imm), 0x0a => ("asl", Acc), 0x0d => ("ora", Abs),
        0x0e => ("asl", Abs), 0x10 => ("bpl", Rel), 0x11 => ("ora", Izy), 0x15 => ("ora", Zpx),
        0x16 => ("asl", Zpx), 0x18 => ("clc", Imp), 0x19 => ("ora", Aby), 0x1d => ("ora", Abx),
        0x1e => ("asl", Abx), 0x20 => ("jsr", Abs), 0x21 => ("and", Izx), 0x24 => ("bit", Zp),
        0x25 => ("and", Zp), 0x26 => ("rol", Zp), 0x28 => ("plp", Imp), 0x29 => ("and", Imm),
        0x2a => ("rol", Acc), 0x2c => ("bit", Abs), 0x2d => ("and", Abs), 0x2e => ("rol", Abs),
        0x30 => ("bmi", Rel), 0x31 => ("and", Izy), 0x35 => ("and", Zpx), 0x36 => ("rol", Zpx),
        0x38 => ("sec", Imp), 0x39 => ("and", Aby), 0x3d => ("and", Abx), 0x3e => ("rol", Abx),
        0x40 => ("rti", Imp), 0x41 => ("eor", Izx), 0x45 => ("eor", Zp), 0x46 => ("lsr", Zp),
        0x48 => ("pha", Imp), 0x49 => ("eor", Imm), 0x4a => ("lsr", Acc), 0x4c => ("jmp", Abs),
        0x4d => ("eor", Abs), 0x4e => ("lsr", Abs), 0x50 => ("bvc", Rel), 0x51 => ("eor", Izy),
        0x55 => ("eor", Zpx), 0x56 => ("lsr", Zpx), 0x58 => ("cli", Imp), 0x59 => ("eor", Aby),
        0x5d => ("eor", Abx), 0x5e => ("lsr", Abx), 0x60 => ("rts", Imp), 0x61 => ("adc", Izx),
        0x65 => ("adc", Zp), 0x66 => ("ror", Zp), 0x68 => ("pla", Imp), 0x69 => ("adc", Imm),
        0x6a => ("ror", Acc), 0x6c => ("jmp", Ind), 0x6d => ("adc", Abs), 0x6e => ("ror", Abs),
        0x70 => ("bvs", Rel), 0x71 => ("adc", Izy), 0x75 => ("adc", Zpx), 0x76 => ("ror", Zpx),
        0x78 => ("sei", Imp), 0x79 => ("adc", Aby), 0x7d => ("adc", Abx), 0x7e => ("ror", Abx),
        0x81 => ("sta", Izx), 0x84 => ("sty", Zp), 0x85 => ("sta", Zp), 0x86 => ("stx", Zp),
        0x88 => ("dey", Imp), 0x8a => ("txa", Imp), 0x8c => ("sty", Abs), 0x8d => ("sta", Abs),
        0x8e => ("stx", Abs), 0x90 => ("bcc", Rel), 0x91 => ("sta", Izy), 0x94 => ("sty", Zpx),
        0x95 => ("sta", Zpx), 0x96 => ("stx", Zpy), 0x98 => ("tya", Imp), 0x99 => ("sta", Aby),
        0x9a => ("txs", Imp), 0x9d => ("sta", Abx), 0xa0 => ("ldy", Imm), 0xa1 => ("lda", Izx),
        0xa2 => ("ldx", Imm), 0xa4 => ("ldy", Zp), 0xa5 => ("lda", Zp), 0xa6 => ("ldx", Zp),
        0xa8 => ("tay", Imp), 0xa9 => ("lda", Imm), 0xaa => ("tax", Imp), 0xac => ("ldy", Abs),
        0xad => ("lda", Abs), 0xae => ("ldx", Abs), 0xb0 => ("bcs", Rel), 0xb1 => ("lda", Izy),
        0xb4 => ("ldy", Zpx), 0xb5 => ("lda", Zpx), 0xb6 => ("ldx", Zpy), 0xb8 => ("clv", Imp),
        0xb9 => ("lda", Aby), 0xba => ("tsx", Imp), 0xbc => ("ldy", Abx), 0xbd => ("lda", Abx),
        0xbe => ("ldx", Aby), 0xc0 => ("cpy", Imm), 0xc1 => ("cmp", Izx), 0xc4 => ("cpy", Zp),
        0xc5 => ("cmp", Zp), 0xc6 => ("dec", Zp), 0xc8 => ("iny", Imp), 0xc9 => ("cmp", Imm),
        0xca => ("dex", Imp), 0xcc => ("cpy", Abs), 0xcd => ("cmp", Abs), 0xce => ("dec", Abs),
        0xd0 => ("bne", Rel), 0xd1 => ("cmp", Izy), 0xd5 => ("cmp", Zpx), 0xd6 => ("dec", Zpx),
        0xd8 => ("cld", Imp), 0xd9 => ("cmp", Aby), 0xdd => ("cmp", Abx), 0xde => ("dec", Abx),
        0xe0 => ("cpx", Imm), 0xe1 => ("sbc", Izx), 0xe4 => ("cpx", Zp), 0xe5 => ("sbc", Zp),
        0xe6 => ("inc", Zp), 0xe8 => ("inx", Imp), 0xe9 => ("sbc", Imm), 0xea => ("nop", Imp),
        0xec => ("cpx", Abs), 0xed => ("sbc", Abs), 0xee => ("inc", Abs), 0xf0 => ("beq", Rel),
        0xf1 => ("sbc", Izy), 0xf5 => ("sbc", Zpx), 0xf6 => ("inc", Zpx), 0xf8 => ("sed", Imp),
        0xf9 => ("sbc", Aby), 0xfd => ("sbc", Abx), 0xfe => ("inc", Abx),
        _ => return None,
    };
    Some(r)
}

/// Length in bytes of the instruction starting with `op` (1 for unknown).
pub fn length(op: u8) -> u16 {
    decode(op).map_or(1, |(_, m)| m.len())
}

/// Format one instruction at `pc`, reading bytes through `rd`.
pub fn format(pc: u16, rd: &dyn Fn(u16) -> u8) -> (String, u16) {
    let op = rd(pc);
    let Some((name, mode)) = decode(op) else {
        return (format!(".db ${op:02x}"), 1);
    };
    let b1 = rd(pc.wrapping_add(1));
    let w = b1 as u16 | (rd(pc.wrapping_add(2)) as u16) << 8;
    let text = match mode {
        Mode::Imp => name.to_string(),
        Mode::Acc => format!("{name} a"),
        Mode::Imm => format!("{name} #${b1:02x}"),
        Mode::Zp => format!("{name} ${b1:02x}"),
        Mode::Zpx => format!("{name} ${b1:02x},x"),
        Mode::Zpy => format!("{name} ${b1:02x},y"),
        Mode::Abs => format!("{name} ${w:04x}"),
        Mode::Abx => format!("{name} ${w:04x},x"),
        Mode::Aby => format!("{name} ${w:04x},y"),
        Mode::Ind => format!("{name} (${w:04x})"),
        Mode::Izx => format!("{name} (${b1:02x},x)"),
        Mode::Izy => format!("{name} (${b1:02x}),y"),
        Mode::Rel => {
            let t = pc.wrapping_add(2).wrapping_add(b1 as i8 as i16 as u16);
            format!("{name} ${t:04x}")
        }
    };
    (text, mode.len())
}

//! Map flash/.gam offsets onto BBKRPG archive resources (bbkrpg/lib.py layout).

const BANK: u32 = 0x4000;
const RES_TYPES: [&str; 13] = [
    "?", "GUT", "MAP", "ARS", "MRS", "SRS", "GRS", "TIL", "ACP", "GDP", "GGJ", "PIC", "MLR",
];

#[derive(Clone)]
pub struct Archive {
    /// .gam file offset of the archive
    pub base: u32,
    pub len: u32,
    /// (archive offset, key) sorted by offset
    entries: Vec<(u32, [u8; 3])>,
    /// end offset of each bank's resources, by bank number
    bank_end: Vec<u32>,
}

pub struct Hit {
    pub key: [u8; 3],
    pub res_offset: u32,
    pub res_start: u32,
}

impl Archive {
    pub fn parse(gam: &[u8]) -> Option<Archive> {
        if gam.len() < 0x46 || &gam[..3] != b"GAM" {
            return None;
        }
        let base = u32::from_le_bytes(gam[0x42..0x46].try_into().ok()?);
        let a = gam.get(base as usize..)?;
        if a.len() < 0x4000 || &a[..3] != b"LIB" {
            return None;
        }
        let n = (a[0x0c] as usize | (a[0x0d] as usize) << 8) / 3;
        let mut entries = Vec::with_capacity(n);
        for e in 0..n {
            let k = [a[0x10 + 3 * e], a[0x11 + 3 * e], a[0x12 + 3 * e]];
            let p = &a[0x2000 + 3 * e..0x2003 + 3 * e];
            entries.push((p[0] as u32 * BANK + (p[1] as u32 | (p[2] as u32) << 8), k));
        }
        entries.sort();
        let nb = a.len() as u32 / BANK;
        let bank_end = (0..nb)
            .map(|b| {
                let h = (b * BANK) as usize;
                b * BANK + (a[h + 12] as u32 | (a[h + 13] as u32) << 8)
            })
            .collect();
        Some(Archive { base, len: a.len() as u32, entries, bank_end })
    }

    /// Resource containing archive offset `off`, if any.
    pub fn locate(&self, off: u32) -> Option<Hit> {
        let i = self.entries.partition_point(|(o, _)| *o <= off);
        if i == 0 {
            return None;
        }
        let (start, key) = self.entries[i - 1];
        let bank = (start / BANK) as usize;
        let mut end = self.bank_end.get(bank).copied().unwrap_or(start);
        if let Some((next, _)) = self.entries.get(i) {
            if next / BANK == start / BANK {
                end = end.min(*next);
            }
        }
        (off < end).then_some(Hit { key, res_offset: off - start, res_start: start })
    }

    pub fn key_str(k: [u8; 3]) -> String {
        format!("{}-{}-{}", k[0], k[1], k[2])
    }

    pub fn type_name(k: [u8; 3]) -> &'static str {
        RES_TYPES.get(k[0] as usize).copied().unwrap_or("?")
    }
}

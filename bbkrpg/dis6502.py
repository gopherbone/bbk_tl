"""Static 6502 disassembly of .gam engine segments (inverse of asm6502's table)."""

from .asm6502 import _LEN, _T

OPS = {op: (mn, mode) for mn, modes in _T.items() for mode, op in modes.items()}


def disasm(data: bytes, start: int, cpu: int, n: int = 40) -> list[str]:
    """Disassemble `n` instructions of `data` from `start`, shown at CPU address `cpu`."""
    out, i = [], start
    for _ in range(n):
        op = data[i]
        if op not in OPS:
            out.append(f"{cpu:04x}  {op:02x}        .db ${op:02x}")
            i, cpu = i + 1, cpu + 1
            continue
        mn, mode = OPS[op]
        ln = _LEN[mode]
        b = data[i:i + ln]
        v = b[1] if ln == 2 else (b[1] | b[2] << 8 if ln == 3 else None)
        arg = {"imp": "", "acc": "a", "imm": f"#${v:02x}" if v is not None else "", "zp": f"${v:02x}" if v is not None else "",
               "zpx": f"${v:02x},x" if v is not None else "", "zpy": f"${v:02x},y" if v is not None else "",
               "izx": f"(${v:02x},x)" if v is not None else "", "izy": f"(${v:02x}),y" if v is not None else "",
               "abs": f"${v:04x}" if v is not None else "", "abx": f"${v:04x},x" if v is not None else "",
               "aby": f"${v:04x},y" if v is not None else "", "ind": f"(${v:04x})" if v is not None else "",
               "rel": f"${(cpu + 2 + (v - 256 if v and v > 127 else v or 0)) & 0xffff:04x}"}[mode]
        out.append(f"{cpu:04x}  {b.hex():8}  {mn} {arg}".rstrip())
        i, cpu = i + ln, cpu + ln
    return out


def seg_disasm(gam: bytes, gam_off: int, n: int = 40) -> list[str]:
    seg = gam_off // 0x4000
    return disasm(gam, gam_off, 0x5000 + gam_off - seg * 0x4000, n)

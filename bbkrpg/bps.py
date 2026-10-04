"""BPS patches (byuu's format, as used by Floating IPS, beat, RetroArch).

create(): SourceCopy for any 16+ byte run found in the source (hash index of
16-byte blocks), TargetCopy is not used, the rest is TargetRead. apply()
checks all three CRC32s.
"""

from __future__ import annotations

import zlib

BLOCK = 16


def _num(n: int) -> bytes:
    out = bytearray()
    while True:
        x = n & 0x7F
        n >>= 7
        if n == 0:
            out.append(0x80 | x)
            return bytes(out)
        out.append(x)
        n -= 1


def _read_num(b: bytes, i: int) -> tuple[int, int]:
    data, shift = 0, 1
    while True:
        x = b[i]
        i += 1
        data += (x & 0x7F) * shift
        if x & 0x80:
            return data, i
        shift <<= 7
        data += shift


def create(source: bytes, target: bytes, metadata: bytes = b"") -> bytes:
    index: dict[bytes, int] = {}
    for i in range(0, len(source) - BLOCK + 1, BLOCK):
        index.setdefault(source[i:i + BLOCK], i)
    out = bytearray(b"BPS1") + _num(len(source)) + _num(len(target)) + _num(len(metadata)) + metadata
    src_rel = 0
    pending = bytearray()

    def flush():
        if pending:
            out.extend(_num(((len(pending) - 1) << 2) | 1))   # TargetRead
            out.extend(pending)
            pending.clear()

    t = 0
    while t < len(target):
        best_len, best_at = 0, 0
        # same offset first (unchanged regions), then any indexed block
        cands = []
        if t < len(source):
            cands.append(t)
        blk = target[t:t + BLOCK]
        if len(blk) == BLOCK and blk in index:
            cands.append(index[blk])
        for s in cands:
            n = 0
            while t + n < len(target) and s + n < len(source) and target[t + n] == source[s + n]:
                n += 1
            if n > best_len:
                best_len, best_at = n, s
        if best_len >= BLOCK:
            flush()
            out.extend(_num(((best_len - 1) << 2) | 2))       # SourceCopy
            delta = best_at - src_rel
            out.extend(_num((abs(delta) << 1) | (1 if delta < 0 else 0)))
            src_rel = best_at + best_len
            t += best_len
        else:
            pending.append(target[t])
            t += 1
    flush()
    out += zlib.crc32(source).to_bytes(4, "little") + zlib.crc32(target).to_bytes(4, "little")
    out += zlib.crc32(bytes(out)).to_bytes(4, "little")
    return bytes(out)


def apply(patch: bytes, source: bytes) -> bytes:
    if patch[:4] != b"BPS1":
        raise ValueError("not a BPS patch")
    if zlib.crc32(patch[:-4]) != int.from_bytes(patch[-4:], "little"):
        raise ValueError("patch checksum mismatch")
    if zlib.crc32(source) != int.from_bytes(patch[-12:-8], "little"):
        raise ValueError("source checksum mismatch: this patch is for a different file")
    i = 4
    slen, i = _read_num(patch, i)
    tlen, i = _read_num(patch, i)
    mlen, i = _read_num(patch, i)
    i += mlen
    out = bytearray()
    src_rel = tgt_rel = 0
    end = len(patch) - 12
    while i < end:
        d, i = _read_num(patch, i)
        cmd, n = d & 3, (d >> 2) + 1
        if cmd == 0:
            out += source[len(out):len(out) + n]
        elif cmd == 1:
            out += patch[i:i + n]
            i += n
        else:
            o, i = _read_num(patch, i)
            o = -(o >> 1) if o & 1 else o >> 1
            if cmd == 2:
                src_rel += o
                out += source[src_rel:src_rel + n]
                src_rel += n
            else:
                tgt_rel += o
                for _ in range(n):
                    out.append(out[tgt_rel])
                    tgt_rel += 1
    if len(out) != tlen or zlib.crc32(bytes(out)) != int.from_bytes(patch[-8:-4], "little"):
        raise ValueError("target checksum mismatch")
    return bytes(out)

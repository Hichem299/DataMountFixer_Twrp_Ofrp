#!/usr/bin/env python3
"""
Chunked, memory-safe in-place patch of BOTH fstab userdata line
variants inside a large image (e.g. super), avoiding full-file mmap
(some Android/Termux builds cap mmap length).

Usage:
    python3 patch_super_chunked.py super
Patches IN PLACE on the file you pass in (make a copy first if you
want to keep the untouched original as a separate file).
"""
import sys
import os

if len(sys.argv) != 2:
    print("Usage: python3 patch_super_chunked.py <image>")
    sys.exit(1)

path = sys.argv[1]

def build_pair(old, wanted):
    pad_len = len(old) - len(wanted)
    if pad_len < 0:
        raise ValueError(f"replacement longer than original: {old[:40]}...")
    if pad_len > 0:
        filler = b"," + b"x" * (pad_len - 1) if pad_len >= 1 else b""
        new = wanted + filler
    else:
        new = wanted
    assert len(new) == len(old)
    return old, new

oldA = (
    b",inlinecrypt"
    b"\tlatemount,wait,check,quota,reservedsize=128M,"
    b"fileencryption=aes-256-xts:aes-256-cts:v2,"
    b"checkpoint=fs,fscompress,"
    b"keydirectory=/metadata/vold/metadata_encryption"
)
wantedA = b"\tlatemount,wait,check,quota,reservedsize=128M,checkpoint=fs,fscompress"

oldB = (
    b",inlinecrypt"
    b"\tlatemount,wait,check,quota,reservedsize=128M,,"
    b"fileencryption=aes-256-xts:aes-256-cts:v2:aes-256-cts:v2,"
    b"keydirectory=/metadata/vold/metadata_encryption,"
    b"checkpoint=fs,fscompress"
)
wantedB = b"\tlatemount,wait,check,quota,reservedsize=128M,checkpoint=fs,fscompress"

pairs = [build_pair(oldA, wantedA), build_pair(oldB, wantedB)]
max_pat_len = max(len(o) for o, n in pairs)

CHUNK = 64 * 1024 * 1024  # 64MB read window
OVERLAP = max_pat_len - 1

size = os.path.getsize(path)
print(f"File size: {size} bytes")

total_patched = 0
with open(path, "r+b") as f:
    pos = 0
    carry = b""
    while pos < size:
        f.seek(pos)
        chunk = f.read(CHUNK)
        if not chunk:
            break
        window = carry + chunk
        window_start = pos - len(carry)

        for old, new in pairs:
            search_from = 0
            while True:
                idx = window.find(old, search_from)
                if idx == -1:
                    break
                abs_pos = window_start + idx
                f.seek(abs_pos)
                f.write(new)
                total_patched += 1
                print(f"  patched at offset {abs_pos}")
                search_from = idx + len(old)

        pos += len(chunk)
        carry = window[-OVERLAP:] if len(window) >= OVERLAP else window

print(f"DONE. Total occurrences patched: {total_patched}")
if total_patched == 0:
    print("WARNING: nothing matched — no changes made.")

#!/usr/bin/env python3
import os
import sys
from pwnlib.util.packing import p32

if __name__ == "__main__":
    if len(sys.argv) < 4:
        print(f"USAGE: {sys.argv[0]} bin_path code_start code_len mem_start")

    bin_file = open(sys.argv[1], "rb").read()
    code_start = eval(sys.argv[2])
    code_len = eval(sys.argv[3])
    mem_start = eval(sys.argv[4])

    prog = open("prog", "wb")
    prog.write(b"yan85\x00\x00\x00")
    prog.write(p32(code_len))
    prog.write(bin_file[code_start:code_start+code_len])
    prog.write(bin_file[mem_start:mem_start+0x100])
    print(f"done.")

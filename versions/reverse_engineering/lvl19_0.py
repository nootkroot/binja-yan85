# CHANGE THESE - current level 19.0

# (op, arg1, arg2)
instr_format = (0, 1, 2)

reg_vals = {
    0: "none",
    0x10: "a",
    0x20: "b",
    0x02: "c",
    0x08: "d",
    0x04: "s",
    0x40: "i",
    0x01: "f",
}

opcodes = {
    0x40: "imm",
    0x01: "add",
    0x10: "stk",
    0x08: "stm",
    0x02: "ldm",
    0x20: "cmp",
    0x04: "jmp",
    0x80: "sys",
}

syscalls = {
    0x20: "open",
    0x04: "read_code",
    0x08: "read_memory",
    0x10: "write",
    0x01: "sleep",
    0x02: "exit",
}

flags = {
    0x10: "L",
    0x08: "G",
    0x02: "E",
    0x01: "N",
    0x04: "Z",
    0x00: "*",
}

# 0 is value, 1 is reg
instr_sigs = {
    "imm": (1, 0),
    "add": (1, 1),
    "stk": (1, 1),
    "stm": (1, 1),
    "ldm": (1, 1),
    "cmp": (1, 1),
    "jmp": (0, 1),
    "sys": (0, 1),
}

reg_locations = {
    "a": 0x400,
    "b": 0x401,
    "c": 0x402,
    "d": 0x403,
    "s": 0x404,
    "i": 0x405,
    "f": 0x406,
}

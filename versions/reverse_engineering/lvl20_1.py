# CHANGE THESE - current level 21.0

# (op, arg1, arg2)
instr_format = (1, 2, 0)

reg_vals = {
    0x00: "none",
    0x08: "a",
    0x10: "b",
    0x01: "c",
    0x40: "d",
    0x20: "s",
    0x04: "i",
    0x02: "f",
}

opcodes = {
    0x80: "imm",
    0x10: "add",
    0x20: "stk",
    0x01: "stm",
    0x08: "ldm",
    0x02: "cmp",
    0x40: "jmp",
    0x04: "sys",
}

syscalls = {
    0x08: "open",
    0x01: "read_code",
    0x02: "read_memory",
    0x10: "write",
    0x20: "sleep",
    0x04: "exit",
}

flags = {
    0x08: "L",
    0x04: "G",
    0x10: "E",
    0x02: "N",
    0x01: "Z",
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

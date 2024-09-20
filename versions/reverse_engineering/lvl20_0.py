# CHANGE THESE - current level 20.0

# (op, arg1, arg2)
instr_format = (1, 2, 0)

reg_vals = {
    0x00: "none",
    0x08: "a",
    0x10: "b",
    0x40: "c",
    0x02: "d",
    0x04: "s",
    0x01: "i",
    0x20: "f",
}

opcodes = {
    0x10: "imm",
    0x08: "add",
    0x40: "stk",
    0x04: "stm",
    0x01: "ldm",
    0x20: "cmp",
    0x80: "jmp",
    0x02: "sys",
}

syscalls = {
    0x20: "open",
    0x04: "read_code",
    0x10: "read_memory",
    0x08: "write",
    0x01: "sleep",
    0x02: "exit",
}

flags = {
    0x02: "L",
    0x08: "G",
    0x04: "E",
    0x01: "N",
    0x10: "Z",
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

from binaryninja import (Architecture, Endianness, FlagRole, InstructionInfo,
                         IntrinsicInfo, RegisterInfo, Type)

from .disassembler import Yan85Disassembler
from .lifter import Yan85Lifter


class Yan85Arch(Architecture):
    name = "yan85"

    endianness = Endianness.BigEndian
    default_int_size = 1
    max_instr_size = 3
    instr_alignment = 1

    stack_pointer = "s"

    regs = {}
    regs["a"] = RegisterInfo("a", 1)
    regs["b"] = RegisterInfo("b", 1)
    regs["c"] = RegisterInfo("c", 1)
    regs["d"] = RegisterInfo("d", 1)
    regs["s"] = RegisterInfo("s", 1)
    regs["i"] = RegisterInfo("i", 1)
    regs["f"] = RegisterInfo("f", 1)

    flags = ["L", "G", "E", "N", "Z"]
    flag_roles = {
        "L": FlagRole.SpecialFlagRole,
        "G": FlagRole.SpecialFlagRole,
        "E": FlagRole.SpecialFlagRole,
        "N": FlagRole.SpecialFlagRole,
        "Z": FlagRole.SpecialFlagRole,
    }
    flag_write_types = ["none", "*"]
    flags_written_by_flag_write_type = {
        "none": [], "*": ["L", "G", "E", "N", "Z"]}

    intrinsics = {
        "open": IntrinsicInfo(
            [Type.pointer_of_width(2, Type.char()), Type.int(1), Type.int(1)],
            [Type.int(1)],
        ),
        "read_code": IntrinsicInfo(
            [Type.int(1), Type.pointer_of_width(2, Type.char()), Type.int(2)],
            [Type.int(1)],
        ),
        "read_memory": IntrinsicInfo(
            [Type.int(1), Type.pointer_of_width(2, Type.char()), Type.int(1)],
            [Type.int(1)],
        ),
        "write": IntrinsicInfo(
            [Type.int(1), Type.pointer_of_width(2, Type.char()), Type.int(1)],
            [Type.int(1)],
        ),
        "sleep": IntrinsicInfo([Type.int(1)], [Type.int(1)]),
        "exit": IntrinsicInfo([Type.int(1)], []),
    }

    def __init__(self):
        super().__init__()
        self.disassembler = Yan85Disassembler()
        self.lifter = Yan85Lifter()

    def get_instruction_info(self, data, addr):
        _, branch_conds = self.disassembler.disas(data, addr)
        instr_info = InstructionInfo(3)
        for branch_info in branch_conds:
            if branch_info.target is not None:
                instr_info.add_branch(branch_info.type, branch_info.target)
            else:
                instr_info.add_branch(branch_info.type)
        return instr_info

    def get_instruction_text(self, data, addr):
        tokens, _ = self.disassembler.disas(data, addr)
        return tokens, 3

    def get_instruction_low_level_il(self, data, addr, il):
        self.lifter.lift_instr(data, addr, il)
        return 3

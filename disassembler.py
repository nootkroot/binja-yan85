from binaryninja import (BranchType, InstructionTextToken,
                         InstructionTextTokenType)

from .versions.active import *


class BranchInfo:
    def __init__(self, _type, target=None):
        self.type = _type
        self.target = target


class Instruction:
    def __init__(self, data):
        self.op = data[instr_format[0]]
        self.arg1 = data[instr_format[1]]
        self.arg2 = data[instr_format[2]]
        sig = instr_sigs[opcodes[self.op]]
        if sig[0]:
            self.arg1 = reg_vals[self.arg1]
        if sig[1]:
            self.arg2 = reg_vals[self.arg2]


class Yan85Disassembler:
    def __init__(self):
        self.instructions = {
            "imm": self.reg_imm1,
            "add": self.two_reg,
            "stk": self.two_reg,
            "stm": self.two_reg,
            "ldm": self.two_reg,
            "cmp": self.two_reg,
            "jmp": self.jmp,
            "sys": self.reg_imm2,
        }

    def disas(self, data, addr):
        # print(f"[{hex(addr)}]:")
        instr = Instruction(data)
        mnem = opcodes[instr.op]
        func = self.instructions[mnem]
        return func(mnem, instr, addr)

    def reg_imm1(self, mnem, instr, addr):
        tokens = [
            InstructionTextToken(
                InstructionTextTokenType.InstructionToken, mnem + " ")
        ]
        tokens.append(
            InstructionTextToken(
                InstructionTextTokenType.RegisterToken, instr.arg1)
        )
        tokens.append(
            InstructionTextToken(
                InstructionTextTokenType.OperandSeparatorToken, ", ")
        )
        tokens.append(
            InstructionTextToken(
                InstructionTextTokenType.IntegerToken, hex(
                    instr.arg2), instr.arg2
            )
        )

        if mnem == "imm" and instr.arg1 == "i":
            branch = BranchInfo(BranchType.UnconditionalBranch, instr.arg2 * 3)
            return tokens, [branch]

        return tokens, []

    def reg_imm2(self, mnem, instr, addr):
        tokens = [
            InstructionTextToken(
                InstructionTextTokenType.InstructionToken, mnem + " ")
        ]
        tokens.append(
            InstructionTextToken(
                InstructionTextTokenType.IntegerToken, hex(
                    instr.arg1), instr.arg1
            )
        )
        tokens.append(
            InstructionTextToken(
                InstructionTextTokenType.OperandSeparatorToken, ", ")
        )
        tokens.append(
            InstructionTextToken(
                InstructionTextTokenType.RegisterToken, instr.arg2)
        )

        if mnem == "sys":
            branch = BranchInfo(BranchType.SystemCall, None)
            return tokens, [branch]
        return tokens, []

    def two_reg(self, mnem, instr, addr):
        tokens = [
            InstructionTextToken(
                InstructionTextTokenType.InstructionToken, mnem + " ")
        ]
        tokens.append(
            InstructionTextToken(
                InstructionTextTokenType.RegisterToken, instr.arg1)
        )
        tokens.append(
            InstructionTextToken(
                InstructionTextTokenType.OperandSeparatorToken, ", ")
        )
        tokens.append(
            InstructionTextToken(
                InstructionTextTokenType.RegisterToken, instr.arg2)
        )

        if mnem == "stk" and instr.arg1 == "i":
            branch = BranchInfo(BranchType.FunctionReturn, None)
            return tokens, [branch]

        return tokens, []

    def jmp(self, mnem, instr, addr):
        tokens = [
            InstructionTextToken(
                InstructionTextTokenType.InstructionToken, mnem + " ")
        ]
        flag_description = "".join(
            [v if instr.arg1 & k else "" for k, v in flags.items()]
        )
        tokens.append(
            InstructionTextToken(
                InstructionTextTokenType.TextToken, flag_description)
        )
        tokens.append(
            InstructionTextToken(
                InstructionTextTokenType.OperandSeparatorToken, ", ")
        )
        tokens.append(
            InstructionTextToken(
                InstructionTextTokenType.RegisterToken, instr.arg2)
        )

        true_branch = BranchInfo(BranchType.IndirectBranch, None)
        false_branch = BranchInfo(BranchType.FalseBranch, addr + 3)
        return tokens, [true_branch, false_branch]

from binaryninja import LowLevelILLabel, LLIL_TEMP, ILRegister
from .disassembler import Instruction
from .versions.active import *


class Yan85Lifter:
    def __init__(self):
        self.instructions = {
            "imm": self.imm,
            "add": self.add,
            "stk": self.stk,
            "stm": self.stm,
            "ldm": self.ldm,
            "cmp": self.cmp,
            "jmp": self.jmp,
            "sys": self.sys,
        }

        self.syscalls = {
            "open": self.open,
            "read_code": self.read_code,
            "read_memory": self.read_memory,
            "write": self.write,
            "sleep": self.sleep,
            "exit": self.exit,
        }

    def flags_to_cond(self, flags, il):
        cond = il.flag(flags[0])

        for flag in flags[1:]:
            cond = il.or_expr(1, il.flag(flag), cond)

        return cond

    def val_to_flags(self, val: int):
        f = []
        for k, v in flags.items():
            if val & k:
                f.append(v)
        return f

    def lift_instr(self, data, addr, il):
        instr = Instruction(data)
        func = self.instructions[opcodes[instr.op]]
        return func(instr, addr, il)

    def imm(self, instr, addr, il):
        il_arg2 = il.const(1, instr.arg2)
        il_imm = il.set_reg(1, instr.arg1, il_arg2)
        il.append(il_imm)
        if instr.arg1 == "i":
            il.append(il.jump(il.mult(2, il_arg2, il.const(1, 3))))

    def add(self, instr, addr, il):
        il_arg1 = il.reg(1, instr.arg1)
        il_arg2 = il.reg(1, instr.arg2)
        il_add = il.add(1, il_arg1, il_arg2)
        il.append(il.set_reg(1, instr.arg1, il_add))

    def stk(self, instr, addr, il):
        if instr.arg2 != "none":
            il_reg = il.reg(1, instr.arg2)
            il.append(il.push(1, il_reg))
        if instr.arg1 != "none":
            il_pop = il.pop(1)
            il_set = il.set_reg(1, instr.arg1, il_pop)
            il.append(il_set)
            if instr.arg1 == "i":
                il.append(il.ret(il.mult(2, il.reg(1, "i"), il.const(1, 3))))

    def stm(self, instr, addr, il):
        il_arg1 = il.reg(1, instr.arg1)
        il_arg2 = il.reg(1, instr.arg2)
        il.append(il.store(1, il.add(2, il_arg1, il.const(2, 0x300)), il_arg2))

    def ldm(self, instr, addr, il):
        il_arg1 = il.reg(1, instr.arg1)
        il_arg2 = il.reg(1, instr.arg2)
        il_load = il.load(1, il.add(2, il_arg2, il.const(2, 0x300)))
        il.append(il.set_reg(1, instr.arg1, il_load))

    def cmp(self, instr, addr, il):
        il_arg1 = il.reg(1, instr.arg1)
        il_arg2 = il.reg(1, instr.arg2)

        il.append(il.set_flag("L", il.compare_unsigned_less_than(1, il_arg1, il_arg2)))

        il.append(
            il.set_flag("G", il.compare_unsigned_greater_than(1, il_arg1, il_arg2))
        )

        il.append(il.set_flag("E", il.compare_equal(1, il_arg1, il_arg2)))

        il.append(il.set_flag("N", il.compare_not_equal(1, il_arg1, il_arg2)))

        il.append(
            il.set_flag(
                "Z",
                il.and_expr(
                    1,
                    il.compare_equal(1, il_arg1, il.const(1, 0)),
                    il.compare_equal(1, il_arg2, il.const(1, 0)),
                ),
            )
        )

    def jmp(self, instr, addr, il):
        il_arg2 = il.reg(1, instr.arg2)

        if instr.arg1 == 0:
            il.append(il.jump(il.mult(2, il_arg2, il.const(1, 3))))
        else:
            cond = self.flags_to_cond(self.val_to_flags(instr.arg1), il)

            t = LowLevelILLabel()
            f = LowLevelILLabel()
            il.append(il.if_expr(cond, t, f))
            il.mark_label(t)
            il.append(il.jump(il.mult(2, il_arg2, il.const(1, 3))))
            il.mark_label(f)

    def sys(self, instr, addr, il):
        for k, v in syscalls.items():
            if instr.arg1 & k:
                self.syscalls[v](instr, addr, il)

    def open(self, instr, addr, il):
        il_regA = il.reg(1, "a")
        il_regB = il.reg(1, "b")
        il_regC = il.reg(1, "c")

        temp = LLIL_TEMP(il.temp_reg_count)
        temp_il = ILRegister(il.arch, temp)
        il.append(
            il.intrinsic(
                [temp_il],
                "open",
                [il.add(2, il_regA, il.const(2, 0x300)), il_regB, il_regC],
            )
        )
        il.append(il.set_reg(1, instr.arg2, il.reg(1, temp)))

    def read_code(self, instr, addr, il):
        il_regA = il.reg(1, "a")
        il_regB = il.reg(1, "b")
        il_regC = il.reg(1, "c")

        temp = LLIL_TEMP(il.temp_reg_count)
        temp_il = ILRegister(il.arch, temp)
        il.append(
            il.intrinsic(
                [temp_il],
                "read_code",
                [il_regA, il.mul(2, il_regB, il.const(1, 3)), il_regC],
            )
        )
        il.append(il.set_reg(1, instr.arg2, il.reg(1, temp)))

    def read_memory(self, instr, addr, il):
        il_regA = il.reg(1, "a")
        il_regB = il.reg(1, "b")
        il_regC = il.reg(1, "c")

        temp = LLIL_TEMP(il.temp_reg_count)
        temp_il = ILRegister(il.arch, temp)
        il.append(
            il.intrinsic(
                [temp_il],
                "read_memory",
                [il_regA, il.add(2, il_regB, il.const(2, 0x300)), il_regC],
            )
        )
        il.append(il.set_reg(1, instr.arg2, il.reg(1, temp)))

    def write(self, instr, addr, il):
        il_regA = il.reg(1, "a")
        il_regB = il.reg(1, "b")
        il_regC = il.reg(1, "c")

        temp = LLIL_TEMP(il.temp_reg_count)
        temp_il = ILRegister(il.arch, temp)
        il.append(
            il.intrinsic(
                [temp_il],
                "write",
                [il_regA, il.add(2, il_regB, il.const(2, 0x300)), il_regC],
            )
        )
        il.append(il.set_reg(1, instr.arg2, il.reg(1, temp)))

    def sleep(self, instr, addr, il):
        il_regA = il.reg(1, "a")

        temp = LLIL_TEMP(il.temp_reg_count)
        temp_il = ILRegister(il.arch, temp)
        il.append(il.intrinsic([temp_il], "sleep", [il_regA]))
        il.append(il.set_reg(1, instr.arg2, il.reg(1, temp)))

    def exit(self, instr, addr, il):
        il_argA = il.reg(1, "a")
        il.append(il.intrinsic([], "exit", [il_argA]))
        il.append(il.no_ret())

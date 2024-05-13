from typing import ClassVar
from dataclasses import dataclass
import enum

from .types import Address, Byte, Register


@dataclass
class BaseOpCode:
    CODE: ClassVar[str]


@dataclass
class OpCodeSys(BaseOpCode):
    CODE = "SYS"

    address: Address


@dataclass
class OpCodeCls(BaseOpCode):
    CODE = "CLS"


@dataclass
class OpCodeRet(BaseOpCode):
    CODE = "RET"


@dataclass
class OpCodeJp(BaseOpCode):
    CODE = "JP"

    address: Address


@dataclass
class OpCodeCall(BaseOpCode):
    CODE = "CALL"

    address: Address


@dataclass
class OpCodeSeByte(BaseOpCode):
    CODE = "SEB"

    register: Register
    byte: Byte


@dataclass
class OpCodeSneByte(BaseOpCode):
    CODE = "SNEB"

    register: Register
    byte: Byte


@dataclass
class OpCodeSe(BaseOpCode):
    CODE = "SE"

    register1: Register
    register2: Register


@dataclass
class OpCodeLdByte(BaseOpCode):
    CODE = "LDB"

    register: Register
    byte: Byte


@dataclass
class OpCodeAddByte(BaseOpCode):
    CODE = "ADDB"

    register: Register
    byte: Byte


@dataclass
class OpCodeLd(BaseOpCode):
    CODE = "LD"

    register1: Register
    register2: Register


@dataclass
class OpCodeOr(BaseOpCode):
    CODE = "OR"

    register1: Register
    register2: Register


@dataclass
class OpCodeAnd(BaseOpCode):
    CODE = "AND"

    register1: Register
    register2: Register


@dataclass
class OpCodeXor(BaseOpCode):
    CODE = "XOR"

    register1: Register
    register2: Register


@dataclass
class OpCodeAdd(BaseOpCode):
    CODE = "ADD"

    register1: Register
    register2: Register


@dataclass
class OpCodeSub(BaseOpCode):
    CODE = "SUB"

    register1: Register
    register2: Register


@dataclass
class OpCodeShiftRight(BaseOpCode):
    CODE = "SHR"

    register1: Register
    register2: Register


@dataclass
class OpCodeSubInv(BaseOpCode):
    CODE = "SUBN"

    register1: Register
    register2: Register


@dataclass
class OpCodeShiftLeft(BaseOpCode):
    CODE = "SHL"

    register1: Register
    register2: Register


@dataclass
class OpCodeSne(BaseOpCode):
    CODE = "SNE"

    register1: Register
    register2: Register


@dataclass
class OpCodeLdI(BaseOpCode):
    CODE = "LDI"

    address: Address


@dataclass
class OpCodeJpV0(BaseOpCode):
    CODE = "JPV0"

    address: Address


@dataclass
class OpCodeRnd(BaseOpCode):
    CODE = "RND"

    register: Register
    byte: Byte


@dataclass
class OpCodeDrw(BaseOpCode):
    CODE = "DRW"

    registerX: Register
    registerY: Register
    nibble: Byte


@dataclass
class OpCodeSkp(BaseOpCode):
    CODE = "SKP"

    register: Register


@dataclass
class OpCodeSknp(BaseOpCode):
    CODE = "SKNP"

    register: Register


@dataclass
class OpCodeLdDelayRead(BaseOpCode):
    CODE = "LDDR"

    register: Register


@dataclass
class OpCodeLdKey(BaseOpCode):
    CODE = "LDK"

    register: Register


@dataclass
class OpCodeLdDelayStore(BaseOpCode):
    CODE = "LDDS"

    register: Register


@dataclass
class OpCodeLdSoundStore(BaseOpCode):
    CODE = "LDSS"

    register: Register


@dataclass
class OpCodeAddI(BaseOpCode):
    CODE = "ADDI"

    register: Register


@dataclass
class OpCodeLdF(BaseOpCode):
    CODE = "LDF"

    register: Register


@dataclass
class OpCodeLdBCD(BaseOpCode):
    CODE = "LDB"

    register: Register


@dataclass
class OpCodeLdRegStore(BaseOpCode):
    CODE = "LDRS"

    max_register: Register


@dataclass
class OpCodeLdRegRead(BaseOpCode):
    CODE = "LDRR"

    max_register: Register


def parse_opcode(value: Address) -> BaseOpCode | None:
    value_inner = value.value
    b0 = (value_inner & 0xf000) >> 12
    b1 = (value_inner & 0x0f00) >> 8
    b2 = (value_inner & 0x00f0) >> 4
    b3 = value_inner & 0x000f

    addr_value = (b1 << 8) + (b2 << 4) + b3
    byte_value = (b2 << 4) + b3

    if b0 == 0x0:
        if b2 == 0xE and b3 == 0xE:
            return OpCodeRet()
        
        elif b2 == 0xE and b3 == 0x0:
            return OpCodeCls()
        
        else:
            return OpCodeSys(address=Address(addr_value))

    elif b0 == 0x1:
        return OpCodeJp(address=Address(addr_value))

    elif b0 == 0x2:
        return OpCodeCall(address=Address(addr_value))

    elif b0 == 0x3:
        return OpCodeSeByte(register=Register(b1), byte=Byte(byte_value))

    elif b0 == 0x4:
        return OpCodeSneByte(register=Register(b1), byte=Byte(byte_value))
    
    elif b0 == 0x5:
        if b3 == 0x0:
            return OpCodeSe(register1=Register(b1), register2=Register(b2))

    elif b0 == 0x6:
        return OpCodeLdByte(register=Register(b1), byte=Byte(byte_value))

    elif b0 == 0x7:
        return OpCodeAddByte(register=Register(b1), byte=Byte(byte_value))

    elif b0 == 0x8:
        if b3 == 0x0:
            return OpCodeLd(register1=Register(b1), register2=Register(b2))
        elif b3 == 0x1:
            return OpCodeOr(register1=Register(b1), register2=Register(b2))
        elif b3 == 0x2:
            return OpCodeAnd(register1=Register(b1), register2=Register(b2))
        elif b3 == 0x3:
            return OpCodeXor(register1=Register(b1), register2=Register(b2))
        elif b3 == 0x4:
            return OpCodeAdd(register1=Register(b1), register2=Register(b2))
        elif b3 == 0x5:
            return OpCodeSub(register1=Register(b1), register2=Register(b2))
        elif b3 == 0x6:
            return OpCodeShiftRight(register1=Register(b1), register2=Register(b2))
        elif b3 == 0x7:
            return OpCodeSubInv(register1=Register(b1), register2=Register(b2))
        elif b3 == 0xE:
            return OpCodeShiftLeft(register1=Register(b1), register2=Register(b2))

    elif b0 == 0x9:
        if b3 == 0x0:
            return OpCodeSne(register1=Register(b1), register2=Register(b2))

    elif b0 == 0xA:
        return OpCodeLdI(address=Address(addr_value))

    elif b0 == 0xB:
        return OpCodeJpV0(address=Address(addr_value))

    elif b0 == 0xC:
        return OpCodeRnd(register=Register(b1), byte=Byte(byte_value))

    elif b0 == 0xD:
        return OpCodeDrw(registerX=Register(b1), registerY=Register(b2), nibble=Byte(b3))

    elif b0 == 0xE:
        if b2 == 0x9 and b3 == 0xE:
            return OpCodeSkp(register=Register(b1))

        elif b2 == 0xA and b3 == 0x1:
            return OpCodeSknp(register=Register(b1))

    elif b0 == 0xF:
        if b2 == 0x0 and b3 == 0x7:
            return OpCodeLdDelayRead(register=Register(b1))

        if b2 == 0x0 and b3 == 0xA:
            return OpCodeLdKey(register=Register(b1))

        if b2 == 0x1 and b3 == 0x5:
            return OpCodeLdDelayStore(register=Register(b1))

        if b2 == 0x1 and b3 == 0x8:
            return OpCodeLdSoundStore(register=Register(b1))

        if b2 == 0x1 and b3 == 0xE:
            return OpCodeAddI(register=Register(b1))

        if b2 == 0x2 and b3 == 0x9:
            return OpCodeLdF(register=Register(b1))

        if b2 == 0x3 and b3 == 0x3:
            return OpCodeLdBCD(register=Register(b1))

        if b2 == 0x5 and b3 == 0x5:
            return OpCodeLdRegStore(max_register=Register(b1))

        if b2 == 0x6 and b3 == 0x5:
            return OpCodeLdRegRead(max_register=Register(b1))
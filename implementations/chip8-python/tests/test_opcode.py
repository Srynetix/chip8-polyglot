from chip8 import opcodes
from chip8.types import Address, Byte, Register

import pytest

@pytest.mark.parametrize("byte,code", [
    ("0123", opcodes.OpCodeSys(address=Address(0x123))),
    ("00E0", opcodes.OpCodeCls()),
    ("00EE", opcodes.OpCodeRet()),
    ("1123", opcodes.OpCodeJp(address=Address(0x123))),
    ("2123", opcodes.OpCodeCall(address=Address(0x123))),
    ("3123", opcodes.OpCodeSeByte(register=Register(0x1), byte=Byte(0x23))),
    ("4123", opcodes.OpCodeSneByte(register=Register(0x1), byte=Byte(0x23))),
    ("5120", opcodes.OpCodeSe(register1=Register(0x1), register2=Register(0x2))),
    ("6123", opcodes.OpCodeLdByte(register=Register(0x1), byte=Byte(0x23))),
    ("7123", opcodes.OpCodeAddByte(register=Register(0x1), byte=Byte(0x23))),
    ("8120", opcodes.OpCodeLd(register1=Register(0x1), register2=Register(0x2))),
    ("8121", opcodes.OpCodeOr(register1=Register(0x1), register2=Register(0x2))),
    ("8122", opcodes.OpCodeAnd(register1=Register(0x1), register2=Register(0x2))),
    ("8123", opcodes.OpCodeXor(register1=Register(0x1), register2=Register(0x2))),
    ("8124", opcodes.OpCodeAdd(register1=Register(0x1), register2=Register(0x2))),
    ("8125", opcodes.OpCodeSub(register1=Register(0x1), register2=Register(0x2))),
    ("8126", opcodes.OpCodeShiftRight(register1=Register(0x1), register2=Register(0x2))),
    ("8127", opcodes.OpCodeSubInv(register1=Register(0x1), register2=Register(0x2))),
    ("812E", opcodes.OpCodeShiftLeft(register1=Register(0x1), register2=Register(0x2))),
    ("9120", opcodes.OpCodeSne(register1=Register(0x1), register2=Register(0x2))),
    ("A123", opcodes.OpCodeLdI(address=Address(0x123))),
    ("B123", opcodes.OpCodeJpV0(address=Address(0x123))),
    ("C123", opcodes.OpCodeRnd(register=Register(0x1), byte=Byte(0x23))),
    ("D123", opcodes.OpCodeDrw(register_x=Register(0x1), register_y=Register(0x2), height=Byte(0x3))),
    ("E19E", opcodes.OpCodeSkp(register=Register(0x1))),
    ("E1A1", opcodes.OpCodeSknp(register=Register(0x1))),
    ("F107", opcodes.OpCodeLdDelayRead(register=Register(0x1))),
    ("F10A", opcodes.OpCodeLdKey(register=Register(0x1))),
    ("F115", opcodes.OpCodeLdDelayStore(register=Register(0x1))),
    ("F118", opcodes.OpCodeLdSoundStore(register=Register(0x1))),
    ("F11E", opcodes.OpCodeAddI(register=Register(0x1))),
    ("F129", opcodes.OpCodeLdF(register=Register(0x1))),
    ("F133", opcodes.OpCodeLdBCD(register=Register(0x1))),
    ("F155", opcodes.OpCodeLdRegStore(max_register=Register(0x1))),
    ("F165", opcodes.OpCodeLdRegRead(max_register=Register(0x1))),
])
def test_opcode(byte, code) -> None:
    assert opcodes.parse_opcode(Address(int(byte, base=16))) == code
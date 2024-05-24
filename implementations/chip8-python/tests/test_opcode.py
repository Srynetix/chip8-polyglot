from chip8 import opcodes
from chip8.types import Address, Byte, Register

import pytest


@pytest.mark.parametrize(
    "byte,code",
    [
        ("0123", opcodes.SYS(address=Address(0x123))),
        ("00FF", opcodes.HIRES()),
        ("00FE", opcodes.LORES()),
        ("00C1", opcodes.SCRLDWN(height=Byte(0x1))),
        ("00FB", opcodes.SCRLRGHT()),
        ("00FC", opcodes.SCRLLFT()),
        ("00FD", opcodes.EXIT()),
        ("00E0", opcodes.CLS()),
        ("00EE", opcodes.RET()),
        ("1123", opcodes.JP(address=Address(0x123))),
        ("2123", opcodes.CALL(address=Address(0x123))),
        ("3123", opcodes.SEB(register=Register(0x1), byte=Byte(0x23))),
        ("4123", opcodes.SNEB(register=Register(0x1), byte=Byte(0x23))),
        ("5120", opcodes.SE(register1=Register(0x1), register2=Register(0x2))),
        ("6123", opcodes.LDB(register=Register(0x1), byte=Byte(0x23))),
        ("7123", opcodes.ADDB(register=Register(0x1), byte=Byte(0x23))),
        ("8120", opcodes.LD(register1=Register(0x1), register2=Register(0x2))),
        ("8121", opcodes.OR(register1=Register(0x1), register2=Register(0x2))),
        ("8122", opcodes.AND(register1=Register(0x1), register2=Register(0x2))),
        ("8123", opcodes.XOR(register1=Register(0x1), register2=Register(0x2))),
        ("8124", opcodes.ADD(register1=Register(0x1), register2=Register(0x2))),
        ("8125", opcodes.SUB(register1=Register(0x1), register2=Register(0x2))),
        (
            "8126",
            opcodes.SHR(register1=Register(0x1), register2=Register(0x2)),
        ),
        (
            "8127",
            opcodes.SUBN(register1=Register(0x1), register2=Register(0x2)),
        ),
        (
            "812E",
            opcodes.SHL(register1=Register(0x1), register2=Register(0x2)),
        ),
        ("9120", opcodes.SNE(register1=Register(0x1), register2=Register(0x2))),
        ("A123", opcodes.LDI(address=Address(0x123))),
        ("B123", opcodes.JPOFST(address=Address(0x123), register=Register(0x1))),
        ("C123", opcodes.RND(register=Register(0x1), byte=Byte(0x23))),
        (
            "D123",
            opcodes.DRW(
                register_x=Register(0x1), register_y=Register(0x2), height=Byte(0x3)
            ),
        ),
        (
            "D120",
            opcodes.SDRW(register_x=Register(0x1), register_y=Register(0x2)),
        ),
        ("E19E", opcodes.SKP(register=Register(0x1))),
        ("E1A1", opcodes.SKNP(register=Register(0x1))),
        ("F107", opcodes.LDLY(register=Register(0x1))),
        ("F10A", opcodes.LDK(register=Register(0x1))),
        ("F115", opcodes.SDLY(register=Register(0x1))),
        ("F118", opcodes.SSND(register=Register(0x1))),
        ("F11E", opcodes.ADDI(register=Register(0x1))),
        ("F129", opcodes.LDF(register=Register(0x1))),
        ("F130", opcodes.SLDF(register=Register(0x1))),
        ("F133", opcodes.LDBCD(register=Register(0x1))),
        ("F155", opcodes.SRG(max_register=Register(0x1))),
        ("F165", opcodes.LRG(max_register=Register(0x1))),
        ("F175", opcodes.SRGF(max_register=Register(0x1))),
        ("F185", opcodes.LRGF(max_register=Register(0x1))),
    ],
)
def test_opcode(byte, code) -> None:
    assert opcodes.parse_opcode(Address(int(byte, base=16))) == code

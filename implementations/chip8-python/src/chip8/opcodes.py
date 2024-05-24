from dataclasses import dataclass

from .types import Address, Byte, Register


class OpCode:
    pass


@dataclass
class SYS(OpCode):
    """SYS (0NNN) - Execute a system instruction NNN."""

    address: Address


@dataclass
class HIRES(OpCode):
    """HIRES (00FF) - Change the display to higher resolution (S-CHIP only)."""


@dataclass
class LORES(OpCode):
    """LORES (00FE) - Change the display to lower resolution (S-CHIP only)."""


@dataclass
class SCRLDWN(OpCode):
    """SCRLDWN (00CN) - Scroll down N lines (S-CHIP only)."""

    height: Byte


@dataclass
class SCRLRGHT(OpCode):
    """SCRLRGHT (OOFB) - Scroll right (S-CHIP only)."""


@dataclass
class SCRLLFT(OpCode):
    """SCRLLFT (00FC) - Scroll left (S-CHIP only)."""


@dataclass
class SCRLUP(OpCode):
    """SCRLUP (00DN) - Scroll up N pixels. (XO-CHIP only)."""

    height: Byte


@dataclass
class EXIT(OpCode):
    """EXIT (00FD) - Exit interpreter (S-CHIP only)."""


@dataclass
class SDRW(OpCode):
    """SDRW (DXY0) - Draw a 16x16 sprite (S-CHIP only)."""

    register_x: Register
    register_y: Register


@dataclass
class CLS(OpCode):
    """CLS (00E0) - Clear screen."""


@dataclass
class RET(OpCode):
    """RET (00EE) - Return from procedure."""


@dataclass
class JP(OpCode):
    """JP (1NNN) - Jump to address NNN."""

    address: Address


@dataclass
class CALL(OpCode):
    """CALL (2NNN) - Push PC to stack and jump to address NNN."""

    address: Address


@dataclass
class SEB(OpCode):
    """SEB (3XNN) - Jump if VX == byte NN."""

    register: Register
    byte: Byte


@dataclass
class SNEB(OpCode):
    """SNEB (4XNN) - Jump if VX != byte NN."""

    register: Register
    byte: Byte


@dataclass
class SE(OpCode):
    """SE (5XY0) - Jump if VX == VY."""

    register1: Register
    register2: Register


@dataclass
class SRGI(OpCode):
    """SRGI (5XY2) - Store VX to VY in (I..I+(Y-X)) (XO-CHIP only)."""

    min_register: Register
    max_register: Register


@dataclass
class LRGI(OpCode):
    """LRGI (5XY3) - Load VX to VY from (I..I+(Y-X)) (XO-CHIP only)."""

    min_register: Register
    max_register: Register


@dataclass
class LDB(OpCode):
    """LDB (6XNN) - VX = byte NN."""

    register: Register
    byte: Byte


@dataclass
class ADDB(OpCode):
    """ADDB (7XNN) - VX += byte NN."""

    register: Register
    byte: Byte


@dataclass
class LD(OpCode):
    """LD (8XY0) - VX = VY."""

    register1: Register
    register2: Register


@dataclass
class OR(OpCode):
    """OR (8XY1) - VX = VX | VY."""

    register1: Register
    register2: Register


@dataclass
class AND(OpCode):
    """AND (8XY2) - VX = VX & VY."""

    register1: Register
    register2: Register


@dataclass
class XOR(OpCode):
    """XOR (8XY3) - VX = VX ^ VY."""

    register1: Register
    register2: Register


@dataclass
class ADD(OpCode):
    """ADD (8XY4) - VX = VX + VY."""

    register1: Register
    register2: Register


@dataclass
class SUB(OpCode):
    """SUB (8XY5) - VX = VX - VY."""

    register1: Register
    register2: Register


@dataclass
class SHR(OpCode):
    """SHR (8XY6) - VX = VX >> VY."""

    register1: Register
    register2: Register


@dataclass
class SUBN(OpCode):
    """SUBN (8XY7) - VX = VY - VX."""

    register1: Register
    register2: Register


@dataclass
class SHL(OpCode):
    """SHL (8XYF) - VX = VX << VY."""

    register1: Register
    register2: Register


@dataclass
class SNE(OpCode):
    """SNE (9XY0) - Jump if VX != VY."""

    register1: Register
    register2: Register


@dataclass
class LDI(OpCode):
    """LDI (ANNN) - I = address NNN."""

    address: Address


@dataclass
class JPOFST(OpCode):
    """JPOFST (BNNN) - Jump to address NNN + register V0.

    Has a quirk (jump_vx) in the form (BXNN), which does a jump
    to address NNN + register VX.
    """

    address: Address

    # For jump_vx quirk
    register: Register


@dataclass
class RND(OpCode):
    """RND (CXNN) - VX = (rand() % 256) | byte NN."""

    register: Register
    byte: Byte


@dataclass
class DRW(OpCode):
    """DRW (DXYN) - Draw a sprite of height N at coordinates VX and VY."""

    register_x: Register
    register_y: Register
    height: Byte


@dataclass
class SKP(OpCode):
    """SKP (EX9E) - Skip to next instruction if key KX is pressed."""

    register: Register


@dataclass
class SKNP(OpCode):
    """SKNP (EXA1) - Skip to next instruction if key KX is NOT pressed."""

    register: Register


@dataclass
class LDIL(OpCode):
    """LDIL (F000, NNNN) - I = long address NNNN (XO-CHIP only)."""

    address: Address


@dataclass
class PLN(OpCode):
    """PLN (FX01) - Select 0 or more drawing planes by bitmask (0 <= N <= 3) (XO-CHIP only)."""

    mask: Byte


@dataclass
class AUD(OpCode):
    """AUD (F002) - Store 16 bytes from I in the audio buffer (XO-CHIP only)."""


@dataclass
class LDLY(OpCode):
    """LDLY (FX07) - VX = Delay timer."""

    register: Register


@dataclass
class LDK(OpCode):
    """LDK (FX0A) - VX = Released key.

    Should not increment PC while no key is released.
    """

    register: Register


@dataclass
class SDLY(OpCode):
    """SDLY (FX15) - Delay timer = VX."""

    register: Register


@dataclass
class SSND(OpCode):
    """SSND (FX18) - Sound timer = VX."""

    register: Register


@dataclass
class ADDI(OpCode):
    """ADDI (FX1E) - I += VX."""

    register: Register


@dataclass
class LDF(OpCode):
    """LDF (FX29) - I = font for hex character X."""

    register: Register


@dataclass
class SLDF(OpCode):
    """SLDF (FX30) - I = super font for hex character X (S-CHIP only)."""

    register: Register


@dataclass
class LDBCD(OpCode):
    """LDBCD (FX33) - (I, I + 1, I + 2) = BCD(VX)."""

    register: Register


@dataclass
class PTCH(OpCode):
    """PTCH (FX3A) - Set audio playback rate to 4000*2^((VX - 64) / 48) (XO-CHIP only)."""

    register: Register


@dataclass
class SRG(OpCode):
    """SRG (FX55) - Store V0 to VX in (I..I+X)."""

    max_register: Register


@dataclass
class LRG(OpCode):
    """LRG (FX65) - Load V0 to VX from (I..I+X)."""

    max_register: Register


@dataclass
class SRGF(OpCode):
    """SRGF (FX75) - Store V0 to VX in flag registers."""

    max_register: Register


@dataclass
class LRGF(OpCode):
    """LRGF (FX85) - Load V0 to VX from flag registers."""

    max_register: Register


def parse_opcode(value: Address) -> OpCode | None:
    value_inner = value.value
    b0 = (value_inner & 0xF000) >> 12
    b1 = (value_inner & 0x0F00) >> 8
    b2 = (value_inner & 0x00F0) >> 4
    b3 = value_inner & 0x000F

    addr_value = (b1 << 8) + (b2 << 4) + b3
    byte_value = (b2 << 4) + b3

    if b0 == 0x0:
        if b2 == 0xC:
            return SCRLDWN(height=Byte(b3))

        elif b2 == 0xD:
            return SCRLUP(height=Byte(b3))

        elif b2 == 0xE:
            if b3 == 0xE:
                return RET()

            if b3 == 0x0:
                return CLS()

        elif b2 == 0xF:
            if b3 == 0xB:
                return SCRLRGHT()

            elif b3 == 0xC:
                return SCRLLFT()

            elif b3 == 0xD:
                return EXIT()

            elif b3 == 0xE:
                return LORES()

            elif b3 == 0xF:
                return HIRES()

        return SYS(address=Address(addr_value))

    elif b0 == 0x1:
        return JP(address=Address(addr_value))

    elif b0 == 0x2:
        return CALL(address=Address(addr_value))

    elif b0 == 0x3:
        return SEB(register=Register(b1), byte=Byte(byte_value))

    elif b0 == 0x4:
        return SNEB(register=Register(b1), byte=Byte(byte_value))

    elif b0 == 0x5:
        if b3 == 0x0:
            return SE(register1=Register(b1), register2=Register(b2))

        elif b3 == 0x2:
            return SRGI(min_register=Register(b1), max_register=Register(b2))

        elif b3 == 0x3:
            return LRGI(min_register=Register(b1), max_register=Register(b2))

    elif b0 == 0x6:
        return LDB(register=Register(b1), byte=Byte(byte_value))

    elif b0 == 0x7:
        return ADDB(register=Register(b1), byte=Byte(byte_value))

    elif b0 == 0x8:
        if b3 == 0x0:
            return LD(register1=Register(b1), register2=Register(b2))
        elif b3 == 0x1:
            return OR(register1=Register(b1), register2=Register(b2))
        elif b3 == 0x2:
            return AND(register1=Register(b1), register2=Register(b2))
        elif b3 == 0x3:
            return XOR(register1=Register(b1), register2=Register(b2))
        elif b3 == 0x4:
            return ADD(register1=Register(b1), register2=Register(b2))
        elif b3 == 0x5:
            return SUB(register1=Register(b1), register2=Register(b2))
        elif b3 == 0x6:
            return SHR(register1=Register(b1), register2=Register(b2))
        elif b3 == 0x7:
            return SUBN(register1=Register(b1), register2=Register(b2))
        elif b3 == 0xE:
            return SHL(register1=Register(b1), register2=Register(b2))

    elif b0 == 0x9:
        if b3 == 0x0:
            return SNE(register1=Register(b1), register2=Register(b2))

    elif b0 == 0xA:
        return LDI(address=Address(addr_value))

    elif b0 == 0xB:
        return JPOFST(address=Address(addr_value), register=Register(b1))

    elif b0 == 0xC:
        return RND(register=Register(b1), byte=Byte(byte_value))

    elif b0 == 0xD:
        if b3 == 0x0:
            return SDRW(register_x=Register(b1), register_y=Register(b2))
        return DRW(register_x=Register(b1), register_y=Register(b2), height=Byte(b3))

    elif b0 == 0xE:
        if b2 == 0x9 and b3 == 0xE:
            return SKP(register=Register(b1))

        elif b2 == 0xA and b3 == 0x1:
            return SKNP(register=Register(b1))

    elif b0 == 0xF:
        if b2 == 0x0:
            if b3 == 0x0:
                # Address will be filled later in time.
                return LDIL(Address(0x0))

            elif b3 == 0x1:
                return PLN(mask=Byte(b1))

            elif b3 == 0x2:
                return AUD()

            elif b3 == 0x7:
                return LDLY(register=Register(b1))

            elif b3 == 0xA:
                return LDK(register=Register(b1))

        elif b2 == 0x1:
            if b3 == 0x5:
                return SDLY(register=Register(b1))

            elif b3 == 0x8:
                return SSND(register=Register(b1))

            elif b3 == 0xE:
                return ADDI(register=Register(b1))

        elif b2 == 0x2:
            if b3 == 0x9:
                return LDF(register=Register(b1))

        elif b2 == 0x3:
            if b3 == 0x0:
                return SLDF(register=Register(b1))

            elif b3 == 0x3:
                return LDBCD(register=Register(b1))

            elif b3 == 0xA:
                return PTCH(register=Register(b1))

        elif b2 == 0x5:
            if b3 == 0x5:
                return SRG(max_register=Register(b1))

        elif b2 == 0x6:
            if b3 == 0x5:
                return LRG(max_register=Register(b1))

        elif b2 == 0x7:
            if b3 == 0x5:
                return SRGF(max_register=Register(b1))

        elif b2 == 0x8:
            if b3 == 0x5:
                return LRGF(max_register=Register(b1))

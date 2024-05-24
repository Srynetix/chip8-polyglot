from chip8.engine import Engine, StepResult
from chip8.types import Address, Byte, Register
from chip8 import opcodes


def test_srgi():
    # Arrange
    engine = Engine()
    engine._registers.set_i(Address(0x200))
    engine._registers.set_vx(Register(0x0), Byte(0x9))
    engine._registers.set_vx(Register(0x1), Byte(0xA))
    engine._registers.set_vx(Register(0x2), Byte(0xB))
    engine._registers.set_vx(Register(0x3), Byte(0xC))
    engine._registers.set_vx(Register(0x4), Byte(0xD))

    # Act
    engine._process_opcode(
        opcodes.SRGI(min_register=Register(1), max_register=Register(3))
    )

    # Assert
    assert engine._registers.i == Address(0x200)
    assert engine._memory.read_memory(Address(0x200), 4) == [
        Byte(0xA),
        Byte(0xB),
        Byte(0xC),
        Byte(0x0),
    ]
    assert engine._registers.pc == Address(0x202)


def test_lrgi():
    # Arrange
    engine = Engine()
    engine._registers.set_i(Address(0x200))
    engine._memory.store_memory(
        Address(0x200),
        [
            Byte(0xA),
            Byte(0xB),
            Byte(0xC),
            Byte(0xD),
        ],
    )

    # Act
    engine._process_opcode(
        opcodes.LRGI(min_register=Register(1), max_register=Register(3))
    )

    # Assert
    assert engine._registers.i == Address(0x200)
    assert engine._registers.get_vx(Register(0x0)) == Byte(0x0)
    assert engine._registers.get_vx(Register(0x1)) == Byte(0xA)
    assert engine._registers.get_vx(Register(0x2)) == Byte(0xB)
    assert engine._registers.get_vx(Register(0x3)) == Byte(0xC)
    assert engine._registers.get_vx(Register(0x4)) == Byte(0x0)
    assert engine._registers.pc == Address(0x202)


def test_ldil():
    # Arrange
    engine = Engine()
    engine._registers.set_i(Address(0x200))

    # Act
    engine._process_opcode(opcodes.LDIL(Address(0xFABC)))

    # Assert
    assert engine._registers.i == 0xFABC
    assert engine._registers.pc == Address(0x202)


def test_ldil_complete():
    # Arrange
    engine = Engine()
    engine.set_instructions_per_step(1)
    engine._registers.set_i(Address(0x0))
    engine._memory.store_memory(
        Address(0x200),
        [
            # LDIL
            Byte(0xF0),
            Byte(0x00),
            Byte(0xDA),
            Byte(0xBC),
            # LRGI (to check if memory is enough)
            Byte(0x50),
            Byte(0x03),
        ],
    )

    # Act
    res1 = engine.step()
    res2 = engine.step()

    # Assert
    assert res1 == res2 == StepResult.Success
    assert engine._registers.i == Address(0xDABC)

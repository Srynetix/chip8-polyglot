import enum
from random import Random
import time

from .display import Display
from .font import Font
from .memory import Memory
from .registers import Registers
from .stack import Stack
from .keypad import Keypad
from .timers import Timers
from .cartridge import Cartridge
from .quirks import Quirks
from .types import Address, Register, Byte
from . import opcodes


class StepResult(enum.Enum):
    Success = enum.auto()
    Loop = enum.auto()
    BadOpCode = enum.auto()


class Engine:
    _display: Display
    _font: Font
    _memory: Memory
    _registers: Registers
    _stack: Stack
    _rng: Random
    _timers: Timers
    _quirks: Quirks
    _keypad: Keypad
    _ticks: int
    _beep: bool

    def __init__(self) -> None:
        self._display = Display()
        self._font = Font.get_default()
        self._memory = Memory()
        self._registers = Registers()
        self._stack = Stack()
        self._keypad = Keypad()
        self._rng = Random()
        self._quirks = Quirks()
        self._timers = Timers()
        self._ticks = 0
        self._beep = False

        self.reset()

    def reset(self) -> None:
        self._display.reset()
        self._memory.reset()
        self._registers.reset()
        self._stack.reset()
        self._keypad.reset()
        self._timers.reset()
        self._ticks = 0
        self._beep = False

        # Load font
        self._memory.store_memory(Address(0x0), self._font._data)

    def load_cartridge(self, cartridge: Cartridge) -> None:
        self._memory.store_memory(Address(0x200), cartridge._data)

    def step_timers(self) -> None:
        self._keypad.step()
        self._timers.step()

    def step(self) -> StepResult:
        self._beep = self._timers.sound_timer.value > 0

        # Read opcode
        int_code = self._memory.read_opcode(self._registers.pc)
        code = opcodes.parse_opcode(int_code)
        if code is None:
            return StepResult.BadOpCode

        # Check infinite loop
        if isinstance(code, opcodes.OpCodeJp):
            if code.address == self._registers.pc:
                # Yep, that's a loop
                return StepResult.Loop

        self._process_opcode(code)
        self._ticks += 1

        return StepResult.Success

    def run_forever(self) -> None:
        while True:
            result = self.step()
            if result != StepResult.Success:
                raise RuntimeError(result)
            time.sleep(0.016)

    def _process_opcode(self, opcode: opcodes.BaseOpCode) -> None:
        if isinstance(opcode, opcodes.OpCodeSys):
            print("Unsupported SYS opcode")
            self._registers.increment_pc()

        elif isinstance(opcode, opcodes.OpCodeCls):
            self._display.reset()
            self._registers.increment_pc()

        elif isinstance(opcode, opcodes.OpCodeRet):
            addr = self._stack.pop_stack()
            self._registers.set_pc(addr)
            self._registers.increment_pc()

        elif isinstance(opcode, opcodes.OpCodeJp):
            self._registers.set_pc(opcode.address)

        elif isinstance(opcode, opcodes.OpCodeCall):
            self._stack.push_stack(self._registers.pc)
            self._registers.set_pc(opcode.address)

        elif isinstance(opcode, opcodes.OpCodeSeByte):
            reg_value = self._registers.get_vx(opcode.register)
            if reg_value == opcode.byte:
                self._registers.increment_pc()
            self._registers.increment_pc()

        elif isinstance(opcode, opcodes.OpCodeSneByte):
            reg_value = self._registers.get_vx(opcode.register)
            if reg_value != opcode.byte:
                self._registers.increment_pc()
            self._registers.increment_pc()

        elif isinstance(opcode, opcodes.OpCodeSe):
            reg_value1 = self._registers.get_vx(opcode.register1)
            reg_value2 = self._registers.get_vx(opcode.register2)
            if reg_value1 == reg_value2:
                self._registers.increment_pc()
            self._registers.increment_pc()

        elif isinstance(opcode, opcodes.OpCodeLdByte):
            self._registers.set_vx(opcode.register, opcode.byte)
            self._registers.increment_pc()

        elif isinstance(opcode, opcodes.OpCodeAddByte):
            self._registers.set_vx(opcode.register, self._registers.get_vx(opcode.register) + opcode.byte)
            self._registers.increment_pc()

        elif isinstance(opcode, opcodes.OpCodeLd):
            self._registers.set_vx(opcode.register1, self._registers.get_vx(opcode.register2))
            self._registers.increment_pc()

        elif isinstance(opcode, opcodes.OpCodeOr):
            self._registers.set_vx(
                opcode.register1, self._registers.get_vx(opcode.register1) | self._registers.get_vx(opcode.register2)
            )

            if self._quirks._vf_reset:
                self._registers.set_carry(False)

            self._registers.increment_pc()

        elif isinstance(opcode, opcodes.OpCodeAnd):
            self._registers.set_vx(
                opcode.register1, self._registers.get_vx(opcode.register1) & self._registers.get_vx(opcode.register2)
            )

            if self._quirks._vf_reset:
                self._registers.set_carry(False)

            self._registers.increment_pc()

        elif isinstance(opcode, opcodes.OpCodeXor):
            self._registers.set_vx(
                opcode.register1, self._registers.get_vx(opcode.register1) ^ self._registers.get_vx(opcode.register2)
            )

            if self._quirks._vf_reset:
                self._registers.set_carry(False)

            self._registers.increment_pc()

        elif isinstance(opcode, opcodes.OpCodeAdd):
            added = self._registers.get_vx(opcode.register1).value + self._registers.get_vx(opcode.register2).value

            self._registers.set_vx(opcode.register1, Byte(added))
            self._registers.set_carry(added > 255)

            self._registers.increment_pc()

        elif isinstance(opcode, opcodes.OpCodeSub):
            vx = self._registers.get_vx(opcode.register1).value
            vy = self._registers.get_vx(opcode.register2).value

            self._registers.set_vx(opcode.register1, Byte(vx - vy))
            self._registers.set_carry(vx >= vy)

            self._registers.increment_pc()

        elif isinstance(opcode, opcodes.OpCodeShiftRight):
            if self._quirks._shift_y:
                self._registers.set_vx(opcode.register1, self._registers.get_vx(opcode.register2))
            vx = self._registers.get_vx(opcode.register1)

            self._registers.set_vx(opcode.register1, Byte(vx.value // 2))
            self._registers.set_carry(vx.value & 1 == 1)

            self._registers.increment_pc()

        elif isinstance(opcode, opcodes.OpCodeSubInv):
            vx = self._registers.get_vx(opcode.register1).value
            vy = self._registers.get_vx(opcode.register2).value

            self._registers.set_vx(opcode.register1, Byte(vy - vx))
            self._registers.set_carry(vx <= vy)

            self._registers.increment_pc()

        elif isinstance(opcode, opcodes.OpCodeShiftLeft):
            if self._quirks._shift_y:
                self._registers.set_vx(opcode.register1, self._registers.get_vx(opcode.register2))
            vx = self._registers.get_vx(opcode.register1)

            self._registers.set_vx(opcode.register1, Byte(vx.value * 2))
            self._registers.set_carry(vx.value & 0b1000_0000 == 0b1000_0000)

            self._registers.increment_pc()

        elif isinstance(opcode, opcodes.OpCodeSne):
            reg_value1 = self._registers.get_vx(opcode.register1)
            reg_value2 = self._registers.get_vx(opcode.register2)

            if reg_value1 != reg_value2:
                self._registers.increment_pc()
            self._registers.increment_pc()
        
        elif isinstance(opcode, opcodes.OpCodeLdI):
            self._registers.set_i(opcode.address)

            self._registers.increment_pc()

        elif isinstance(opcode, opcodes.OpCodeJpV0):
            v0 = self._registers.get_vx(Register(0))

            self._registers.set_pc(Address(v0.value + opcode.address.value))

        elif isinstance(opcode, opcodes.OpCodeRnd):
            value = self._rng.randint(0, 256) & opcode.byte.value
            self._registers.set_vx(opcode.register, Byte(value))

            self._registers.increment_pc()

        elif isinstance(opcode, opcodes.OpCodeDrw):
            vx = self._registers.get_vx(opcode.registerX)
            vy = self._registers.get_vx(opcode.registerY)
            mem = self._memory.read_memory(self._registers.i, opcode.nibble)

            collision = self._display.draw(vx.value, vy.value, mem, clip=self._quirks._draw_clipping)
            self._registers.set_carry(collision)

            self._registers.increment_pc()

        elif isinstance(opcode, opcodes.OpCodeSkp):
            vx = self._registers.get_vx(opcode.register)
            if self._keypad.get_kx(vx):
                self._registers.increment_pc()
            self._registers.increment_pc()

        elif isinstance(opcode, opcodes.OpCodeSknp):
            vx = self._registers.get_vx(opcode.register)
            if not self._keypad.get_kx(vx):
                self._registers.increment_pc()
            self._registers.increment_pc()

        elif isinstance(opcode, opcodes.OpCodeLdDelayRead):
            self._registers.set_vx(opcode.register, self._timers.delay_timer)

            self._registers.increment_pc()

        elif isinstance(opcode, opcodes.OpCodeLdKey):
            if self._keypad._last_released_key:
                self._registers.set_vx(opcode.register, self._keypad._last_released_key)
                self._registers.increment_pc()

        elif isinstance(opcode, opcodes.OpCodeLdDelayStore):
            self._timers.set_delay_timer(self._registers.get_vx(opcode.register))

            self._registers.increment_pc()

        elif isinstance(opcode, opcodes.OpCodeLdSoundStore):
            self._timers.set_sound_timer(self._registers.get_vx(opcode.register))

            self._registers.increment_pc()

        elif isinstance(opcode, opcodes.OpCodeAddI):
            i_value = self._registers.i.value
            reg_value = self._registers.get_vx(opcode.register).value

            carry = (i_value + reg_value) >= 0x1000
            if self._quirks._add_i_carry:
                self._registers.set_carry(carry)

            self._registers.set_i(Address(i_value + reg_value))

            self._registers.increment_pc()

        elif isinstance(opcode, opcodes.OpCodeLdF):
            self._registers.set_i(Address(opcode.register.value * (8 * 5)))

            self._registers.increment_pc()

        elif isinstance(opcode, opcodes.OpCodeLdBCD):
            value = self._registers.get_vx(opcode.register).value
            i0 = value // 100
            i1 = (value % 100) // 10
            i2 = (value % 10)

            self._memory.store_memory(self._registers.i, [Byte(i0)])
            self._memory.store_memory(self._registers.i + 1, [Byte(i1)])
            self._memory.store_memory(self._registers.i + 2, [Byte(i2)])

            self._registers.increment_pc()

        elif isinstance(opcode, opcodes.OpCodeLdRegStore):
            for x in range(opcode.max_register.value + 1):
                self._memory.store_memory(self._registers.i + x, [self._registers.get_vx(Register(x))])

            if self._quirks._index_increment:
                self._registers.set_i(self._registers.i + opcode.max_register.value + 1)

            self._registers.increment_pc()

        elif isinstance(opcode, opcodes.OpCodeLdRegRead):
            for x in range(opcode.max_register.value + 1):
                value = self._memory.read_memory(self._registers.i + x, Byte(1))
                self._registers.set_vx(Register(x), value[0])

            if self._quirks._index_increment:
                self._registers.set_i(self._registers.i + opcode.max_register.value + 1)

            self._registers.increment_pc()

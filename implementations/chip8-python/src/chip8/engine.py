import enum
import logging
from random import Random

from .signal import Signal

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

logger = logging.getLogger(__name__)


class StepResult(enum.Enum):
    Success = enum.auto()
    Loop = enum.auto()
    BadOpCode = enum.auto()
    Exit = enum.auto()


class Engine:
    _display: Display
    _memory: Memory
    _registers: Registers
    _stack: Stack
    _rng: Random
    _timers: Timers
    _quirks: Quirks
    _keypad: Keypad
    _ticks: int
    _instructions_per_step: int

    on_loop: Signal
    on_exit: Signal
    on_hires: Signal
    on_lores: Signal

    def __init__(self) -> None:
        self._display = Display()
        self._memory = Memory()
        self._registers = Registers()
        self._stack = Stack()
        self._keypad = Keypad()
        self._rng = Random()
        self._quirks = Quirks()
        self._timers = Timers()
        self._ticks = 0
        self._instructions_per_step = 10

        self.on_exit = Signal()
        self.on_loop = Signal()
        self.on_hires = Signal()
        self.on_lores = Signal()

        self.reset()

    def reset(self) -> None:
        self._display.reset()
        self._memory.reset()
        self._registers.reset()
        self._stack.reset()
        self._keypad.reset()
        self._timers.reset()
        self._ticks = 0

        self._memory.store_font(Font.get_default())
        self._memory.store_super_font(Font.get_super_default())

    def load_cartridge(self, cartridge: Cartridge) -> None:
        self._memory.store_cartridge(cartridge)

    def step_timers(self) -> None:
        self._keypad.step()
        self._timers.step()

    def set_instructions_per_step(self, value: int) -> None:
        self._instructions_per_step = value

    @property
    def instructions_per_step(self) -> int:
        return self._instructions_per_step

    @property
    def beeping(self) -> bool:
        return self._timers.sound_timer > 0

    @property
    def quirks(self) -> Quirks:
        return self._quirks

    def step(self) -> StepResult:
        instructions_boost = self._display._mode == self._display.Mode.HIRES
        instructions_per_step = (
            self._instructions_per_step * 2
            if instructions_boost
            else self._instructions_per_step
        )

        for _ in range(instructions_per_step):
            res = self._step_instruction()
            if res != StepResult.Success:
                return res

        return StepResult.Success

    def _step_instruction(self) -> StepResult:
        # Read opcode
        int_code = self._memory.read_opcode(self._registers.pc)
        code = opcodes.parse_opcode(int_code)

        logging.info(f" [step] PC={self._registers.pc} int_code={int_code} code={code}")

        if code is None:
            return StepResult.BadOpCode
        
        # Check exit
        if isinstance(code, opcodes.EXIT):
            self.on_exit.emit()
            return StepResult.Exit

        # Check infinite loop
        if isinstance(code, opcodes.JP):
            if code.address == self._registers.pc:
                # Yep, that's a loop
                self.on_loop.emit()
                return StepResult.Loop

        self._process_opcode(code)
        self._ticks += 1

        return StepResult.Success

    def _process_opcode(self, opcode: opcodes.OpCode) -> None:
        if isinstance(opcode, opcodes.SYS):
            print(f"Unsupported SYS opcode: {opcode}")
            self._registers.increment_pc()

        elif isinstance(opcode, opcodes.CLS):
            self._display.clear()
            self._registers.increment_pc()

        elif isinstance(opcode, opcodes.LORES):
            self._display.set_mode(Display.Mode.LORES)
            self.on_lores.emit()
            self._registers.increment_pc()

        elif isinstance(opcode, opcodes.HIRES):
            self._display.set_mode(Display.Mode.HIRES)
            self.on_hires.emit()
            self._registers.increment_pc()

        elif isinstance(opcode, opcodes.SCRLLFT):
            self._display.scroll_left(legacy_mode=self._quirks.legacy_scrolling)
            self._registers.increment_pc()

        elif isinstance(opcode, opcodes.SCRLRGHT):
            self._display.scroll_right(legacy_mode=self._quirks.legacy_scrolling)
            self._registers.increment_pc()

        elif isinstance(opcode, opcodes.SCRLDWN):
            self._display.scroll_down(
                opcode.height, legacy_mode=self._quirks.legacy_scrolling
            )
            self._registers.increment_pc()

        elif isinstance(opcode, opcodes.RET):
            addr = self._stack.pop_stack()
            self._registers.set_pc(addr)
            self._registers.increment_pc()

        elif isinstance(opcode, opcodes.JP):
            self._registers.set_pc(opcode.address)

        elif isinstance(opcode, opcodes.CALL):
            self._stack.push_stack(self._registers.pc)
            self._registers.set_pc(opcode.address)

        elif isinstance(opcode, opcodes.SEB):
            reg_value = self._registers.get_vx(opcode.register)
            if reg_value == opcode.byte:
                self._registers.increment_pc()
            self._registers.increment_pc()

        elif isinstance(opcode, opcodes.SNEB):
            reg_value = self._registers.get_vx(opcode.register)
            if reg_value != opcode.byte:
                self._registers.increment_pc()
            self._registers.increment_pc()

        elif isinstance(opcode, opcodes.SE):
            reg_value1 = self._registers.get_vx(opcode.register1)
            reg_value2 = self._registers.get_vx(opcode.register2)
            if reg_value1 == reg_value2:
                self._registers.increment_pc()
            self._registers.increment_pc()

        elif isinstance(opcode, opcodes.LDB):
            self._registers.set_vx(opcode.register, opcode.byte)
            self._registers.increment_pc()

        elif isinstance(opcode, opcodes.ADDB):
            self._registers.set_vx(
                opcode.register, self._registers.get_vx(opcode.register) + opcode.byte
            )
            self._registers.increment_pc()

        elif isinstance(opcode, opcodes.LD):
            self._registers.set_vx(
                opcode.register1, self._registers.get_vx(opcode.register2)
            )
            self._registers.increment_pc()

        elif isinstance(opcode, opcodes.OR):
            self._registers.set_vx(
                opcode.register1,
                self._registers.get_vx(opcode.register1)
                | self._registers.get_vx(opcode.register2),
            )

            if self._quirks.vf_reset:
                self._registers.set_carry(False)

            self._registers.increment_pc()

        elif isinstance(opcode, opcodes.AND):
            self._registers.set_vx(
                opcode.register1,
                self._registers.get_vx(opcode.register1)
                & self._registers.get_vx(opcode.register2),
            )

            if self._quirks.vf_reset:
                self._registers.set_carry(False)

            self._registers.increment_pc()

        elif isinstance(opcode, opcodes.XOR):
            self._registers.set_vx(
                opcode.register1,
                self._registers.get_vx(opcode.register1)
                ^ self._registers.get_vx(opcode.register2),
            )

            if self._quirks.vf_reset:
                self._registers.set_carry(False)

            self._registers.increment_pc()

        elif isinstance(opcode, opcodes.ADD):
            # Get inner value to handle overflow
            added = (
                self._registers.get_vx(opcode.register1).value
                + self._registers.get_vx(opcode.register2).value
            )

            self._registers.set_vx(opcode.register1, Byte(added))
            self._registers.set_carry(added > 255)

            self._registers.increment_pc()

        elif isinstance(opcode, opcodes.SUB):
            vx = self._registers.get_vx(opcode.register1)
            vy = self._registers.get_vx(opcode.register2)

            self._registers.set_vx(opcode.register1, vx - vy)
            self._registers.set_carry(vx >= vy)

            self._registers.increment_pc()

        elif isinstance(opcode, opcodes.SHR):
            if self._quirks.shift_y:
                self._registers.set_vx(
                    opcode.register1, self._registers.get_vx(opcode.register2)
                )
            vx = self._registers.get_vx(opcode.register1)

            self._registers.set_vx(opcode.register1, vx // 2)
            self._registers.set_carry(vx & 1 == 1)

            self._registers.increment_pc()

        elif isinstance(opcode, opcodes.SUBN):
            vx = self._registers.get_vx(opcode.register1)
            vy = self._registers.get_vx(opcode.register2)

            self._registers.set_vx(opcode.register1, vy - vx)
            self._registers.set_carry(vx <= vy)

            self._registers.increment_pc()

        elif isinstance(opcode, opcodes.SHL):
            if self._quirks.shift_y:
                self._registers.set_vx(
                    opcode.register1, self._registers.get_vx(opcode.register2)
                )
            vx = self._registers.get_vx(opcode.register1)

            self._registers.set_vx(opcode.register1, vx * 2)
            self._registers.set_carry(vx & 0b1000_0000 == 0b1000_0000)

            self._registers.increment_pc()

        elif isinstance(opcode, opcodes.SNE):
            reg_value1 = self._registers.get_vx(opcode.register1)
            reg_value2 = self._registers.get_vx(opcode.register2)

            if reg_value1 != reg_value2:
                self._registers.increment_pc()
            self._registers.increment_pc()

        elif isinstance(opcode, opcodes.LDI):
            self._registers.set_i(opcode.address)

            self._registers.increment_pc()

        elif isinstance(opcode, opcodes.JPOFST):
            if self._quirks.jump_vx:
                vx = self._registers.get_vx(opcode.register)
                addr = Address(vx.value) + opcode.address
            else:
                v0 = self._registers.get_vx(Register(0))
                addr = Address(v0.value) + opcode.address
            self._registers.set_pc(addr)

        elif isinstance(opcode, opcodes.RND):
            value = opcode.byte & Byte.random(self._rng)
            self._registers.set_vx(opcode.register, value)

            self._registers.increment_pc()

        elif isinstance(opcode, opcodes.DRW):
            vx = self._registers.get_vx(opcode.register_x)
            vy = self._registers.get_vx(opcode.register_y)
            mem = self._memory.read_memory(self._registers.i, opcode.height.value)

            collision = self._display.draw(
                vx.value, vy.value, mem, clip=self._quirks.draw_clipping
            )
            self._registers.set_carry(collision)
            self._registers.increment_pc()

        elif isinstance(opcode, opcodes.SDRW):
            vx = self._registers.get_vx(opcode.register_x)
            vy = self._registers.get_vx(opcode.register_y)
            mem = self._memory.read_memory(self._registers.i, 16 * 2)

            collision = self._display.super_draw(
                vx.value, vy.value, mem, clip=self._quirks.draw_clipping
            )
            self._registers.set_carry(collision)
            self._registers.increment_pc()

        elif isinstance(opcode, opcodes.SKP):
            vx = self._registers.get_vx(opcode.register)
            if self._keypad.get_kx(vx):
                self._registers.increment_pc()
            self._registers.increment_pc()

        elif isinstance(opcode, opcodes.SKNP):
            vx = self._registers.get_vx(opcode.register)
            if not self._keypad.get_kx(vx):
                self._registers.increment_pc()
            self._registers.increment_pc()

        elif isinstance(opcode, opcodes.LDLY):
            self._registers.set_vx(opcode.register, self._timers.delay_timer)

            self._registers.increment_pc()

        elif isinstance(opcode, opcodes.LDK):
            if self._keypad._last_released_key:
                self._registers.set_vx(opcode.register, self._keypad._last_released_key)
                self._registers.increment_pc()

        elif isinstance(opcode, opcodes.SDLY):
            self._timers.set_delay_timer(self._registers.get_vx(opcode.register))

            self._registers.increment_pc()

        elif isinstance(opcode, opcodes.SSND):
            self._timers.set_sound_timer(self._registers.get_vx(opcode.register))

            self._registers.increment_pc()

        elif isinstance(opcode, opcodes.ADDI):
            i_value = self._registers.i
            reg_value = self._registers.get_vx(opcode.register)

            # Look for overflow
            addition = i_value + reg_value
            carry = addition >= 0x1000
            if self._quirks.add_i_carry:
                self._registers.set_carry(carry)

            self._registers.set_i(addition)

            self._registers.increment_pc()

        elif isinstance(opcode, opcodes.LDF):
            self._registers.set_i(
                self._memory.FONT_START_LOCATION
                + Address(opcode.register.value * Font.SPRITE_HEIGHT)
            )

            self._registers.increment_pc()

        elif isinstance(opcode, opcodes.SLDF):
            self._registers.set_i(
                self._memory.SUPER_FONT_START_LOCATION
                + Address(opcode.register.value * Font.SUPER_SPRITE_HEIGHT)
            )

            self._registers.increment_pc()

        elif isinstance(opcode, opcodes.LDBCD):
            value = self._registers.get_vx(opcode.register)

            i0 = value // 100
            i1 = (value % 100) // 10
            i2 = value % 10

            self._memory.store_memory(self._registers.i, [i0])
            self._memory.store_memory(self._registers.i + 1, [i1])
            self._memory.store_memory(self._registers.i + 2, [i2])

            self._registers.increment_pc()

        elif isinstance(opcode, opcodes.SRG):
            for x in range(opcode.max_register.value + 1):
                self._memory.store_memory(
                    self._registers.i + x, [self._registers.get_vx(Register(x))]
                )

            if self._quirks.index_increment:
                self._registers.set_i(self._registers.i + opcode.max_register + 1)

            self._registers.increment_pc()

        elif isinstance(opcode, opcodes.LRG):
            for x in range(opcode.max_register.value + 1):
                value = self._memory.read_memory(self._registers.i + x, 1)
                self._registers.set_vx(Register(x), value[0])

            if self._quirks.index_increment:
                self._registers.set_i(self._registers.i + opcode.max_register + 1)

            self._registers.increment_pc()

        elif isinstance(opcode, opcodes.SRGF):
            for x in range(opcode.max_register.value + 1):
                value = self._memory.store_local_storage(
                    self._registers.i + x, [self._registers.get_vx(Register(x))]
                )

            self._registers.increment_pc()

        elif isinstance(opcode, opcodes.LRGF):
            for x in range(opcode.max_register.value + 1):
                value = self._memory.read_local_storage(self._registers.i + x, 1)
                self._registers.set_vx(Register(x), value[0])

            self._registers.increment_pc()

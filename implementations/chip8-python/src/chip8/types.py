from random import Random


class Address:
    value: int

    def __init__(self, value: int) -> None:
        self.value = value % 65536

    def __repr__(self) -> str:
        return f"Address({self})"
    
    def __str__(self) -> str:
        return f"&{hex(self.value).upper()}"

    def __add__(self, other) -> "Address":
        if isinstance(other, int):
            return Address(self.value + other)
        elif isinstance(other, (Address, Byte, Register)):
            return Address(self.value + other.value)
        raise RuntimeError("Could not add address")
    
    def __sub__(self, other) -> "Address":
        if isinstance(other, int):
            return Address(self.value - other)
        elif isinstance(other, (Address, Byte, Register)):
            return Address(self.value - other.value)
        raise RuntimeError("Could not subtract address")

    def __mul__(self, other) -> "Address":
        if isinstance(other, int):
            return Address(self.value * other)
        elif isinstance(other, (Address, Byte, Register)):
            return Address(self.value * other.value)
        raise RuntimeError("Could not multiply address")

    def __gt__(self, other) -> bool:
        if isinstance(other, int):
            return self.value > other
        elif isinstance(other, (Address, Byte, Register)):
            return self.value > other.value
        raise RuntimeError("Could not compare address")

    def __lt__(self, other) -> bool:
        if isinstance(other, int):
            return self.value < other
        elif isinstance(other, (Address, Byte, Register)):
            return self.value < other.value
        raise RuntimeError("Could not compare address")

    def __ge__(self, other) -> bool:
        if isinstance(other, int):
            return self.value >= other
        elif isinstance(other, (Address, Byte, Register)):
            return self.value >= other.value
        raise RuntimeError("Could not compare address")

    def __eq__(self, other) -> bool:
        if isinstance(other, int):
            return self.value == other
        elif isinstance(other, (Address, Byte, Register)):
            return self.value == other.value
        raise RuntimeError("Could not compare address")
    

class Register:
    value: int

    def __init__(self, value: int) -> None:
        if value < 0 or value > 15:
            raise RuntimeError("Unsupported register value")
        self.value = value

    def __str__(self) -> str:
        return f"V{hex(self.value)[2:].upper()}"

    def __repr__(self) -> str:
        return f"Register({self})"

    def __add__(self, other) -> "Register":
        if isinstance(other, int):
            return Register(self.value + other)
        elif isinstance(other, (Address, Byte, Register)):
            return Register(self.value + other.value)
        raise RuntimeError("Could not add register")
    
    def __sub__(self, other) -> "Register":
        if isinstance(other, int):
            return Register(self.value - other)
        elif isinstance(other, (Address, Byte, Register)):
            return Register(self.value - other.value)
        raise RuntimeError("Could not subtract register")

    def __mul__(self, other) -> "Register":
        if isinstance(other, int):
            return Register(self.value * other)
        elif isinstance(other, (Address, Byte, Register)):
            return Register(self.value * other.value)
        raise RuntimeError("Could not multiply register")

    def __gt__(self, other) -> bool:
        if isinstance(other, int):
            return self.value > other
        elif isinstance(other, (Address, Byte, Register)):
            return self.value > other.value
        raise RuntimeError("Could not compare register")

    def __lt__(self, other) -> bool:
        if isinstance(other, int):
            return self.value < other
        elif isinstance(other, (Address, Byte, Register)):
            return self.value < other.value
        raise RuntimeError("Could not compare register")

    def __eq__(self, other) -> bool:
        if isinstance(other, int):
            return self.value == other
        elif isinstance(other, (Address, Byte, Register)):
            return self.value == other.value
        raise RuntimeError("Could not compare register")
    

class Byte:
    value: int

    def __init__(self, value: int) -> None:
        self.value = value % 256

    def __repr__(self) -> str:
        return f"Byte({self})"

    def __str__(self) -> str:
        return hex(self.value).upper()

    def __or__(self, other) -> "Byte":
        if isinstance(other, int):
            return Byte(self.value | other)
        elif isinstance(other, Byte):
            return Byte(self.value | other.value)
        raise RuntimeError("Could not binary-or byte")

    def __and__(self, other) -> "Byte":
        if isinstance(other, int):
            return Byte(self.value & other)
        elif isinstance(other, Byte):
            return Byte(self.value & other.value)
        raise RuntimeError("Could not binary-and byte")

    def __xor__(self, other) -> "Byte":
        if isinstance(other, int):
            return Byte(self.value ^ other)
        elif isinstance(other, Byte):
            return Byte(self.value ^ other.value)
        raise RuntimeError("Could not binary-xor byte")
        
    def __add__(self, other) -> "Byte":
        if isinstance(other, int):
            return Byte(self.value + other)
        elif isinstance(other, (Address, Byte, Register)):
            return Byte(self.value + other.value)
        raise RuntimeError("Could not add byte")
    
    def __sub__(self, other) -> "Byte":
        if isinstance(other, int):
            return Byte(self.value - other)
        elif isinstance(other, (Address, Byte, Register)):
            return Byte(self.value - other.value)
        raise RuntimeError("Could not subtract byte")
    
    def __mul__(self, other) -> "Byte":
        if isinstance(other, int):
            return Byte(self.value * other)
        elif isinstance(other, (Address, Byte, Register)):
            return Byte(self.value * other.value)
        raise RuntimeError("Could not multiply byte")
    
    def __gt__(self, other) -> bool:
        if isinstance(other, int):
            return self.value > other
        elif isinstance(other, (Address, Byte, Register)):
            return self.value > other.value
        raise RuntimeError("Could not compare byte")

    def __lt__(self, other) -> bool:
        if isinstance(other, int):
            return self.value < other
        elif isinstance(other, (Address, Byte, Register)):
            return self.value < other.value
        raise RuntimeError("Could not compare byte")
    
    def __eq__(self, other) -> bool:
        if isinstance(other, int):
            return self.value == other
        elif isinstance(other, (Address, Byte, Register)):
            return self.value == other.value
        raise RuntimeError("Could not compare byte")
    
    def __ge__(self, other) -> bool:
        if isinstance(other, int):
            return self.value >= other
        elif isinstance(other, (Address, Byte, Register)):
            return self.value >= other.value
        raise RuntimeError("Could not compare byte")
    
    def __floordiv__(self, other) -> "Byte":
        if isinstance(other, int):
            return Byte(self.value // other)
        elif isinstance(other, (Address, Byte, Register)):
            return Byte(self.value // other.value)
        raise RuntimeError("Could not divide byte")
    
    def __mod__(self, other) -> "Byte":
        if isinstance(other, int):
            return Byte(self.value % other)
        elif isinstance(other, (Address, Byte, Register)):
            return Byte(self.value % other.value)
        raise RuntimeError("Could not mod byte")
    
    @classmethod
    def random(cls, rng: Random) -> "Byte":
        return cls(rng.randint(0, 256))
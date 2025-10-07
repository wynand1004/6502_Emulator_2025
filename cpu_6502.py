# 6502 CPU Emulator
# By @TokyoEdtech
# Python Version: 3.12

# REF: http://www.6502.org/tutorials/6502opcodes.html

from enum import Enum, auto

class Mode(Enum):
    IMMEDIATE = auto()
    ABSOLUTE = auto()
    IMPLIED = auto()
    
class CPU:
    
    def __init__(self):
        self.memory = []
        for _ in range(0, 65536):
            self.memory.append(0)
        
        self.a = 0x00
        self.x = 0x00
        self.y = 0x00
        self.pc = 0x1000
        
        self.commands = {
            0xA9: {"f": self.LDA, "m": Mode.IMMEDIATE},
            0xA2: {"f": self.LDX, "m": Mode.IMMEDIATE},
            0xA0: {"f": self.LDY, "m": Mode.IMMEDIATE},
            
            0x8D: {"f": self.STA, "m": Mode.ABSOLUTE},
            0x8E: {"f": self.STX, "m": Mode.ABSOLUTE},
            0x8C: {"f": self.STY, "m": Mode.ABSOLUTE},
            
            0xE8: {"f": self.INX, "m": Mode.IMPLIED},
            0xC8: {"f": self.INY, "m": Mode.IMPLIED},
            0xAA: {"f": self.TAX, "m": Mode.IMPLIED},
            0x8A: {"f": self.TXA, "m": Mode.IMPLIED},
            0xA8: {"f": self.TAY, "m": Mode.IMPLIED},
            0x98: {"f": self.TYA, "m": Mode.IMPLIED},
        }
        
        self.increments = {
            Mode.IMMEDIATE: 2,
            Mode.ABSOLUTE: 3,
            Mode.IMPLIED: 1
        }
        
    def tick(self):
        # fetch command
        command = self.memory[self.pc]
        
        # print(f"{hex(self.pc)}: {command}") 
        
        # execute
        if command in self.commands:
            f = self.commands[command]["f"]
            m = self.commands[command]["m"]
            f(m)
            self.pc += self.increments[m]
        else:
            print(f"Command: {command} not impemented")


    def get_location_by_mode(self, mode):
        loc = 0
        
        if mode == Mode.IMMEDIATE:
            loc = self.pc + 1
            
        elif mode == Mode.ABSOLUTE:
            lsb = self.memory[self.pc+1]
            msb = self.memory[self.pc+2]
            loc = msb * 256 + lsb            
            
        return loc
        

    # LDA
    def LDA(self, mode):
        # Find the location based on the mode
        loc = self.get_location_by_mode(mode)
        # Load value from memory
        val = self.memory[loc]
        # Put that value in the accumulator
        self.a = val
        
    # LDX
    def LDX(self, mode):
        # Find the location based on the mode
        loc = self.get_location_by_mode(mode)
        # Load value from memory
        val = self.memory[loc]
        # Put that value in the accumulator
        self.x = val
        
    # LDY
    def LDY(self, mode):
        # Find the location based on the mode
        loc = self.get_location_by_mode(mode)
        # Load value from memory
        val = self.memory[loc]
        # Put that value in the accumulator
        self.y = val
        
    # STA
    def STA(self, mode):
        # Find the location based on the mode
        loc = self.get_location_by_mode(mode)
        # Update memory
        self.memory[loc] = self.a

    # STX
    def STX(self, mode):
        # Find the location based on the mode
        loc = self.get_location_by_mode(mode)
        # Update memory
        self.memory[loc] = self.x

    # STY
    def STY(self, mode):
        # Find the location based on the mode
        loc = self.get_location_by_mode(mode)
        # Update memory
        self.memory[loc] = self.y
        
    # INX
    def INX(self, mode):
        self.x += 1
    
    # INY
    def INY(self, mode):
        self.y += 1
        
    # DEX
    def INX(self, mode):
        self.x -= 1
    
    # DEY
    def INY(self, mode):
        self.y -= 1
        
    # TAX
    def TAX(self, mode):
        self.x = self.a
        
    # TXA
    def TXA(self, mode):
        self.a = self.x
        
    # TAY
    def TAY(self, mode):
        self.y = self.a
        
    # TYA
    def TYA(self, mode):
        self.a = self.y

# Create CPU object
cpu = CPU()
print(cpu.a)

cpu.memory[0x1000] = 0xA9 # LDA #0x44
cpu.memory[0x1001] = 0x44

cpu.memory[0x1002] = 0xA2 # LDX #0x45
cpu.memory[0x1003] = 0x45

cpu.memory[0x1004] = 0xA0 # LDY #0x46
cpu.memory[0x1005] = 0x46


cpu.memory[0x1006] = 0x8D # STA 0x4400
cpu.memory[0x1007] = 0x00
cpu.memory[0x1008] = 0x44

cpu.memory[0x1009] = 0x8E # STX 0x4401
cpu.memory[0x100A] = 0x01
cpu.memory[0x100B] = 0x44

cpu.memory[0x100C] = 0x8C # STY 0x4402
cpu.memory[0x100D] = 0x02
cpu.memory[0x100E] = 0x44

cpu.memory[0x100F] = 0xE8 # INX
cpu.memory[0x1010] = 0xC8 # INY


for _ in range(100):
    cpu.tick()

print(f"a: {cpu.a}")
print(f"x: {cpu.x}")
print(f"y: {cpu.y}")

print()
print(cpu.memory[0x4400])
print(cpu.memory[0x4401])
print(cpu.memory[0x4402])

print()
print(f"a: {cpu.a}")
print(f"x: {cpu.x}")
print(f"y: {cpu.y}")

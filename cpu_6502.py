# 6502 CPU Emulator
# By @TokyoEdtech
# Python Version: 3.12

# REF: http://www.6502.org/tutorials/6502opcodes.html

from enum import Enum, auto

class Mode(Enum):
    IMMEDIATE = auto()
    ABSOLUTE = auto()
    ZEROPAGE = auto()
    ZEROPAGEX = auto()
    ABSOLUTEX = auto()
    ABSOLUTEY = auto()
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
        
        self.carry = False;
        self.interrupt = False;
        self.overflow = False;
        self.decimal = False;
        
        
        
        self.commands = {
            0x42: {"f": self.print_status, "m": Mode.IMPLIED},
             
            0xA9: {"f": self.LDA, "m": Mode.IMMEDIATE},
            0xA5: {"f": self.LDA, "m": Mode.ZEROPAGE},
            0xB5: {"f": self.LDA, "m": Mode.ZEROPAGEX},
            0xBD: {"f": self.LDA, "m": Mode.ABSOLUTEX},
            0xB9: {"f": self.LDA, "m": Mode.ABSOLUTEY},
            
            
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
            
            0x18: {"f": self.CLC, "m": Mode.IMPLIED},
            0x38: {"f": self.SEC, "m": Mode.IMPLIED},
            0x58: {"f": self.CLI, "m": Mode.IMPLIED},
            0x78: {"f": self.SEI, "m": Mode.IMPLIED},
            0xB8: {"f": self.CLV, "m": Mode.IMPLIED},
            0xD8: {"f": self.CLD, "m": Mode.IMPLIED},
            0xF8: {"f": self.SED, "m": Mode.IMPLIED},
            
        }
        
        self.increments = {
            Mode.IMMEDIATE: 2,
            Mode.ZEROPAGE: 2,
            Mode.ZEROPAGEX: 2,
            Mode.ABSOLUTE: 3,
            Mode.IMPLIED: 1,
            Mode.ABSOLUTEX: 3,
            Mode.ABSOLUTEY: 3
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
        
        elif mode == Mode.ABSOLUTEX:
            lsb = self.memory[self.pc+1]
            msb = self.memory[self.pc+2]
            loc = msb * 256 + lsb 
            loc += self.x
            
        elif mode == Mode.ABSOLUTEY:
            lsb = self.memory[self.pc+1]
            msb = self.memory[self.pc+2]
            loc = msb * 256 + lsb 
            loc += self.y
            
        elif mode == Mode.ZEROPAGE:
            lsb = self.memory[self.pc+1]
            loc = lsb   
            
        elif mode == Mode.ZEROPAGEX:
            lsb = self.memory[self.pc+1]
            loc = lsb + x
            
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
    def DEX(self, mode):
        self.x -= 1
    
    # DEY
    def DEY(self, mode):
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
        
    # CLC
    def CLC(self, mode):
        self.carry = False
        
    # SEC
    def SEC(self, mode):
        self.carry = True
    
    # CLI
    def CLI(self, mode):
        self.interrupt = False
    
    # SEI
    def SEI(self, mode):
        self.interrupt = True
    
    # CLV
    def CLV(self, mode):
        self.overflow = False
    
    # CLD
    def CLD(self, mode):
        self.decimal = False
    
    # SED
    def SED(self, mode):
        self.decimal = True

    # Testing / Debugging
    def push(self, value):
        self.memory[self.pc] = value
        self.pc += 1
        
    def print_status(self, mode):
        print(f"a: {self.a}")
        print(f"x: {self.x}")
        print(f"y: {self.y}")
        print(f"pc: {self.pc}")
        print(f"carry: {self.carry}") 
        print(f"interrupt: {self.interrupt}")
        print(f"overflow: {self.overflow}")
        print(f"decimal: {self.decimal}")
        input()        



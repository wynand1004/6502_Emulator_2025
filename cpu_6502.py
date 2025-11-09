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
    INDIRECT = auto()
    RELATIVE = auto()
    ACCUMULATOR = auto()
    
class CPU:
    
    def __init__(self):
        self.memory = []
        for _ in range(0, 65536):
            self.memory.append(0)
        
        self.a = 0x00
        self.x = 0x00
        self.y = 0x00
        self.pc = 0x1000
        self.sp = 0xFF
        
        self.n = False # N
        self.v = False # V
        self.b = False # B
        self.d = False # D
        self.i = False # I 
        self.z = False # Z
        self.c = False # C
        
        self.commands = {
            0x42: {"f": self.print_status, "m": Mode.IMPLIED},
             
            0xA9: {"f": self.LDA, "m": Mode.IMMEDIATE},
            0xA5: {"f": self.LDA, "m": Mode.ZEROPAGE},
            0xAD: {"f": self.LDA, "m": Mode.ABSOLUTE},
            0xB5: {"f": self.LDA, "m": Mode.ZEROPAGEX},
            0xBD: {"f": self.LDA, "m": Mode.ABSOLUTEX},
            0xB9: {"f": self.LDA, "m": Mode.ABSOLUTEY},
            
            
            0xA2: {"f": self.LDX, "m": Mode.IMMEDIATE},
            0xAE: {"f": self.LDX, "m": Mode.ABSOLUTE},
            
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
            0xCA: {"f": self.DEX, "m": Mode.IMPLIED},
            0x88: {"f": self.DEY, "m": Mode.IMPLIED},
            
            0x18: {"f": self.CLC, "m": Mode.IMPLIED},
            0x38: {"f": self.SEC, "m": Mode.IMPLIED},
            0x58: {"f": self.CLI, "m": Mode.IMPLIED},
            0x78: {"f": self.SEI, "m": Mode.IMPLIED},
            0xB8: {"f": self.CLV, "m": Mode.IMPLIED},
            0xD8: {"f": self.CLD, "m": Mode.IMPLIED},
            0xF8: {"f": self.SED, "m": Mode.IMPLIED},
            
            0x4C: {"f": self.JMP, "m": Mode.ABSOLUTE},
            0x6C: {"f": self.JMP, "m": Mode.INDIRECT},
            
            0xC9: {"f": self.CMP, "m": Mode.IMMEDIATE},
            0xC5: {"f": self.CMP, "m": Mode.ZEROPAGE},
            0xD5: {"f": self.CMP, "m": Mode.ZEROPAGEX},
            0xCD: {"f": self.CMP, "m": Mode.ABSOLUTE},
            0xDD: {"f": self.CMP, "m": Mode.ABSOLUTEX},
            0xD9: {"f": self.CMP, "m": Mode.ABSOLUTEY}, 
            
            0x10: {"f": self.BPL, "m": Mode.RELATIVE},
            0x30: {"f": self.BMI, "m": Mode.RELATIVE}, 
            0x50: {"f": self.BVC, "m": Mode.RELATIVE},
            0x70: {"f": self.BVS, "m": Mode.RELATIVE},
            0x90: {"f": self.BCC, "m": Mode.RELATIVE},
            0xB0: {"f": self.BCS, "m": Mode.RELATIVE},
            0xD0: {"f": self.BNE, "m": Mode.RELATIVE},
            0xF0: {"f": self.BEQ, "m": Mode.RELATIVE},
            
            0x9A: {"f": self.TXS, "m": Mode.IMPLIED},
            0xBA: {"f": self.TSX, "m": Mode.IMPLIED},
            0x48: {"f": self.PHA, "m": Mode.IMPLIED},
            0x68: {"f": self.PLA, "m": Mode.IMPLIED},
            0x08: {"f": self.PHP, "m": Mode.IMPLIED},
            0x28: {"f": self.PLP, "m": Mode.IMPLIED},
            
            0x20: {"f": self.JSR, "m": Mode.ABSOLUTE},
            0x60: {"f": self.RTS, "m": Mode.IMPLIED},
            
            0x69: {"f": self.ADC, "m": Mode.IMMEDIATE},
        
            0x29: {"f": self.AND, "m": Mode.IMMEDIATE},
            
            0x09: {"f": self.ORA, "m": Mode.IMMEDIATE},
            
            0x49: {"f": self.EOR, "m": Mode.IMMEDIATE},
            
            0xE9: {"f": self.SBC, "m": Mode.IMMEDIATE},
            
            0xEA: {"f": self.NOP, "m": Mode.IMPLIED},
            
            0x0A: {"f": self.ASL, "m": Mode.ACCUMULATOR},
            
            0x4A: {"f": self.LSR, "m": Mode.ACCUMULATOR},
            
            0x2A: {"f": self.ROL, "m": Mode.ACCUMULATOR},
            
            0x6A: {"f": self.ROR, "m": Mode.ACCUMULATOR},
            
            0xE0: {"f": self.CPX, "m": Mode.IMMEDIATE},
            0xE4: {"f": self.CPX, "m": Mode.ZEROPAGE},
            0xEC: {"f": self.CPX, "m": Mode.ABSOLUTE},
            
            0xC0: {"f": self.CPY, "m": Mode.IMMEDIATE},
            0xC4: {"f": self.CPY, "m": Mode.ZEROPAGE},
            0xCC: {"f": self.CPY, "m": Mode.ABSOLUTE},
            
            0xE6: {"f": self.INC, "m": Mode.ZEROPAGE},
            0xF6: {"f": self.INC, "m": Mode.ZEROPAGEX},
            0xEE: {"f": self.INC, "m": Mode.ABSOLUTE},
            0xFE: {"f": self.INC, "m": Mode.ABSOLUTEX},
            
            0xC6: {"f": self.DEC, "m": Mode.ZEROPAGE},
            0xD6: {"f": self.DEC, "m": Mode.ZEROPAGEX},
            0xCE: {"f": self.DEC, "m": Mode.ABSOLUTE},
            0xDE: {"f": self.DEC, "m": Mode.ABSOLUTEX},
            
            
            
        }

        self.increments = {
            Mode.IMMEDIATE: 2,
            Mode.ZEROPAGE: 2,
            Mode.ZEROPAGEX: 2,
            Mode.ABSOLUTE: 3,
            Mode.IMPLIED: 1,
            Mode.ABSOLUTEX: 3,
            Mode.ABSOLUTEY: 3,
            Mode.INDIRECT: 3,
            Mode.RELATIVE: 2,
            Mode.ACCUMULATOR: 1
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
            print(f"Command: {command} not impemented at location {hex(self.pc)}")
            input()

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
            
        elif mode == Mode.INDIRECT:
            # Get the memory location where the JMP address is
            lsb = self.memory[self.pc+1]
            msb = self.memory[self.pc+2]
            loc = msb * 256 + lsb 
            
            # Get the JMP address from the memory location
            lsb = self.memory[loc]
            msb = self.memory[loc + 1]
            loc = msb * 256 + lsb
            
        elif mode == Mode.RELATIVE:
            loc = self.pc + 1
            
        return loc

    # Wrap 8 bit values
    def wrap(self, value):
        if value > 255:
            value = value % 256;
        if value < 0:
            value += 256
        return value

    def set_nz(self, value):
        self.z = (value == 0)
        self.n = bool(value & 0x80)

    # LDA
    def LDA(self, mode):
        # Find the location based on the mode
        loc = self.get_location_by_mode(mode)
        # Load value from memory
        val = self.memory[loc]
        # Put that value in the accumulator
        self.a = val
        # Set nz
        self.set_nz(self.a)
        
    # LDX
    def LDX(self, mode):
        # Find the location based on the mode
        loc = self.get_location_by_mode(mode)
        # Load value from memory
        val = self.memory[loc]
        # Put that value in the accumulator
        self.x = val
        # Set nz
        self.set_nz(self.x)
        
    # LDY
    def LDY(self, mode):
        # Find the location based on the mode
        loc = self.get_location_by_mode(mode)
        # Load value from memory
        val = self.memory[loc]
        # Put that value in the accumulator
        self.y = val
        # Set nz
        self.set_nz(self.y)
        
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
       
    # INC
    def INC(self, mode):
        # Find the location based on the mode
        loc = self.get_location_by_mode(mode)
        value = self.memory[loc]

        value += 1
        value = self.wrap(value)
        self.memory[loc] = value
        
        # Set nz
        self.set_nz(value)        
        

    # INX
    def INX(self, mode):
        self.x += 1
        self.x = self.wrap(self.x)
        # Set nz
        self.set_nz(self.x)
    
    # INY
    def INY(self, mode):
        self.y += 1
        self.y = self.wrap(self.y)
        # Set nz
        self.set_nz(self.y)
    
    # DEC
    def DEC(self, mode):
        # Find the location based on the mode
        loc = self.get_location_by_mode(mode)
        value = self.memory[loc]

        value -= 1
        value = self.wrap(value)
        self.memory[loc] = value
        
        # Set nz
        self.set_nz(value) 
        
    # DEX
    def DEX(self, mode):
        self.x -= 1
        self.x = self.wrap(self.x)
        # Set nz
        self.set_nz(self.x)
    
    # DEY
    def DEY(self, mode):
        self.y -= 1
        self.y = self.wrap(self.y)
        # Set nz
        self.set_nz(self.y)
        
    # TAX
    def TAX(self, mode):
        self.x = self.a
        # Set nz
        self.set_nz(self.x)
        
    # TXA
    def TXA(self, mode):
        self.a = self.x
        # Set nz
        self.set_nz(self.a)
        
    # TAY
    def TAY(self, mode):
        self.y = self.a
        # Set nz
        self.set_nz(self.y)
        
    # TYA
    def TYA(self, mode):
        self.a = self.y
        # Set nz
        self.set_nz(self.a)
        
    # CLC
    def CLC(self, mode):
        self.c = False
        
    # SEC
    def SEC(self, mode):
        self.c = True
    
    # CLI
    def CLI(self, mode):
        self.i = False
    
    # SEI
    def SEI(self, mode):
        self.i = True
    
    # CLV
    def CLV(self, mode):
        self.v = False
    
    # CLD
    def CLD(self, mode):
        self.d = False
    
    # SED
    def SED(self, mode):
        self.d = True
        
    # JMP
    def JMP(self, mode):
        # Find the location based on the mode
        loc = self.get_location_by_mode(mode)
        # Set pc to loc
        self.pc = loc - self.increments[mode]
        
    # CMP
    def CMP(self, mode):
        # Find the location based on the mode
        loc = self.get_location_by_mode(mode)
        value = self.memory[loc]
        
        # Set Carry if >= a
        if value >= self.a:
            self.c = True
            
        if value == self.a:
            self.z = True
        
        if self.a >= 128:
            self.n = True
    
    # CPX
    def CPX(self, mode):
        # Find the location based on the mode
        loc = self.get_location_by_mode(mode)
        value = self.memory[loc]
        
        # Set Carry if >= x
        if value >= self.x:
            self.c = True
            
        if value == self.x:
            self.z = True
        
        if self.x >= 128:
            self.n = True
    
    # CPY
    def CPY(self, mode):
        # Find the location based on the mode
        loc = self.get_location_by_mode(mode)
        value = self.memory[loc]
        
        # Set Carry if >= y
        if value >= self.y:
            self.c = True
            
        if value == self.y:
            self.z = True
        
        if self.y >= 128:
            self.n = True

            
    #BMI
    def BMI(self, mode):
        # Find the location based on the mode
        loc = self.get_location_by_mode(mode)
        value = self.memory[loc]
        
        # Jump to the offset
        if self.n == True:
            # Recalculate if negative
            if value >= 128:
                value -= 256
                
            self.pc = self.pc + value
            
    # BPL
    def BPL(self, mode):
        # Find the location based on the mode
        loc = self.get_location_by_mode(mode)
        value = self.memory[loc]
        
        # Jump to the offset
        if self.n == False:
            # Recalculate if negative
            if value >= 128:
                value -= 256
                
            self.pc = self.pc + value
                
    # BVC
    def BVC(self, mode):
        # Find the location based on the mode
        loc = self.get_location_by_mode(mode)
        value = self.memory[loc]
        
        # Jump to the offset
        if self.v == True:
            # Recalculate if negative
            if value >= 128:
                value -= 256
                
            self.pc = self.pc + value
                
    # BVS
    def BVS(self, mode):
        # Find the location based on the mode
        loc = self.get_location_by_mode(mode)
        value = self.memory[loc]
        
        # Jump to the offset
        if self.v == False:
            # Recalculate if negative
            if value >= 128:
                value -= 256
                
            self.pc = self.pc + value
                
    # BCC
    def BCC(self, mode):
        # Find the location based on the mode
        loc = self.get_location_by_mode(mode)
        value = self.memory[loc]
        
        # Jump to the offset
        if self.c == False:
            # Recalculate if negative
            if value >= 128:
                value -= 256
                
            self.pc = self.pc + value
                
    # BCS
    def BCS(self, mode):
        # Find the location based on the mode
        loc = self.get_location_by_mode(mode)
        value = self.memory[loc]
        
        # Jump to the offset
        if self.c == True:
            # Recalculate if negative
            if value >= 128:
                value -= 256
                
            self.pc = self.pc + value
                
    # BNE
    def BNE(self, mode):
        # Find the location based on the mode
        loc = self.get_location_by_mode(mode)
        value = self.memory[loc]
        
        # Jump to the offset
        if self.z == False:
            # Recalculate if negative
            if value >= 128:
                value -= 256
                
            self.pc = self.pc + value    
    
    # BEQ
    def BEQ(self, mode):
        # Find the location based on the mode
        loc = self.get_location_by_mode(mode)
        value = self.memory[loc]
        
        # Jump to the offset
        if self.z == True:
            # Recalculate if negative
            if value >= 128:
                value -= 256
                
            self.pc = self.pc + value

    # TXS
    def TXS(self, mode):
        self.sp = self.x
        
    # TXA
    def TSX(self, mode):
        sefl.x = self.sp
        # Set nz
        self.set_nz(self.x)
        
    # PHA
    def PHA(self, mode):
        # Find the location
        loc = 0x0100 + self.sp
        
        # Copy from the accumulator
        self.memory[loc] = self.a
        
        # Decrement the stack pointer
        self.sp -= 1
        
        # Wrap
        self.sp = self.wrap(self.sp)

    # PLA
    def PLA(self, mode):
        # Increment the Stack Pointer
        self.sp += 1
        
        # Wrap
        self.sp = self.wrap(self.sp)
        
        # Find the location
        loc = 0x100 + self.sp
        
        # Copy the value to the Accumulator
        self.a = self.memory[loc]
        
        # Set nz
        self.set_nz(self.a)
    
    # PHP
    def PHP(self, mode):
        # nvb1dizc
        val = 0
        if self.n == True:
            val += 128
        if self.v == True:
            val += 64
        if self.b == True:
            val += 32
        val += 16
        if self.d == True:
            val += 8
        if self.i == True:
            val += 4
        if self.z == True:
            val += 2
        if self.c == True:
            val += 1

        # Find the location
        loc = 0x100 + self.sp
        
        # Copy from the accumulator
        self.memory[loc] = val
        
        # Decrement the stack pointer
        self.sp -= 1
        
        # Wrap
        self.sp = self.wrap(self.sp)

    # PLP
    def PLP(self, mode):
        # Increment the Stack Pointer
        self.sp += 1
        
        # Wrap
        self.sp = self.wrap(self.sp)
        
        # Find the location
        loc = 0x100 + self.sp
        
        # Find the value
        val = self.memory[loc]
        
        # Decode value and update flags
        if val & 128 == 128:
            self.n = True
        else:
            self.n = False
            
        if val & 64 == 64:
            self.v = True
        else:
            self.v = False
            
        if val & 32 == 32:
            self.b = True
        else:
            self.b = False
            
        if val & 8 == 8:
            self.d = True
        else:
            self.d = False
            
        if val & 4 == 4:
            self.i = True
        else:
            self.i = False
            
        if val & 2 == 2:
            self.z = True
        else:
            self.z = False
            
        if val & 1 == 1:
            self.c = True
        else:
            self.c = False
            
            
    # JSR
    def JSR(self, mode):
        # Return location (-1)
        loc = self.pc + 2
        
        msb = loc % 256
        lsb = loc - (msb * 256)
        
        # Copy value from accumulator
        temp_a = self.a
        
        # Push onto stack
        self.a = msb
        self.PHA(mode)
        
        self.a = lsb
        self.PHA(mode)
        
        # Copy temp back to a
        self.a = temp_a
        
        # Change program counter to new location
        # Find the location based on the mode
        loc = self.get_location_by_mode(mode)
        
        # Set pc to loc
        self.pc = loc - self.increments[mode]
        
    # RTS
    def RTS(self, mode):
        # Copy a value to temp
        temp_a = self.a
        
        # Pull the lsb
        self.PLA(mode)
        lsb = self.a
        
        # Pull the msb
        self.PLA(mode)
        msb = self.a
        
        # Restore temp to a
        self.a = temp_a
        
        # Set PC to return address
        loc = msb * 256 + lsb
        self.pc = loc

    # ADC
    def ADC(self, mode):
        # Find the location based on the mode
        loc = self.get_location_by_mode(mode)
        
        # Get the value
        value = self.memory[loc]
        
        # Add value to the accumulator
        self.a += value
        
        # If the carry flag is set, add 1
        if self.c == True:
            self.a += 1
        
        # Carry and Wrap around
        if self.a > 255:
            self.c = True
            self.a = self.wrap(self.a)
        else:
            self.c = False
            
        # Set nz
        self.set_nz(self.a)
            
    def SBC(self, mode):
        # Find the location based on the mode
        loc = self.get_location_by_mode(mode)
        
        # Get the value
        value = self.memory[loc]
        
        # Subtract value from accumulator
        self.a -= value

        # Check carry flag
        if self.c == False:
            self.a -= 1
            
        if self.a < 0:
            self.a = self.wrap(self.a)
            
            if self.c == True:
                self.c = False
            else:
                self.c = True
                
        # Set nz
        self.set_nz(self.a)

    def AND(self, mode):
        # Find the location based on the mode
        loc = self.get_location_by_mode(mode)
        
        # Get the value
        value = self.memory[loc]
        
        # Perform logial AND
        self.a = self.a & value
        
        # Set nz
        self.set_nz(self.a)
        
    def ORA(self, mode):
        # Find the location based on the mode
        loc = self.get_location_by_mode(mode)
        
        # Get the value
        value = self.memory[loc]
        
        # Perform logial AND
        self.a = self.a | value
        
        # Set nz
        self.set_nz(self.a)
        
    def EOR(self, mode):
        # Find the location based on the mode
        loc = self.get_location_by_mode(mode)
        
        # Get the value
        value = self.memory[loc]
        
        # Perform logial AND
        self.a = self.a ^ value
        
        # Set nz
        self.set_nz(self.a)

    def NOP(self, mode):
        pass
        
    def ASL(self, mode):
        if mode == Mode.ACCUMULATOR:
            value = self.a
        else:
            # Find the location based on the mode
            loc = self.get_location_by_mode(mode)
        
            # Get the value
            value = self.memory[loc]
            
        # Check the leftmost bit
        if value & 128 == 128:
            self.c = True
        else:
            self.c = False
        
        # Shift Left
        value = value << 1
        
        # Wrap
        value = self.wrap(value)
        
        # Put the value into Accumulator or memory
        if mode == Mode.ACCUMULATOR:
            self.a = value
        else:
            self.memory[loc] = value
            
        # Set nz
        self.set_nz(value)
            
    def LSR(self, mode):
        if mode == Mode.ACCUMULATOR:
            value = self.a
        else:
            # Find the location based on the mode
            loc = self.get_location_by_mode(mode)
        
            # Get the value
            value = self.memory[loc]
            
        # Check the rightmost bit
        if value & 1 == 1:
            self.c = True
        else:
            self.c = False
        
        # Shift Left
        value = value >> 1
        
        # Wrap
        value = self.wrap(value)
        
        # Put the value into Accumulator or memory
        if mode == Mode.ACCUMULATOR:
            self.a = value
        else:
            self.memory[loc] = value
            
        # Set nz
        self.set_nz(value)

    def ROL(self, mode):
        if mode == Mode.ACCUMULATOR:
            value = self.a
        else:
            # Find the location based on the mode
            loc = self.get_location_by_mode(mode)
        
            # Get the value
            value = self.memory[loc]
            
        # Check carry bit
        temp = 0
        if self.c == True:
            temp = 1
            
        # Check the leftmost bit
        if value & 128 == 128:
            self.c = True
        else:
            self.c = False
        
        # Shift Left
        value = value << 1
        
        # Wrap
        value = self.wrap(value)
        
        # Add the carry
        value = value | temp
        
        # Put the value into Accumulator or memory
        if mode == Mode.ACCUMULATOR:
            self.a = value
        else:
            self.memory[loc] = value
            
        # Set nz
        self.set_nz(value)

    def ROR(self, mode):
        if mode == Mode.ACCUMULATOR:
            value = self.a
        else:
            # Find the location based on the mode
            loc = self.get_location_by_mode(mode)
        
            # Get the value
            value = self.memory[loc]
            
        # Check carry bit
        temp = 0
        if self.c == True:
            temp = 128
            
        # Check the rightmost bit
        if value & 1 == 1:
            self.c = True
        else:
            self.c = False
        
        # Shift Right
        value = value >> 1
        
        # Wrap
        value = self.wrap(value)
        
        # Add the carry
        value = value | temp
        
        # Put the value into Accumulator or memory
        if mode == Mode.ACCUMULATOR:
            self.a = value
        else:
            self.memory[loc] = value
            
        # Set nz
        self.set_nz(value)


    # Testing / Debugging
    def push(self, value):
        self.memory[self.pc] = value
        self.pc += 1
        
    def print_status(self, mode):
        print(f"a: {self.a}")
        print(f"x: {self.x}")
        print(f"y: {self.y}")
        print(f"pc: {self.pc}  sp: {self.sp}")
        print(f"n v b d i z c")
        print(f"{int(self.n)} {int(self.v)} {int(self.b)} {int(self.d)} {int(self.i)} {int(self.z)} {int(self.c)}")
        input()        



# 6502 CPU Emulator
# By @TokyoEdtech
# Python Version: 3.12

# REF: http://www.6502.org/tutorials/6502opcodes.html

class CPU:
    
    def __init__(self):
        self.memory = []
        for _ in range(0, 65536):
            self.memory.append(0)
        
        self.a = 0x00
        self.x = 0x00
        self.y = 0x00
        self.pc = 0x1000
        
    def tick(self):
        # fetch command
        command = self.memory[self.pc]
        
        print(f"{hex(self.pc)}: {command}") 
        
        # execute
        if command == 0xA9:
            self.LDA(0)
            self.pc += 2
            
        if command == 0xA2:
            self.LDX(0)
            self.pc += 2
            
        if command == 0xA0:
            self.LDY(0)
            self.pc += 2
            
        if command == 0x8D:
            self.STA(1)
            self.pc += 3
            
        if command == 0x8E:
            self.STX(1)
            self.pc += 3
            
        if command == 0x8C:
            self.STY(1)
            self.pc += 3

        
    # LDA
    def LDA(self, mode):
        # Load value from memory
        val = self.memory[self.pc+1]
        # Put that value in the accumulator
        self.a = val
        
    # LDX
    def LDX(self, mode):
        # Load value from memory
        val = self.memory[self.pc+1]
        # Put that value in the accumulator
        self.x = val
        
    # LDY
    def LDY(self, mode):
        # Load value from memory
        val = self.memory[self.pc+1]
        # Put that value in the accumulator
        self.y = val
        
    # STA
    def STA(self, mode):
        lsb = self.memory[self.pc+1]
        msb = self.memory[self.pc+2]
        loc = msb * 256 + lsb
        
        self.memory[loc] = self.a

    # STX
    def STX(self, mode):
        lsb = self.memory[self.pc+1]
        msb = self.memory[self.pc+2]
        loc = msb * 256 + lsb
        
        self.memory[loc] = self.x

    # STY
    def STY(self, mode):
        lsb = self.memory[self.pc+1]
        msb = self.memory[self.pc+2]
        loc = msb * 256 + lsb
        
        self.memory[loc] = self.y

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

for _ in range(100):
    cpu.tick()

print(cpu.a)
print(cpu.x)
print(cpu.y)

print()
print(cpu.memory[0x4400])
print(cpu.memory[0x4401])
print(cpu.memory[0x4402])

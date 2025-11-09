# 6502 CPU System
# By @TokyoEdtech
# Python Version: 3.12

from cpu_6502 import *

# Create CPU object
cpu = CPU()
print(cpu.a)

cpu.pc = 0x1000

cpu.push(0xA2) # LDX #
cpu.push(0x01) 

cpu.push(0xE0) # CPX #
cpu.push(0x00)

cpu.push(0x42) # DBG

# LDY #
cpu.push(0xA0) 
cpu.push(0x01) 

cpu.push(0xC0) # CPY #
cpu.push(0x01)

cpu.push(0x42) # DBG

cpu.push(0xA9) # LDA #XX
cpu.push(0x01)

cpu.push(0x8D) # STA $4400
cpu.push(0x00)
cpu.push(0x44)

cpu.push(0x42) # DBG

cpu.push(0xCE) # DEC $4400
cpu.push(0x00)
cpu.push(0x44)

cpu.push(0xAD) # LDA $4400
cpu.push(0x00)
cpu.push(0x44)

cpu.push(0x42) # DBG

cpu.push(0xEE) # INC $4400
cpu.push(0x00)
cpu.push(0x44)

cpu.push(0xAD) # LDA $4400
cpu.push(0x00)
cpu.push(0x44)

cpu.push(0x42) # DBG

cpu.pc = 0x1000

for _ in range(30):
    cpu.tick()




print()
print(cpu.memory[0x4400])
print(cpu.memory[0x4401])
print(cpu.memory[0x4402])


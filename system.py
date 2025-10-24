# 6502 CPU System
# By @TokyoEdtech
# Python Version: 3.12

from cpu_6502 import *

# Create CPU object
cpu = CPU()
print(cpu.a)

cpu.pc = 0x1000

cpu.push(0xA2) # LDX #0xFF
cpu.push(0xFF) 

cpu.push(0x42) # DBG

cpu.push(0xA9) # LDA #0x90
cpu.push(0x90) 

cpu.push(0xC9) # CMP #0x01
cpu.push(0x01)

cpu.push(0x42) # DBG

cpu.push(0xF0) # BEQ LDX #0xFF
cpu.push(0xF6)

cpu.push(0xA2) # LDX #0x01
cpu.push(0x01) 

cpu.push(0x42) # DBG

cpu.pc = 0x1003

for _ in range(30):
    cpu.tick()




print()
print(cpu.memory[0x4400])
print(cpu.memory[0x4401])
print(cpu.memory[0x4402])


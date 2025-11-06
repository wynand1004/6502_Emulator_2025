# 6502 CPU System
# By @TokyoEdtech
# Python Version: 3.12

from cpu_6502 import *

# Create CPU object
cpu = CPU()
print(cpu.a)

cpu.pc = 0x1000

# N and Z Flags
cpu.push(0xA9) # LDA #0xXX
cpu.push(0xFF)

cpu.push(0x42)

cpu.pc = 0x1000

for _ in range(30):
    cpu.tick()




print()
print(cpu.memory[0x4400])
print(cpu.memory[0x4401])
print(cpu.memory[0x4402])


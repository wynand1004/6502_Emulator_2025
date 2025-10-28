# 6502 CPU System
# By @TokyoEdtech
# Python Version: 3.12

from cpu_6502 import *

# Create CPU object
cpu = CPU()
print(cpu.a)

cpu.pc = 0x1000

# AND / OR / EOR

cpu.push(0xA9) # LDA #0x01
cpu.push(0x01)

cpu.push(0x42) # DBG

cpu.push(0x09) # ORA #XX
cpu.push(0x04)

cpu.push(0x42) # DBG

cpu.pc = 0x1000

for _ in range(30):
    cpu.tick()




print()
print(cpu.memory[0x4400])
print(cpu.memory[0x4401])
print(cpu.memory[0x4402])


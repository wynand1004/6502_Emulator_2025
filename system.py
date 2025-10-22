# 6502 CPU System
# By @TokyoEdtech
# Python Version: 3.12

from cpu_6502 import *

# Create CPU object
cpu = CPU()
print(cpu.a)

cpu.pc = 0x1000

cpu.push(0xA9) # LDA #0x0D LSB 0x100D
cpu.push(0x0D)

cpu.push(0x8D) # STA 0x2000
cpu.push(0x00)
cpu.push(0x20)

cpu.push(0xA9) # LDA #0x10 MSB 0x100D
cpu.push(0x10)

cpu.push(0x8D) # STA 0x2001
cpu.push(0x01)
cpu.push(0x20)

cpu.push(0xA9) # LDA #0x02
cpu.push(0x02)

cpu.push(0xAA) # TAX
cpu.push(0xCA) # DEX LOC 0x100D

cpu.push(0x42) # DBG
cpu.push(0x6C) # JMP 0x2000
cpu.push(0x00)
cpu.push(0x20)
 

cpu.pc = 0x1000

for _ in range(30):
    cpu.tick()




print()
print(cpu.memory[0x4400])
print(cpu.memory[0x4401])
print(cpu.memory[0x4402])


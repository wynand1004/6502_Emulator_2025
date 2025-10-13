# 6502 CPU System
# By @TokyoEdtech
# Python Version: 3.12

from cpu_6502 import *

# Create CPU object
cpu = CPU()
print(cpu.a)

cpu.pc = 0x1000

cpu.push(0xA9) # LDA #0x0A
cpu.push(0x0A)

cpu.push(0x42) # DBG

cpu.push(0x8D) # STA 0x4401
cpu.push(0x01)
cpu.push(0x44)

cpu.push(0x42) # DBG

cpu.push(0xA2) # LDX #0x01
cpu.push(0x01)

cpu.push(0xBD) # LDA 0x4400, X
cpu.push(0x00)
cpu.push(0x44)

cpu.push(0x42) # DBG

cpu.push(0xA5) # LDA 0x55
cpu.push(0x55) 

cpu.push(0x42) # DBG

# Test flags
cpu.push(0x38) # SEC
cpu.push(0x42) # DBG


cpu.push(0x78) # SEI
cpu.push(0x42) # DBG


cpu.push(0xF8) # SED
cpu.push(0x42) # DBG


cpu.pc = 0x1000

for _ in range(100):
    cpu.tick()




print()
print(cpu.memory[0x4400])
print(cpu.memory[0x4401])
print(cpu.memory[0x4402])


# 6502 CPU System
# By @TokyoEdtech
# Python Version: 3.12

from cpu_6502 import *

# Create CPU object
cpu = CPU()
print(cpu.a)

cpu.pc = 0x1000

# JSR / RTS

cpu.push(0x20) # JSR $1008
cpu.push(0x08)
cpu.push(0x10)

cpu.push(0x42) # DBG

cpu.push(0xA0) # LDY #$02
cpu.push(0x02)

cpu.push(0x42) # DBG

cpu.push(0) # HALT ON ERROR

cpu.push(0xA2) # LDX #$01
cpu.push(0x01)

cpu.push(0x42)

cpu.push(0x60) # RTS

cpu.pc = 0x1000

for _ in range(30):
    cpu.tick()




print()
print(cpu.memory[0x4400])
print(cpu.memory[0x4401])
print(cpu.memory[0x4402])


import sys
from amaranth import *

from memory import Memory
from cpu import CPU

class SOC(Elaboratable):

    def __init__(self):

        self.leds = Signal(5)

        # Signals in this list can easily be plotted as vcd traces
        self.ports = []

    def elaborate(self, platform):

        m = Module()

        memory = Memory()
        cpu = CPU()

        m.submodules.cpu = cpu
        m.submodules.memory = memory

        self.cpu = cpu
        self.memory = memory

        x10 = Signal(32)

        # Connect memory to CPU
        m.d.comb += [
            memory.mem_addr.eq(cpu.mem_addr),
            memory.mem_rstrb.eq(cpu.mem_rstrb),
            cpu.mem_rdata.eq(memory.mem_rdata)
        ]

        # CPU debug output
        m.d.comb += [
            x10.eq(cpu.x10),
            self.leds.eq(x10[0:5])
        ]

        return m

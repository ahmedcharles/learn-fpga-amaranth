from amaranth import *
from amaranth.lib import memory

from clockworks import Clockworks

class SOC(Elaboratable):

    def __init__(self):

        self.leds = Signal(5)

    def elaborate(self, platform):

        m = Module()

        cw = Clockworks(slow=21)

        m.domains += ClockDomain(cw.domain_name)

        m.submodules.cw = cw

        sequence = [
                0b00001,
                0b00010,
                0b00100,
                0b01000,
                0b10000,
                0b10001,
                0b10010,
                0b10100,
                0b11000,
                0b00000,
        ]

        pc = Signal(range(len(sequence)), reset=0)
        m.submodules.mem = mem = DomainRenamer(cw.domain_name)(memory.Memory(
            shape=unsigned(32),
            depth=len(sequence),
            init=sequence,
            attrs={"ram_style": "block"},
        ))
        rd = mem.read_port()
        rd_en = Signal(reset=0)
        prev_rd_en = Signal(reset=0)

        m.d.slow += [
            rd_en.eq(1),
            prev_rd_en.eq(rd_en),
            pc.eq(Mux((pc == len(sequence) - 1) | ~rd_en, 0, pc + 1)),
        ]
        m.d.comb += [
            rd.en.eq(rd_en),
            rd.addr.eq(pc),
            self.leds.eq(Mux(prev_rd_en, rd.data, ~0)),
        ]

        return m

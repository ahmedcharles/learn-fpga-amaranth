from amaranth import ClockSignal, Elaboratable, Signal, Module
from amaranth.lib import wiring
from amaranth.lib.wiring import In, Out

# This module handles clock division and provides a new 'slow' clock domain

class Clockworks(Elaboratable):

    def __init__(self, slow=0, sim_slow=None):
        self.domain_name = "slow"

        self.slow = slow
        if slow == 0:
            self.sim_slow = 0
        elif sim_slow is None:
            self.sim_slow = 10
        else:
            self.sim_slow = sim_slow

        super().__init__()

    def elaborate(self, platform):

        o_clk = Signal()
        m = Module()

        if self.slow != 0:
            # When the design is simulated, platform is None
            if platform is None:
                # Have the simulation run at a different speed than the
                # actual hardware (usually faster).
                slow_bit = self.sim_slow
            else:
                slow_bit = self.slow

            slow_clk = Signal(slow_bit + 1)
            m.d.sync += slow_clk.eq(slow_clk + 1)
            m.d.comb += o_clk.eq(slow_clk[slow_bit])

        else:
            # When no division is requested, just use the clock signal of
            # the default 'sync' domain.
            m.d.comb += o_clk.eq(ClockSignal("sync"))

        # Assign the slow clock to the clock signal of the new domain
        m.d.comb += ClockSignal("slow").eq(o_clk)

        return m

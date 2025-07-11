from amaranth import *
from amaranth.sim import *

from soc import SOC

soc = SOC()

prev_clk = 0

async def testbench(ctx):
    while True:
        global prev_clk
        clk = ctx.get(soc.slow_clk)
        if prev_clk == 0 and prev_clk != clk:
            state = ctx.get(soc.state)
            if state == 2:
                print("-- NEW CYCLE -----------------------")
                print("  F: LEDS = {:05b}".format(ctx.get(soc.leds)))
                print("  F: pc={}".format(ctx.get(soc.pc)))
                print("  F: instr={:#032b}".format(ctx.get(soc.instr)))
                if ctx.get(soc.isALUreg):
                    print("     ALUreg rd={} rs1={} rs2={} funct3={}".format(
                        ctx.get(soc.rdId), ctx.get(soc.rs1Id), ctx.get(soc.rs2Id),
                        ctx.get(soc.funct3)))
                if ctx.get(soc.isALUimm):
                    print("     ALUimm rd={} rs1={} imm={} funct3={}".format(
                        ctx.get(soc.rdId), ctx.get(soc.rs1Id), ctx.get(soc.Iimm),
                        ctx.get(soc.funct3)))
                if ctx.get(soc.isBranch):
                    print("    BRANCH rs1={} rs2={}".format(
                        ctx.get(soc.rs1Id), ctx.get(soc.rs2Id)))
                if ctx.get(soc.isLoad):
                    print("    LOAD")
                if ctx.get(soc.isStore):
                    print("    STORE")
                if ctx.get(soc.isSystem):
                    print("    SYSTEM")
                    break
            if state == 4:
                print("  R: LEDS = {:05b}".format(ctx.get(soc.leds)))
                print("  R: rs1={}".format(ctx.get(soc.rs1)))
                print("  R: rs2={}".format(ctx.get(soc.rs2)))
            if state == 1:
                print("  E: LEDS = {:05b}".format(ctx.get(soc.leds)))
                print("  E: Writeback x{} = {:032b}".format(ctx.get(soc.rdId),
                                             ctx.get(soc.writeBackData)))
        await ctx.tick()
        prev_clk = clk

sim = Simulator(soc)
sim.add_clock(1e-6)
sim.add_testbench(testbench)

with sim.write_vcd('bench.vcd', 'bench.gtkw', traces=soc.ports):
    # Let's run for a quite long time
    sim.run_until(2)

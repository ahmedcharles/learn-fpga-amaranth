from amaranth import *
from amaranth.sim import *

from soc import SOC

soc = SOC()

prev_pc = 0

async def testbench(ctx):
    while True:
        global prev_pc
        pc = ctx.get(soc.pc)
        if prev_pc != pc:
            print("pc={}".format(pc))
            print("instr={:#032b}".format(ctx.get(soc.instr)))
            print("LEDS = {:05b}".format(ctx.get(soc.leds)))
            if ctx.get(soc.isALUreg):
                print("ALUreg rd={} rs1={} rs2={} funct3={}".format(
                    ctx.get(soc.rdId), ctx.get(soc.rs1Id), ctx.get(soc.rs2Id),
                    ctx.get(soc.funct3)))
            if ctx.get(soc.isALUimm):
                print("ALUimm rd={} rs1={} imm={} funct3={}".format(
                    ctx.get(soc.rdId), ctx.get(soc.rs1Id), ctx.get(soc.Iimm),
                    ctx.get(soc.funct3)))
            if ctx.get(soc.isLoad):
                print("LOAD rd={} rs1={} imm={} funct3={}".format(
                    ctx.get(soc.rdId), ctx.get(soc.rs1Id), ctx.get(soc.Iimm),
                    ctx.get(soc.funct3)))
            if ctx.get(soc.isStore):
                print("STORE rs1={} rs2={} imm={} funct3={}".format(
                    ctx.get(soc.rs1Id), ctx.get(soc.rs2Id), ctx.get(soc.Iimm),
                    ctx.get(soc.funct3)))
            if ctx.get(soc.isSystem):
                print("SYSTEM rd={} rs1={} imm={} funct3={}".format(
                    ctx.get(soc.rdId), ctx.get(soc.rs1Id), ctx.get(soc.Iimm),
                    ctx.get(soc.funct3)))
                break
        await ctx.tick()
        prev_pc = pc

sim = Simulator(soc)
sim.add_clock(1e-6)
sim.add_testbench(testbench)

with sim.write_vcd('bench.vcd', 'bench.gtkw', traces=soc.ports):
    # Let's run for a quite long time
    sim.run_until(2)

"""
# Mos Transistor Characterization
"""

import hdl21 as h
from hdl21.prefix import u
from hdl21.pdk import sample_pdk as pdk
from dataclasses import dataclass


@dataclass
class AcDc:
    dc: h.Scalar
    ac: h.Scalar


def sim(my_nmos: h.Module, vgsp: AcDc, vdsp: AcDc) -> h.sim.Sim:
    @h.module
    class Tb:
        """# Mos Char Testbench"""

        VSS = h.Port()  # The testbench interface: sole port VSS

        vds = h.Vdc(dc=vdsp.dc, ac=vdsp.ac)(n=VSS)
        vgs = h.Vdc(dc=vgsp.dc, ac=vgsp.ac)(n=VSS)

        # The transistor under test
        mn = my_nmos(d=vds.p, g=vgs.p, s=VSS, b=VSS)

    @h.sim.sim
    class Sim:
        tb = Tb

        op = h.sim.Op()
        ac = h.sim.Ac(sweep=h.sim.LogSweep(start=1, stop=2, npts=2))
        mod = h.sim.Include(pdk.install.models)  # Include the Models

    Sim.attrs.append(h.Literal("// AAAAAHHHHH!!!!!!"))

    return Sim


# Simulation runtime options
opts = h.sim.SimOptions(
    simulator=h.sim.SupportedSimulators.SPECTRE,  # Use Spectre, the PDK's sole supported simulator
    fmt=h.sim.ResultFormat.SIM_DATA,  # Get Python-native result types
    rundir="/tmp/camp/mos_char",  # Set the working directory for the simulation. Uses a temporary directory by default.
)


def get_the_gain(my_nmos: h.Module) -> float:
    # Do a sim with vgs stimulated, get gm
    s = sim(my_nmos, vgsp=AcDc(dc=3.3, ac=1), vdsp=AcDc(dc=3.3, ac=0))
    results = s.run(opts=opts)
    acres = results["ac"]
    gm = abs(acres.data["xtop.vds:p"][0])

    # Do another sim with vds stimulated, get gds
    s = sim(my_nmos, vgsp=AcDc(dc=3.3, ac=0), vdsp=AcDc(dc=3.3, ac=1))
    results = s.run(opts=opts)
    acres = results["ac"]
    gds = abs(acres.data["xtop.vds:p"][0])

    return gm / gds


for my_nmos in [
    pdk.Nmos(),
    pdk.Nmos(l=10 * u),
    pdk.Nmos(l=100 * u),
    pdk.Nmos(l=100000),
]:
    gain = get_the_gain(my_nmos)
    print(gain)

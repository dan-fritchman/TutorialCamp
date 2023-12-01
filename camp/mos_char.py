"""
# Mos Transistor Characterization
"""

import hdl21 as h
from hdl21.pdk import sample_pdk as pdk


@h.module
class Tb:
    """# Mos Char Testbench"""

    VSS = h.Port()  # The testbench interface: sole port VSS

    # The task at hand: fill in this testbench!
    # - Add DC sources for Vds and Vgs
    # - Add an instance of the Nmos transistor

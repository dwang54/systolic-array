"""pytest entry point: builds rtl/pe.sv and runs the cocotb tests in tb_pe.py.

Simulator is chosen with SIM=icarus|verilator (default icarus).
Set WAVES=1 to dump waveforms into build/pe/<sim>/.
"""

from conftest import run_cocotb


def test_pe():
    run_cocotb(toplevel="pe", sources=["pe.sv"], test_module="tb_pe")

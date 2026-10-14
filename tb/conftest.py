"""Shared pytest plumbing for building and running cocotb testbenches."""

import os
import sys
from pathlib import Path

from cocotb_tools.runner import get_runner

ROOT = Path(__file__).resolve().parent.parent
RTL = ROOT / "rtl"
TB = ROOT / "tb"
MODEL = ROOT / "model"

os.environ["MAKEFLAGS"] = f"{os.environ.get('MAKEFLAGS', '')} PYTHON3={sys.executable}".strip()


def run_cocotb(toplevel, sources, test_module, parameters=None, build_name=None):
    sim = os.getenv("SIM", "icarus")
    waves = os.getenv("WAVES", "0") == "1"
    build_dir = ROOT / "build" / (build_name or toplevel) / sim

    runner = get_runner(sim)
    runner.build(
        sources=[RTL / s for s in sources],
        hdl_toplevel=toplevel,
        parameters=parameters or {},
        build_dir=build_dir,
        timescale=("1ns", "1ps"),
        waves=waves,
        always=True,
    )
    runner.test(
        hdl_toplevel=toplevel,
        test_module=test_module,
        test_dir=build_dir,
        extra_env={"PYTHONPATH": os.pathsep.join([str(TB), str(MODEL)])},
        waves=waves,
    )

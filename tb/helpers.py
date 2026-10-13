"""Small helpers shared by cocotb testbenches."""

import cocotb
from cocotb.clock import Clock
from cocotb.triggers import FallingEdge, RisingEdge, Timer


def to_unsigned(value, width):
    """Two's-complement encode a Python int for driving a signal."""
    return value & ((1 << width) - 1)


def to_signed(value, width):
    """Decode a signal's raw bits as a signed integer."""
    v = int(value)
    return v - (1 << width) if v & (1 << (width - 1)) else v


async def start_clock_and_reset(dut, period_ns=10):
    """Start the clock and apply an async active-low reset for 2 cycles."""
    cocotb.start_soon(Clock(dut.clk, period_ns, unit="ns").start())
    dut.rst_n.value = 0
    await Timer(1, unit="ns")
    for _ in range(2):
        await RisingEdge(dut.clk)
    dut.rst_n.value = 1
    await FallingEdge(dut.clk)


async def step(dut):
    """Advance one clock. Inputs set before calling are sampled on the rising
    edge; outputs are read safely after the following falling edge."""
    await RisingEdge(dut.clk)
    await FallingEdge(dut.clk)

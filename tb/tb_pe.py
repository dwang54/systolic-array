"""cocotb tests for rtl/pe.sv. Run via `make test` (see tb/test_pe.py)."""

import random

import cocotb

from helpers import start_clock_and_reset, step, to_signed, to_unsigned

DATA_W, ACC_W = 8, 32


def drive(dut, a=0, b=0, en=1, clear=0):
    dut.a_in.value = to_unsigned(a, DATA_W)
    dut.b_in.value = to_unsigned(b, DATA_W)
    dut.en.value = en
    dut.clear.value = clear


def acc(dut):
    return to_signed(dut.acc.value, ACC_W)


@cocotb.test()
async def reset_clears_state(dut):
    drive(dut, en=0)
    await start_clock_and_reset(dut)
    assert acc(dut) == 0
    assert int(dut.a_out.value) == 0 and int(dut.b_out.value) == 0


@cocotb.test()
async def accumulates_random_stream(dut):
    drive(dut, en=0)
    await start_clock_and_reset(dut)
    rng = random.Random(1)
    expected = 0
    for _ in range(200):
        a, b = rng.randint(-128, 127), rng.randint(-128, 127)
        drive(dut, a, b)
        await step(dut)
        expected += a * b
        assert acc(dut) == expected
        assert to_signed(dut.a_out.value, DATA_W) == a
        assert to_signed(dut.b_out.value, DATA_W) == b


@cocotb.test()
async def extreme_values_no_overflow(dut):
    """-128 * -128 is the largest product; 1000 of them must not wrap."""
    drive(dut, en=0)
    await start_clock_and_reset(dut)
    for _ in range(1000):
        drive(dut, -128, -128)
        await step(dut)
    assert acc(dut) == 1000 * 16384


@cocotb.test()
async def enable_low_holds_state(dut):
    drive(dut, en=0)
    await start_clock_and_reset(dut)
    drive(dut, 5, 7)
    await step(dut)
    drive(dut, 100, 100, en=0)
    for _ in range(5):
        await step(dut)
    assert acc(dut) == 35
    assert to_signed(dut.a_out.value, DATA_W) == 5


@cocotb.test()
async def clear_semantics(dut):
    drive(dut, en=0)
    await start_clock_and_reset(dut)
    drive(dut, 3, 4)
    await step(dut)                      # acc = 12
    drive(dut, 2, -5, clear=1)           # clear + en: start fresh with this product
    await step(dut)
    assert acc(dut) == -10
    drive(dut, 9, 9, en=0, clear=1)      # clear alone: zero, no MAC
    await step(dut)
    assert acc(dut) == 0

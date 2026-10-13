# Common commands. Run `make help` to list them.
SIM    ?= icarus
WAVES  ?= 0
PYTHON ?= $(if $(wildcard .venv/bin/python),.venv/bin/python,python3)
TOP    ?= pe

.PHONY: help test wave lint synth clean

help:
	@echo "make test           run all testbenches (SIM=icarus|verilator)"
	@echo "make wave           run tests with waveform dumps into build/"
	@echo "make lint           verilator lint of rtl/"
	@echo "make synth TOP=pe   yosys synthesis + cell/area stats"
	@echo "make clean          delete build outputs"

test:
	SIM=$(SIM) WAVES=$(WAVES) $(PYTHON) -m pytest -q tb

wave:
	$(MAKE) test WAVES=1
	@echo "Waveforms written under build/<module>/$(SIM)/ (open with Surfer)"

lint:
	verilator --lint-only -Wall rtl/*.sv

synth:
	@mkdir -p build/synth
	yosys -q -p "read_verilog -sv rtl/*.sv; synth -top $(TOP); tee -o build/synth/$(TOP)_stat.txt stat"
	@echo "Report: build/synth/$(TOP)_stat.txt"

clean:
	rm -rf build .pytest_cache tb/__pycache__ model/__pycache__ results.xml

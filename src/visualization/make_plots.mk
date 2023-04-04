SHELL := bash
.ONESHELL:
.SHELLFLAGS := -eu -o pipefail -c

.PHONY: all clean

VPATH:=./data/processed

VIOLINS:=./reports/figures/violin/
REGPLOT:=./reports/figures/regression/
PERCPLOT:=./reports/figures/percentiles/

all: percplot

violin: final_bp_db.csv
	./src/visualization/violin.py $< $(VIOLINS) $(PARAMS) --healthy

regplot: final_bp_db.csv
	./src/visualization/regplot.py $< $(REGPLOT) $(PARAMS) --healthy

percplot: final_bp_db.csv
	./src/visualization/percentile_plot.py $< $(PERCPLOT) $(PARAMS) --healthy

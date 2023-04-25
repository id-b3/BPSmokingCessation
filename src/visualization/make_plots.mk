SHELL := bash
.ONESHELL:
.SHELLFLAGS := -eu -o pipefail -c

.PHONY: all clean

VPATH:=./data/processed

VIOLINS:=./reports/figures/violin/
REGPLOT:=./reports/figures/regression/
PERCPLOT:=./reports/figures/percentiles/

ifeq ($(STUDY_HEALTHY),true)
	H_FLAG = --healthy
endif

all: violin regplot percplot

violin: final_bp_db.csv
	./src/visualization/violin.py $< $(VIOLINS) $(PARAMS) $(H_FLAG)

regplot: final_bp_db.csv
	./src/visualization/regplot.py $< $(REGPLOT) $(PARAMS) $(H_FLAG)

percplot: final_bp_db.csv
	./src/visualization/percentile_plot.py $< $(PERCPLOT) $(PARAMS) $(H_FLAG)

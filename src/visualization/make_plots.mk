SHELL := bash
.ONESHELL:
.SHELLFLAGS := -eu -o pipefail -c

.PHONY: all clean

VPATH=./data/processed

VIOLINS=./reports/figures/violin/
REGPLOT=./reports/figures/regression/
PARAMS=bp_pi10,bp_tcount,bp_airvol,bp_wap_avg,bp_la_avg,bp_wt_avg,bp_ir_avg,bp_or_avg

all: violin regplot

violin: final_bp_db.csv
	./src/visualization/violin.py $< $(VIOLINS) $(PARAMS) --healthy

regplot: final_bp_db.csv
	./src/visualization/regplot.py $< $(REGPLOT) $(PARAMS) --healthy

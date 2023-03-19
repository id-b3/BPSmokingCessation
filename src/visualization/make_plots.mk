SHELL := bash
.ONESHELL:
.SHELLFLAGS := -eu -o pipefail -c

.PHONY: all clean

VPATH=./data/processed

VIOLINS=./reports/figures/violin/
PARAMS=bp_pi10,bp_tcount,bp_airvol,bp_wap_avg,bp_la_avg,bp_wt_avg,bp_ir_avg,bp_or_avg

all: violin

violin: final_bp_db.csv
	./src/visualization/violin.py $< $(VIOLINS) $(PARAMS)

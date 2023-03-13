SHELL := bash
.ONESHELL:
.SHELLFLAGS := -eu -o pipefail -c

.PHONY: all clean

VPATH=./data/processed/

COL_SUM=$(VPATH)bp_db_summary.csv
BP_CSV=final_bp_db.csv

FILTER_COLS=age,gender,smoking

all: $(COL_SUM)

$(COL_SUM): $(BP_CSV)
	csvstat --csv $< > $@

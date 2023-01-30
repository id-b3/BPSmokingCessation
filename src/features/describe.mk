SHELL := bash
.ONESHELL:
.SHELLFLAGS := -eu -o pipefail -c

.PHONY: all clean

VPATH=./data/processed/

COL_SUM=$(VPATH)db_summary.csv
BP_CSV=bronchial_parameter_db.csv

FILTER_COLS=age,gender,smoking

all: $(COL_SUM)

$(COL_SUM): $(BP_CSV)
	csvstat --csv $< > $@

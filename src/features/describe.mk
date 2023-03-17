SHELL := bash
.ONESHELL:
.SHELLFLAGS := -eu -o pipefail -c

.PHONY: all clean

REPPATH=./reports/descriptive/
BP_CSV=./data/processed/final_bp_db.csv

DEMO_CSV=$(REPPATH)demographics.csv

all: $(DEMO_CSV)

$(DEMO_CSV): $(BP_CSV)
	mkdir -p $(REPPATH)
	./src/features/get_demographics.py $< $@

SHELL := bash
.ONESHELL:
.SHELLFLAGS := -eu -o pipefail -c

.PHONY: all clean

REPPATH=./reports/descriptive/
BP_CSV=./data/processed/final_bp_db.csv

DEMO_CSV=$(REPPATH)demographics.csv
FLOW_MM=$(REPPATH)participant_flowchart.md

all: $(DEMO_CSV) $(FLOW_MM)

$(DEMO_CSV): $(BP_CSV)
	mkdir -p $(REPPATH)
	./src/features/get_demographics.py $< $@

$(FLOW_MM): $(BP_CSV)
	mkdir -p $(REPPATH)
	./src/features/participant_flowchart.py $< $@

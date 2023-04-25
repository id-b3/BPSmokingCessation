SHELL := bash
.ONESHELL:
.SHELLFLAGS := -eu -o pipefail -c

.PHONY: all clean

REPPATH=./reports/descriptive/

DEMO_CSV=$(REPPATH)demographics.csv
FLOW_MM=$(REPPATH)participant_flowchart.csv

ifeq ($(STUDY_HEALTHY),true)
	H_FLAG = --healthy
endif

all: $(DEMO_CSV) $(FLOW_MM)

$(DEMO_CSV): $(BP_FINAL)
	mkdir -p $(REPPATH)
	./src/features/descriptive/demographics.py $< $@ $(H_FLAG)

$(FLOW_MM): $(BP_FINAL)
	mkdir -p $(REPPATH)
	./src/features/descriptive/participant_flowchart.py $< $@

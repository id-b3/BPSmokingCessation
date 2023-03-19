SHELL := bash
.ONESHELL:
.SHELLFLAGS := -eu -o pipefail -c

.PHONY: all clean

REPPATH=./reports/analyses/

ANOVA=$(REPPATH)gender_anova_tukey.csv

all: $(ANOVA)

$(ANOVA): $(BP_FINAL)
	mkdir -p $(REPPATH)
	./src/features/analysis/gender_analysis.py $< $(PARAMS) $(dir $@)

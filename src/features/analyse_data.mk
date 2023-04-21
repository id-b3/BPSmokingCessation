SHELL := bash
.ONESHELL:
.SHELLFLAGS := -eu -o pipefail -c

.PHONY: all clean

REPPATH=./reports/analyses/

GENDER=$(REPPATH)gender_anova_tukey.csv
AGE=$(REPPATH)age_pearson_rsq.csv

all: $(GENDER) $(AGE) MLR

$(GENDER): $(BP_FINAL)
	mkdir -p $(REPPATH)
	./src/features/analysis/gender_analysis.py $< $(PARAMS) $@ --healthy

$(AGE): $(BP_FINAL)
	mkdir -p $(REPPATH)
	./src/features/analysis/age_analysis.py $< $(PARAMS) $@ --healthy

MLR: $(BP_FINAL)
	mkdir -p $(REPPATH)
	./src/models/relational/multivariate_regression.py $< $(PARAMS) $(REPPATH) --healthy

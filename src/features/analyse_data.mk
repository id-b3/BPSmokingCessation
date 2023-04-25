SHELL := bash
.ONESHELL:
.SHELLFLAGS := -eu -o pipefail -c

.PHONY: all clean

REPPATH=./reports/analyses/

GENDER=$(REPPATH)gender_anova_tukey.csv
AGE=$(REPPATH)age_pearson_rsq.csv

ifeq ($(STUDY_HEALTHY),true)
	H_FLAG = --healthy
endif

all: $(GENDER) $(AGE) MLR

$(GENDER): $(BP_FINAL)
	mkdir -p $(REPPATH)
	./src/features/analysis/gender_analysis.py $< $(PARAMS) $@ $(H_FLAG)

$(AGE): $(BP_FINAL)
	mkdir -p $(REPPATH)
	./src/features/analysis/age_analysis.py $< $(PARAMS) $@ $(H_FLAG)

MLR: $(BP_FINAL)
	mkdir -p $(REPPATH)
	./src/models/relational/multivariate_regression.py $< $(PARAMS) $(REPPATH) $(H_FLAG)

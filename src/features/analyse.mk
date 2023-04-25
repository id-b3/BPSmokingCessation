SHELL := bash
.ONESHELL:
.SHELLFLAGS := -eu -o pipefail -c

.PHONY: all clean

REPPATH=./reports/analyses/

GENDER=$(REPPATH)gender_anova_tukey.csv
AGE=$(REPPATH)age_pearson_rsq.csv
HEIGHT=$(REPPATH)height_pearson_rsq.csv
CESSATION=$(REPPATH)cessation_mlr.csv

ifeq ($(STUDY_HEALTHY),true)
	H_FLAG = --healthy
endif

all: $(GENDER) $(AGE) $(HEIGHT) $(CESSATION)

$(GENDER): $(BP_FINAL)
	mkdir -p $(REPPATH)
	./src/features/analysis/gender_analysis.py $< $(PARAMS) $@ $(H_FLAG)

$(AGE): $(BP_FINAL)
	mkdir -p $(REPPATH)
	./src/features/analysis/correlation.py $< $(PARAMS) $@ "age_at_scan" $(H_FLAG)

$(HEIGHT): $(BP_FINAL)
	mkdir -p $(REPPATH)
	./src/features/analysis/correlation.py $< $(PARAMS) $@ "length_at_scan" $(H_FLAG)

$(CESSATION): $(BP_FINAL)
	mkdir -p $(REPPATH)
	./src/features/analysis/cessation_analysis.py $< $(PARAMS) $@ $(H_FLAG)


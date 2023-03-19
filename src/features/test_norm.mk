SHELL := bash
.ONESHELL:
.SHELLFLAGS := -eu -o pipefail -c

.PHONY: all clean

# CONDA_ACTIVATE=source $$(conda info --base)/etc/profile.d/conda.sh ; conda activate ; conda activate

all: hist

hist: $(BP_FINAL)
	# $(CONDA_ACTIVATE) stats
	for col in $(PARAMS) ; do \
		csvcut -c "$$col,gender,GOLD_stage,copd_diagnosis,asthma_diagnosis" $< | python ./src/features/descriptive/test_normality.py ; \
	done

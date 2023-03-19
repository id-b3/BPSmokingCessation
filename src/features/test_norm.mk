SHELL := bash
.ONESHELL:
.SHELLFLAGS := -eu -o pipefail -c

.PHONY: all clean

VPATH=./data/processed/
CONDA_ACTIVATE=source $$(conda info --base)/etc/profile.d/conda.sh ; conda activate ; conda activate
FIGS=bp_pi10 bp_tcount bp_airvol bp_tlv bp_wap_avg bp_la_avg bp_wt_avg

all: hist

hist: final_bp_db.csv
	$(CONDA_ACTIVATE) stats
	for col in $(FIGS) ; do \
		csvcut -c "$$col,gender,GOLD_stage,copd_diagnosis,asthma_diagnosis" $< | python ./src/features/test_normality.py ; \
	done

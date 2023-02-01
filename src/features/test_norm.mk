SHELL := bash
.ONESHELL:
.SHELLFLAGS := -eu -o pipefail -c

.PHONY: all clean

VPATH=./data/processed/
CONDA_ACTIVATE=source $$(conda info --base)/etc/profile.d/conda.sh ; conda activate ; conda activate
FIGS=bp_pi10 bp_tcount bp_airvol bp_tlv bp_wap_3 bp_la_3 bp_wt_3

all: hist

hist: final_bp_db.csv
	$(CONDA_ACTIVATE) stats
	for col in $(FIGS) ; do \
		csvcut -c "$$col,gender" $< | python ./src/visualization/test_normality.py ; \
	done

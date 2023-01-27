SHELL := bash
.ONESHELL:
.SHELLFLAGS := -eu -o pipefail -c

.PHONY: all clean

VPATH=./data/raw/
DINT=./data/interim/
DPRC=./data/processed/

SPSS_FILES=1a_q_1.sav 1a_v_1.sav 2a_q_2.sav 2a_v_1.sav
CSV_FILES=$(DINT)1a_q_1.csv $(DINT)1a_v_1.csv $(DINT)2a_q_2.csv $(DINT)2a_v_1.csv

BP_COLS=bp_wap,bp_la,bp_wt,bp_ir,bp_or

SEG_CSV=segmentation_review_final.csv
SPLT_CSV=$(DINT)formatted_bp_data.csv
MRG_CSV=$(DINT)data_merged.csv
BP_CSV=$(DPRC)bronchial_parameter_db.csv


all: $(BP_CSV)
	echo "Done"

# Remove any columns that contain only 1 unique value
$(BP_CSV): $(MRG_CSV)
	< $< csvcut -C $$(csvstat $< --unique | grep ': 1$$' | cut -d. -f 1 | tr -d ' ' | paste -sd,) > $@

# Merge all CSV files into one using the patientID as an index
$(MRG_CSV): $(CSV_FILES) $(SPLT_CSV)
	csvjoin -c patientID $^ > $@

# Expand the semicolon delim'd bps and change participant_id to patientID
$(SPLT_CSV): $(SEG_CSV)
	csvjoin <(csvcut -C $(BP_COLS) $< | sed 's/participant_id/patientID/') <(csvcut -c $(BP_COLS) $< | awk -f ./src/data/expand_bps.awk) > $@

# Convert the SPSS files into CSV files
$(CSV_FILES): $(DINT)%.csv : %.sav
	pspp-convert $< $@

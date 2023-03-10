SHELL := bash
.ONESHELL:
.SHELLFLAGS := -eu -o pipefail -c

.PHONY: all clean

VPATH=./data/raw/
DINT=./data/interim/
DPRC=./data/processed/

SPSS_FILES=1a_q_1.sav 1b_q_1.sav 1c_q_1.sav 1a_v_1.sav 2a_q_2.sav 2b_q_1.sav 2a_v_1.sav
CSV_FILES=$(DINT)2b_q_1.csv $(DINT)2a_q_2.csv $(DINT)2a_v_1.csv $(DINT)1c_q_1.csv $(DINT)1b_q_1.csv $(DINT)1a_q_1.csv $(DINT)1a_v_1.csv
BP_COLS=bp_wap,bp_la,bp_wt,bp_ir,bp_or

SEG_CSV=final_bp_list.csv
SCN_CSV=participant_age-at-scan.csv
SPLT_CSV=$(DINT)formatted_bp_data.csv
MRG_CSV=$(DINT)data_merged.csv
BP_CSV=$(DINT)bronchial_parameter_db_full.csv
BP_FILT_CSV=$(DINT)bp_db_filtered.csv
BP_FINAL=$(DPRC)final_bp_db.csv

DB_COLS=1,341,342,343,344,125,126,127,200,210,297,298,299,58,86,191,201,232,59,106,192,202,224,60,107,193,203,225,61,108,256,62,109,194,204,270,65,116,196,281,66,117,197,207,282,88,162,212,326,91,166,223,224,220,221,103,218,227,293,146,151,152,156,171,172,313,318,319,322,332,333,2,3,4,5,6,8,9,10,11,13,14,15,16,17,18,19,20,21,22,23,24,25,26,27,28,29,30,31,32,33,34,35,36,37,38,39,40,41,42,43,44,45,46,47,48,49,50,51,52,53,54,55,56,57
# DB_COLS=1,2,311,308,309,88,89,90,185,186,187,36,167,37,168,24,147,48,169,62,170,67,175,74,75,178,179,15,16,152,226,4,117,222,149,10,12,13,19,85,164,104,109,113,206,211,216,110,212,123,124,231,232,310,255,258,259,260,251,252,253,254,262,263,264,265,266,267,268,269,270,271,272,273,274,275,276,277,278,279,280,281,282,283,284,285,286,287,288,289,290,291,292,293,294,295,296,297,298,299,300,301,302,303,304,305,306


all: $(BP_FINAL)
	echo "Done"

$(BP_FINAL): $(BP_FILT_CSV)
	< $< ./src/data/fill_missing.py
	< $@ wc -l

$(BP_FILT_CSV): $(BP_CSV)
	< $< csvcut -c $(DB_COLS) > $@
	< $@ wc -l

# Remove any columns that contain only 1 unique value
$(BP_CSV): $(MRG_CSV)
	< $< csvcut -C $$(csvstat $< --unique | grep ': 1$$' | cut -d. -f 1 | tr -d ' ' | paste -sd,) > $@
	< $@ wc -l

# Merge all CSV files into one using the patientID as an index
$(MRG_CSV): $(SPLT_CSV) $(CSV_FILES) $(SCN_CSV)
	csvjoin --left -c patientID $^ > $@
	< $@ wc -l

# Expand the semicolon delim'd bps and change participant_id to patientID
$(SPLT_CSV): $(SEG_CSV)
	csvjoin <(csvcut -C $(BP_COLS) $< | sed 's/participant_id/patientID/') <(csvcut -c $(BP_COLS) $< | awk -f ./src/data/expand_bps.awk) > $@
	< $@ wc -l

# Convert the SPSS files into CSV files
$(CSV_FILES): $(DINT)%.csv : %.sav
	pspp-convert $< $@_nonan.csv
	# Replace $$5, $$6, $$7 with nan
	sed 's/\$$[0-9]//g' $@_nonan.csv | csvsort -c patientID > $@
	< $@ wc -l

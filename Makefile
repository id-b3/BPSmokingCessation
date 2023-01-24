SHELL := bash
.ONESHELL:
.SHELLFLAGS := -eu -o pipefail -c

.PHONY: all clean

SPSS_FILES=./data/1a_q_1.sav ./data/1a_v_1.sav ./data/2a_q_2.sav ./data/2a_v_1.sav
CSV_FILES=./data/1a_q_1.csv ./data/1a_v_1.csv ./data/2a_q_2.csv ./data/2a_v_1.csv
SEG_CSV=./data/segmentation_review_final.csv
BP_CSV=./data/bronchial_parameters.csv


all: data/data_cleaned.csv
	echo "Done"

# Convert the SPSS files into CSV files
%.csv: %.sav
	pspp-convert $^ $@

# Change the id from participant_id to patientID
$(BP_CSV): $(SEG_CSV)

# Merge all CSV files into one using the patientID as an index
data/data_merged.csv: $(CSV_FILES) $(BP_CSV)
	csvjoin -c patientID $^ <(sed 's/participant_id/patientID/' $(BP_CSV)) > $@

# Remove any columns that contain only 1 unique value
data/data_cleaned.csv: data/data_merged.csv
	< $< csvcut -C $$(csvstat $< --unique | grep ': 1$$' | cut -d. -f 1 | tr -d ' ' | paste -sd,) > $@

clean:
	rm -f data/data_merged.csv

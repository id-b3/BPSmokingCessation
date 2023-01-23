SHELL := bash
.ONESHELL:
.SHELLFLAGS := -eu -o pipefail -c

.PHONY: all clean

all: data/data_cleaned.csv
	echo "Done"

# Convert the SPSS files into CSV files
data/csv/1a_q.csv: ./data/1a_q_1.sav
	mkdir -p data/csv
	pspp-convert ./data/1a_q_1.sav ./data/csv/1a_q.csv

data/csv/1a_v.csv: ./data/1a_v_1.sav
	mkdir -p data/csv
	pspp-convert ./data/1a_v_1.sav ./data/csv/1a_v.csv

data/csv/2a_q.csv: ./data/2a_q_2.sav
	mkdir -p data/csv
	pspp-convert ./data/2a_q_2.sav ./data/csv/2a_q.csv

data/csv/2a_v.csv: ./data/2a_v_1.sav
	mkdir -p data/csv
	pspp-convert ./data/2a_v_1.sav ./data/csv/2a_v.csv

# Change the id from participant_id to patientID
data/bronchial_parameters.csv: ./data/segmentation_review_final.csv
	sed 's/participant_id/patientID/' $< > $@

# Merge all CSV files into one using the patientID as an index
data/data_merged.csv: data/csv/1a_q.csv data/csv/1a_v.csv data/csv/2a_q.csv data/csv/2a_v.csv ./data/bronchial_parameters.csv
	csvjoin -c patientID $^ > $@

# Remove any columns that contain only 1 unique value
data/data_cleaned.csv: data/data_merged.csv
	< $< csvcut -C $$(csvstat $< --unique | grep ': 1$$' | cut -d. -f 1 | tr -d ' ' | paste -sd,) > $@

clean:
  rm -f data/data_merged.csv

SHELL = /bin/bash

data/processed/all_plants.csv : data/intermediate/all_plants.csv
	@echo "Reformatting gene detection data..."
	cat $< | python processors/transform_wide_to_long.py > $@

.INTERMEDIATE : data/intermediate/all_plants.csv
data/intermediate/all_plants.csv : data/raw/all_plants.csv
	@echo "Adding pre-populated lab name column..."
	csvstack -n lab_name -g SCAN $< > $@

data/raw/all_plants.csv :
	@echo "Downloading gene detection data..."
	wget --no-use-server-timestamps https://soe-wbe-pilot.wl.r.appspot.com/plantdata?plant=All \
		-O $@

.PHONY : clean
clean :
	@echo "Removing data..."
	rm $$(find data -name *.csv)

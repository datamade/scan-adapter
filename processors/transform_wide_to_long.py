import csv
import sys

from yaml import load as load_yaml, Loader


reader = csv.DictReader(sys.stdin)

output_columns = [
	"lab_name",
	"lab_sample_id",
	"wwtp_name",
	"sample_collect_date",
	"test_result_date",
	"target",
	"units",
	"measurement",
	"measurement_source",
	"lower_confidence_interval",
	"lci_source",
	"upper_confidence_interval",
	"uci_source",
]

writer = csv.DictWriter(sys.stdout, fieldnames=output_columns)

with open("targets.yml", "r") as f:
	targets = load_yaml(f, Loader=Loader) 

genes = targets["genes"]
measurement_types = targets["measurement_types"]

writer.writeheader()

for row in reader:
	output_row = {
		"lab_name": row["lab_name"],
		"lab_sample_id": row["Sample"],
		"wwtp_name": row["Plant"],
		"sample_collect_date": row["Collection_Date"],
		"test_result_date": row["Date"],
	}

	for gene, gene_meta in genes.items():
		for measurement_type in gene_meta["measurements"]:
			measurement_meta = measurement_types[measurement_type]
			
			try:
				measurement_key = f"{gene}_{measurement_meta['variable_suffix']}"
				measurement = row[measurement_key]
			except KeyError:
				measurement_key = f"{gene_meta['alias']}_{measurement_meta['variable_suffix']}"
				measurement = row[measurement_key]

			# TODO: Blank values mean a sample was not tested for a particular gene.
			# Should we include those in the output, or omit them?

			if measurement_meta["confidence"]:
				lci_key = f"{measurement_key}_{measurement_types['lower_confidence']['variable_suffix']}"
				uci_key = f"{measurement_key}_{measurement_types['upper_confidence']['variable_suffix']}"
				
				lci, uci = row[lci_key], row[uci_key]
			else:
				lci_key, uci_key, lci, uci = None, None, None, None

			result = output_row.copy()

			result.update({
				"target": gene,
				"units": measurement_meta["description"],
				"measurement": measurement,
				"measurement_source": measurement_key,
				"lower_confidence_interval": lci,
				"lci_source": lci_key,
				"upper_confidence_interval": uci,
				"uci_source": uci_key,
			})

			writer.writerow(result)

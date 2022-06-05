import csv
from typing import Dict
from dicter.filter import apply
from dicter.parser import parse


class CSV_filter:
    def __init__(self, input_file_path: str, output_file_path) -> None:
        self.in_path = input_file_path
        self.out_path = output_file_path

    def write_filtered_file(self, dict: Dict):
        # Read full file into a list of dicts.
        # FIXME: apply should be able to work with Dictreader.
        #        We should not have to load the whole file into memory.
        expression = parse(dict)
        input_file = csv.DictReader(open(self.in_path))
        records = []
        for input in input_file:
            records.append(input)

        # apply the expression to the full recordset
        filtered_records = apply(expression, records)
        if len(filtered_records) == 0:
            print("No records to write.  No file created.")
            return

        # Write filtered records out to out_path
        # Get the field names from the first record
        field_names = filtered_records[0].keys()

        # Write the output csv
        with open(self.out_path, 'w', encoding='UTF8', newline='') as f:
            writer = csv.DictWriter(f, fieldnames=field_names)
            writer.writeheader()
            writer.writerows(filtered_records)

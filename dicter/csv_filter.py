import csv
from typing import Dict
from dicter.filter import apply
from dicter.parser import parse


class CSV_filter:
    def __init__(self, input_file_path: str, output_file_path) -> None:
        self.in_path = input_file_path
        self.out_path = output_file_path

    def write_filtered_file(self, dict: Dict):

        # Parse the input dict
        expression = parse(dict)

        # Open the input file
        input_file = csv.DictReader(open(self.in_path))

        # Apply the expression
        filtered_records = apply(expression, input_file)
        if len(filtered_records) == 0:
            print("No records to write.  No file created.")
            return

        # Get the field names from the first record
        field_names = filtered_records[0].keys()

        # Write the output csv
        with open(self.out_path, 'w', encoding='UTF8', newline='') as f:
            writer = csv.DictWriter(f, fieldnames=field_names)
            writer.writeheader()
            writer.writerows(filtered_records)

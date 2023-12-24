import csv
from typing import Dict
from dicter.filter import apply
from dicter.parser import parse


class CSV_filter:
    """
    Writes filtered extracts of self.in_path to self.out_path.
    """

    def __init__(self, input_file_path: str, output_file_path) -> None:
        """
        Create a CSV_filter with the given input and output file paths.
        Arguments:
            input_file_path : full path to the csv input file
            output_file_path : full path to the output file
        """
        self.in_path = input_file_path
        self.out_path = output_file_path

    def write_filtered_file(self, dct: Dict):
        """
        Filter the records in self.in_path using the expression represented by dict.
        Write the filtered records to self.out_path.
        Arguments:
            dct : dictionary representing a filter expression.
        """
        # Parse the input dict
        expression = parse(dct)

        # Open the input file with explicit encoding
        input_file = csv.DictReader(open(self.in_path, encoding='UTF8'))

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

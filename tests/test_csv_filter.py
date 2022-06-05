from pathlib import Path
from dicter.csv_filter import CSV_filter
import csv
import os

TEST_DATA_DIR = Path(__file__).resolve().parent / 'data'
IN_FILE = TEST_DATA_DIR / 'in.csv'
OUT_FILE = TEST_DATA_DIR / 'out.csv'


def test_filter():
    csv_filter = CSV_filter(IN_FILE, OUT_FILE)
    csv_filter.write_filtered_file(
        {'$and':
            [
                {'$lt': {'Data.Temperature.Min Temp': 30}},
                {'$gt': {'Data.Wind.Speed': 15}}
            ]
         })
    input_file = csv.DictReader(open(OUT_FILE))
    records = []
    for input in input_file:
        records.append(input)
        assert(float(input['Data.Temperature.Min Temp']) < 30)
        assert(float(input['Data.Wind.Speed']) > 15)
    assert(len(records) == 2)
    os.remove(OUT_FILE)


def test_filter_regex():
    csv_filter = CSV_filter(IN_FILE, OUT_FILE)
    # Multi-word station city names
    csv_filter.write_filtered_file(
        {'$re': {'Station.City': r'\w+\s+\w+'}}
    )
    input_file = csv.DictReader(open(OUT_FILE))
    records = []
    for input in input_file:
        records.append(input)
        assert(' ' in input['Station.City'])
    assert(len(records) == 7)
    os.remove(OUT_FILE)

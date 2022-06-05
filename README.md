

# dicter: filter and analyze python recordsets and csv files
[![Package Status](https://img.shields.io/badge/status-experimental-yellow)](https://github.com/psteitz/dicter)
[![License](https://img.shields.io/badge/license-apache2-green))](https://github.com/psteitz/dicter/blob/main/LICENSE)

## What is this?

**dicter** is a small utility for filtering and analyzing data in csv files or lists of python dictionaries. Filter conditions are expressed using boolean combinations of assertions about field values. 

## Main Features
Here are the things you can do with dicter:

  - Read in a csv file and write out a filtered file including records that satisfy assertions about column values.
  - Filter a list of python dictionaries based on key-value assertions.
  - Compute statistics on filtered recordsets or csv files.

## Where to get it
The source code is currently hosted on GitHub at:
https://github.com/psteitz/dicter

There is no binary installer or packaged distribution at this time.

## Dependencies
- [NumPy - used for statistics](https://www.numpy.org)
 

## License
[Apache 2.0](LICENSE)

## Documentation
Basically non-existent, but here are some hints.

Filter conditions for csvs or lists of records are expressed using python dictionaries in a hopefully intuitive syntax.  Complex boolean expressions are built by combining other expressions using logical operators ``$not, $and, $or``. "Atomic" assertions about record field values (key-value assertions) can be numeric or string comparisons, regex matching or list inclusion.

See the sources, unit tests in ``/tests`` and examples in ``/examples`` for the full picture. Here are some examples that should give the idea of how things work:

### Filtering a csv
A sample csv file of weather station readings is included in ``/examples``.  Each record in the file is a set of daily readings from a weather station.  Among the columns are "Data.Temperature.Min Temp" and "Data.Wind.Speed".  Assume that ``IN_FILE`` is the full path to the file to be filtered.  The following code will write a filtered file to ``OUT_FILE`` that contains records that satisfy the condition:

- Minimum temperature is less than  30 and wind speed is greater than 15

```
csv_filter = CSV_filter(IN_FILE, OUT_FILE)
    csv_filter.write_filtered_file(
        {'$and':
            [
                {'$lt': {'Data.Temperature.Min Temp': 30}},
                {'$gt': {'Data.Wind.Speed': 15}}
            ]
         })
```
Note that the input to ``csv_filter.write`` is a python dictionary, not a string.  The example dict has one key, ``$and`` with corresponding value a list of two operands.  In the example, the operands are atomic assertions, but they could themselves be logical expressions.  The basic syntax of all dicter filters is ``{key : value}`` where ``key`` is an operator and ``value`` is either a list of operands or just one if ``key`` is unary.  The ``$and`` and ``$or`` operators can take arbitrary length lists.

### Filtering a recordset and computing stats on filtered records
If we use python's built-in csv to read the csv in ``/examples`` into a list of dicts, we can filter the recordset and compute column stats on the filtered records like so:

```
input_records = csv.DictReader(open(IN_FILE))
    filtered_records = apply(
        {'$and':
            [
                {'$or': [
                    {'$gt': {'Data.Temperature.Max Temp': 100}},
                    {'$gt': {'Data.Temperature.Min Temp': 80}}
                ]},
                {'$not': {'Station.State': 'Arizona'}}
            ]
         }, input_records)
    print(Stats(filtered_records, 'Data.Temperature.Min Temp').percentile(90))
```
The filter condition above says to include all non-Arizona readings where the max temp was greater than 100 or the min temp was greater than 80.  The ``Stats`` constructor computes descriptive stats for the designtated column in the filtered recordset and the ``percentile`` method reports the requested percentile.  

## Development
Issues can be reported [here](https://github.com/psteitz/dicter/issues).  PRs are welcome [here](https://github.com/psteitz/dicter/pulls).  

   

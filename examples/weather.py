import csv
from dicter.stats import Stats
from dicter.filter import apply

CSV_FILE_PATH = 'weather.csv'

# Parse the csv into a list of dicts
input_file = csv.DictReader(open(CSV_FILE_PATH, encoding='utf-8'))
records = []
for line in input_file:
    data = {}
    data['precipitation'] = line['Data.Precipitation']
    data['date'] = line['Date.Full']
    data['city'] = line['Station.City']
    data['state'] = line['Station.State']
    data['avg_temp'] = line['Data.Temperature.Avg Temp']
    data['max_temp'] = line['Data.Temperature.Max Temp']
    data['min_temp'] = line['Data.Temperature.Min Temp']
    data['wind'] = line['Data.Wind.Speed']
    records.append(data)

# All readings where min temperature is below zero
print("Cold days")
cold_readings = apply({'$lt': {'min_temp': 0}},
                      records)
for reading in cold_readings:
    print(reading)

# All readings where min is below zero and wind is greater than 15.
cold_and_windy = apply(
    {'$and': [{'$lt': {'min_temp': 0}}, {'$gt': {'wind': 15}}]},
    records)

print("Cold and windy")
for reading in cold_and_windy:
    print(reading)

# Get some statistics on the average temp among the cold and windy days
stats = Stats(cold_and_windy, 'avg_temp')
print("Number of cold and windy readings:", stats.n())
print("Median average temp among cold and windy readings:", stats.median())
print("90th percentile:", stats.percentile(90))

# Hot days in California or Arizona
overall_stats = Stats(records, 'avg_temp')
# 1.7 standard deviations above average
hot = overall_stats.mean() + 1.7 * overall_stats.std()
print("Hot readings from az, ca")
hot_az_ca = apply(
    {'$and':
        [
            {'$in': {'state': ['Arizona', 'California']}},
            {'$gt': {'avg_temp': hot}}
        ]
     }, records
)
for reading in hot_az_ca:
    print(reading)

import datetime
import pandas
from query_setup import collection
from epoch_converter import convert_epoch


# Use to build an entry of a DataFrame with pandas.DataFrame.append().
def make_row(datetimerecorded, stationname, frequency, use_weekday=False):
    if use_weekday:
        weekday = datetimerecorded.weekday()
        if   weekday == 1: weekday = "Monday"
        elif weekday == 2: weekday = "Tuesday"
        elif weekday == 3: weekday = "Wednesday"
        elif weekday == 4: weekday = "Thursday"
        elif weekday == 5: weekday = "Friday"
        elif weekday == 6: weekday = "Saturday"
        elif weekday == 7: weekday = "Sunday"

        return {
            "weekday": datetimerecorded,
            "stationname": stationname,
            "frequency": frequency,
            "hour": datetimerecorded.hour
        }

    else:
        return {
            "datetimerecorded": datetimerecorded,
            "stationname": stationname,
            "frequency": frequency
        }


# Generate valid, which will use make_row to build a DataFrame of relevant data.
valid = pandas.DataFrame()
i = 0
for document in collection.find({"recorded.speed" : {"$gt" : 100}}):
    i = 1
    epoch = document["recorded"]["datetimerecorded"]
    datetimerecorded = convert_epoch(epoch / 1000, type="datetime")
    stationname = document["location"]["stationname"]
    speed = document["recorded"]["speed"]
    if speed is not None:
        valid = valid.append(make_row(datetimerecorded, stationname, speed), ignore_index=True)

if i == 0: raise Exception("There is no data to work with; this will not run.")


# Scrub the minutes and seconds off each record and track the frequency of the
# values combined.
valid["datetimerecorded"] = valid["datetimerecorded"].apply(lambda date: date.replace(second=0))
valid["datetimerecorded"] = valid["datetimerecorded"].apply(lambda date: date.replace(minute=0))

data = pandas.DataFrame()
for datehour in valid["datetimerecorded"].unique():
    for station in valid["stationname"].unique():
        temp = valid[(valid["stationname"] == station) & (valid["datetimerecorded"] == datehour)]
        data = data.append(make_row(datehour, station, len(temp.index)), ignore_index=True)


# Condense the timeframe into a single week.
comps = {}
for index, row in data.iterrows():
    key = (row["datetimerecorded"], row["stationname"])
    if key not in comps:
        comps[key] = {}
        comps[key]["count"] = row["frequency"]
    else:
        comps[key]["count"] += row["frequency"]

final = pandas.DataFrame()
for key in comps:
    datetimerecorded = key[0]
    stationname = key[1]
    freq = comps[key]["count"]
    final = final.append(
                make_row(datetimerecorded, stationname, freq, use_weekday=True),
                ignore_index=True
                )

print("The frequency of an entry going faster than 100 MPH by hour, station, and weekday:")
print(final)

# TODO: visualize


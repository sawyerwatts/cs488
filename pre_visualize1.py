import datetime
import pandas

from query_setup import collection
from epoch_converter import convert_epoch


###############################################################################
# Functions
###########

# Use to build an entry of a DataFrame with pandas.DataFrame.append().
def make_row(datetimerecorded, stationname, nextstationname, frequency, use_weekday=False):
    if use_weekday:
        weekday = datetimerecorded.weekday()
        if   weekday == 0: weekday = "Monday"
        elif weekday == 1: weekday = "Tuesday"
        elif weekday == 2: weekday = "Wednesday"
        elif weekday == 3: weekday = "Thursday"
        elif weekday == 4: weekday = "Friday"
        elif weekday == 5: weekday = "Saturday"
        elif weekday == 6: weekday = "Sunday"

        return {
            "weekday": weekday,
            "stationname": stationname,
            "nextstationname": nextstationname,
            "frequency": frequency,
            "hour": datetimerecorded.hour
        }

    else:
        return {
            "datetimerecorded": datetimerecorded,
            "stationname": stationname,
            "nextstationname": nextstationname,
            "frequency": frequency
        }


###############################################################################
# Verify and collected needed data
##################################

# Generate valid, which will use make_row to build a DataFrame of relevant data.
valid = pandas.DataFrame()
i = 0
for document in collection.find({"recorded.speed" : {"$gt" : 100}}):
    i = 1
    epoch = document["recorded"]["datetimerecorded"]
    datetimerecorded = convert_epoch(epoch / 1000, type="datetime")
    stationname = document["location"]["stationname"]
    nextstationname = document["location"]["nextstationname"]
    speed = document["recorded"]["speed"]
    if speed is not None:
        valid = valid.append(make_row(datetimerecorded, stationname, nextstationname, speed), ignore_index=True)

if i == 0: raise Exception("There is no data to work with; this will not run.")


# Scrub the minutes and seconds off each record and track the frequency of the
# values combined.
valid["datetimerecorded"] = valid["datetimerecorded"].apply(lambda date: date.replace(second=0))
valid["datetimerecorded"] = valid["datetimerecorded"].apply(lambda date: date.replace(minute=0))

data = pandas.DataFrame()
for datehour in valid["datetimerecorded"].unique():
    for station in valid["stationname"].unique():
        temp = valid[(valid["stationname"] == station) & (valid["datetimerecorded"] == datehour)]
        nextstationname = valid[valid["stationname"] == station]["nextstationname"].iloc[0]
        data = data.append(make_row(datehour, station, nextstationname, len(temp.index)), ignore_index=True)


# Condense the timeframe into a single week.
# TODO: this is failing
comps = {}
for index, row in data.iterrows():
    key = (row["datetimerecorded"], row["stationname"], row["nextstationname"])
    if key not in comps:
        comps[key] = {}
        comps[key]["count"] = row["frequency"]
    else:
        comps[key]["count"] += row["frequency"]

final = pandas.DataFrame()
for key in comps:
    datetimerecorded = key[0]
    stationname = key[1]
    nextstationname = key[2]
    freq = comps[key]["count"]
    final = final.append(
                make_row(datetimerecorded, stationname, nextstationname, freq, use_weekday=True),
                ignore_index=True
                )

print("The frequency of an entry going faster than 100 MPH by hour, station, and weekday:")
print(final)

final.to_csv("visualize1.csv", index=False)



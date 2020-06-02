import datetime
import pandas
from query_setup import collection
from epoch_converter import convert_epoch


# Use to build an entry of a DataFrame with pandas.DataFrame.append().
def make_row(datetimerecorded, stationname, speed, use_weekday=False):
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
            "avgspeed": speed,
            "hour": datetimerecorded.hour
        }

    else:
        return {
            "datetimerecorded": datetimerecorded,
            "stationname": stationname,
            "speed": speed
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


# Scrub the minutes and seconds off each record and average these into a single
# value.
valid["datetimerecorded"] = valid["datetimerecorded"].apply(lambda date: date.replace(second=0))
valid["datetimerecorded"] = valid["datetimerecorded"].apply(lambda date: date.replace(minute=0))

data = pandas.DataFrame()
for datehour in valid["datetimerecorded"].unique():
    for station in valid["stationname"].unique():
        temp = valid[(valid["stationname"] == station) & (valid["datetimerecorded"] == datehour)]
        total = 0
        for index, row in temp.iterrows():
            total += row["speed"]
        avg = total / len(temp.index)
        data = data.append(make_row(datehour, station, avg), ignore_index=True)

print("Speed that is averaged by hour and station:") # TODO: delete
print(data) # TODO: delete
print() # TODO: delete


# Condense the timeframe into a single week.
comps = {}
for index, row in data.iterrows():
    key = (row["datetimerecorded"], row["stationname"])
    if key not in comps:
        comps[key] = {}
        comps[key]["total"] = row["speed"]
        comps[key]["count"] = 1
    else:
        comps[key]["total"] += row["speed"]
        comps[key]["count"] += 1

final = pandas.DataFrame()
for key in comps:
    datetimerecorded = key[0]
    stationname = key[1]
    avg = comps[key]["total"] / comps[key]["count"]
    final = final.append(make_row(datetimerecorded, stationname, avg, use_weekday=True), ignore_index=True)

print("Speed that is averaged by hour, station, and weekday:")
print(final)

# TODO: visualize



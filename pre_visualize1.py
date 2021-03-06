import datetime
import pandas
import numpy as np

from epoch_converter import convert_epoch


###############################################################################
# Functions.
############

def npdt_to_pydt(npdt):
    ts = (npdt - np.datetime64('1970-01-01T00:00:00Z')) / np.timedelta64(1, "s")
    pydt = datetime.datetime.utcfromtimestamp(ts)
    return pydt


# Use to build an entry of a DataFrame with pandas.DataFrame.append().
def make_row(datetimerecorded, stationname, frequency, hour=None, use_weekday=False, no_converting=False):
    if no_converting:
        if hour is None: raise Exception("hour cannot be unsupplied if no_converting is supplied.")
        return {
            "weekday": datetimerecorded,
            "stationname": stationname,
            "frequency": frequency,
            "hour": hour
        }

    elif use_weekday:
        if isinstance(datetimerecorded, np.datetime64):
            datetimerecorded = npdt_to_pydt(datetimerecorded)

        hour = datetimerecorded.hour
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
            "frequency": frequency,
            "hour": hour
        }

    else:
        return {
            "datetimerecorded": datetimerecorded,
            "stationname": stationname,
            "frequency": frequency
        }




###############################################################################
# Verify and collected needed data.
###################################

if __name__ == "__main__":
    from query_setup import collection

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
            data = data.append(make_row(datehour, station, len(temp.index), use_weekday=True), ignore_index=True)
    
    
    # Condense the timeframe into a single week.
    comps = {}
    for index, row in data.iterrows():
        key = (row["weekday"], row["hour"], row["stationname"])
        if key in comps:
            comps[key]["count"] += row["frequency"]
        else:
            comps[key] = {}
            comps[key]["count"] = row["frequency"]
    
    final = pandas.DataFrame()
    for key in comps:
        weekday = key[0]
        hour = key[1]
        stationname = key[2]
        freq = comps[key]["count"]
        final = final.append(
                    make_row(weekday, stationname, freq, hour, no_converting=True),
                    ignore_index=True
                    )
    
    print("The frequency of an entry going faster than 100 MPH by hour, station, and weekday:")
    print(final)
    
    final.to_csv("visualize1.csv", index=False)
    

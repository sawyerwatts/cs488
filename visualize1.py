import datetime
import pandas
from query_setup import collection
from epoch_converter import convert_epoch


###############################################################################
# Functions
###########

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

final.to_csv("data1.csv", index=False)


###############################################################################
# Visualize
###########

import plotly.graph_objects as go
from plotly.subplots import make_subplots

# TODO: make small multiples for each *day*.

# TODO: have the subtitles be extracted from the data
fig = make_subplots(rows=4, cols=2, subplot_titles=["Monday", "Tuesday", "Wednesday", "Thursday", "Friday", "Saturday", "Sunday"])
fig.add_trace(
    go.Scatter(
        name="Monday",
        x = [0, 1, 2, 3, 4], # TODO: replace with hour
        y = ["Station A", "Station B", "Station C", "Station D", "Station E"], # TODO: replace with stations
        mode="markers",
        marker=dict(
            size=15,
            color=[5, 4, 3, 2, 1], # TODO: have this map the color to the frequency
            colorscale="Viridis",
            showscale=True,
            line=dict(
                    color="Black",
                    width=2
            )
        )
    ),
    row=1, col=1
)
fig.update_xaxes(range=[-1, 24], row=1, col=1)

fig.add_trace(
    go.Scatter(
        name="Tuesday",
        x = [0, 1, 2, 3, 4], # TODO: replace with hour
        y = ["Station A", "Station B", "Station C", "Station D", "Station E"], # TODO: replace with stations
        mode="markers",
        marker=dict(
            size=15,
            color=[5, 4, 3, 2, 1], # TODO: have this map the color to the frequency
            colorscale="Viridis",
            showscale=True,
            line=dict(
                    color="Black",
                    width=2
            )
        )
    ),
    row=1, col=2
)
fig.update_xaxes(range=[-1, 24], row=1, col=2)

fig.update_layout(
    title="Frequencies of speeding (over 100 MPH) per Hour by Station",
    showlegend=False,
    height=2000,
    font=dict(
        size=18
    )
)

fig.show()

# fig.write_html("./vis1.html")


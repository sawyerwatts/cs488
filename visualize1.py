import pandas
import plotly.graph_objects as go
from plotly.subplots import make_subplots
import numpy as np


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
# Tweak and visualize.
######################


data = pandas.read_csv("visualize1.csv")
data.sort_values(by="stationname", inplace=True)

weekdays = list(set(data["weekday"].tolist()))
stations = [
    "Airportway WB to SB",
    "Airportway EB to SB",
    "Columbia to I-205 SB",
    "Glisan to I-205 SB",
    "Stark/Washington SB",
    "Division SB",
    "Powell Blvd SB",
    "Foster SB",
    "Johnson Creek SB",
    "Sunnyside SB",
    "Sunnyside NB",
    "Johnson Cr NB",
    "Foster NB",
    "Powell to I-205 NB",
    "Division NB",
    "Glisan to I-205 NB",
    "Columbia to I-205 NB"]


# Fill in any missing gaps from stations without any occurrences so the
# visualization is full.
for station in stations:
    for weekday in weekdays:
        for hour in range(0, 24):
            temp = data[
                    (data["stationname"] == station)
                    & (data["weekday"] == weekday)
                    & (data["hour"] == hour)
                    ]
            if len(temp.index) == 0:
                data = data.append(
                    make_row(weekday, station, 0, hour, no_converting=True),
                    ignore_index=True
                    )


# Sorts stations by position on highway.
conditions = []
choices = []
for station in stations:
    conditions.append( data["stationname"] == station )
    choices.append(len(choices))

data["order"] = np.select(conditions, choices, default=99)
data.sort_values(by="order", inplace=True)


# Visualize.
print("The frequency of an entry going faster than 100 MPH by hour, station, and weekday")
print(data)

fig = make_subplots(rows=len(weekdays), cols=1, subplot_titles=weekdays)
for i in range(len(weekdays)):
    subset = data[data["weekday"] == weekdays[i]]
    row_counter = i + 1
    fig.add_trace(
        go.Scatter(
            name=weekdays[i],
            x = subset["hour"],
            y = subset["stationname"],
            hovertext = subset["frequency"],
            mode="markers",
            marker=dict(
                size=20,
                color= subset["frequency"],
                colorscale="Viridis",
                showscale=True,
            )
        ),
        row=row_counter, col=1
    )
    fig.update_xaxes(title_text="Instances per Hour (24-Hour)", range=[0, 23], row=row_counter, col=1)


fig.update_layout(
    title="Frequencies of speeding (over 100 MPH) per Hour by Station",
    showlegend=False,
    height=750*len(weekdays),
    font=dict(
        size=18
    )
)

fig.show()
fig.to_html("visualize1.html")


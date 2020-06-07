import pandas
import plotly.graph_objects as go
from plotly.subplots import make_subplots

final = pandas.read_csv("visualize1.csv")
final.sort_values(by="stationname", inplace=True)
print("The frequency of an entry going faster than 100 MPH by hour, station, and weekday:")
print(final)

weekdays = list(set(final["weekday"].tolist()))
fig = make_subplots(rows=len(weekdays), cols=1, subplot_titles=weekdays)
for i in range(len(weekdays)):
    subset = final[final["weekday"] == weekdays[i]]
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
    fig.update_xaxes(title_text="time (24-Hour)", range=[0, 23], row=row_counter, col=1)


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


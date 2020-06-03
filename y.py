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


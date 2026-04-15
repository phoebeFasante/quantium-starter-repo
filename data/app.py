import pandas as pd
from dash import Dash, html, dcc
import plotly.express as px

# Load cleaned data from previous task
df = pd.read_csv("formatted_sales_data.csv")

# Convert Date column to datetime
df["Date"] = pd.to_datetime(df["Date"])

# Group by date and sum sales
daily_sales = df.groupby("Date", as_index=False)["Sales"].sum()

# Sort by date
daily_sales = daily_sales.sort_values("Date")

# Create line chart
fig = px.line(
    daily_sales,
    x="Date",
    y="Sales",
    title="Pink Morsel Sales Over Time"
)

# Axis labels
fig.update_layout(
    xaxis_title="Date",
    yaxis_title="Sales",
)

# Optional: add marker for price increase date
fig.add_vline(
    x="2021-01-15",
    line_dash="dash",
    line_color="red"
)

app = Dash(__name__)

app.layout = html.Div(
    style={"padding": "20px", "fontFamily": "Arial"},
    children=[
        html.H1("Soul Foods Pink Morsel Sales Visualiser"),
        dcc.Graph(figure=fig),
    ],
)

if __name__ == "__main__":
    app.run(debug=True)
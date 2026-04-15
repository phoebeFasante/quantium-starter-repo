import pandas as pd
from dash import Dash, html, dcc, Input, Output
import plotly.express as px

# Load cleaned data
df = pd.read_csv("formatted_sales_data.csv")
df["Date"] = pd.to_datetime(df["Date"])
df = df.sort_values("Date")

app = Dash(__name__)

def build_figure(region_value: str):
    filtered_df = df.copy()

    if region_value != "all":
        filtered_df = filtered_df[filtered_df["Region"].str.lower() == region_value]

    daily_sales = (
        filtered_df.groupby("Date", as_index=False)["Sales"]
        .sum()
        .sort_values("Date")
    )

    fig = px.line(
        daily_sales,
        x="Date",
        y="Sales",
        markers=True,
    )

    fig.update_layout(
        title=f"Pink Morsel Sales Over Time ({region_value.title()})" if region_value != "all" else "Pink Morsel Sales Over Time (All Regions)",
        xaxis_title="Date",
        yaxis_title="Sales",
        plot_bgcolor="white",
        paper_bgcolor="white",
        font=dict(family="Arial, sans-serif", size=14, color="#1f2937"),
        title_font=dict(size=24),
        margin=dict(l=40, r=40, t=80, b=40),
    )

    fig.update_traces(line=dict(width=3), marker=dict(size=6))

    fig.update_xaxes(showgrid=False)
    fig.update_yaxes(showgrid=True, gridcolor="#e5e7eb")

    fig.add_vline(
        x="2021-01-15",
        line_dash="dash",
        line_color="#ef4444",
        annotation_text="Price increase",
        annotation_position="top left",
    )

    return fig


app.layout = html.Div(
    style=styles["page"],
    children=[
        html.Div(
            style=styles["container"],
            children=[
                html.H1(
                    "Soul Foods Pink Morsel Sales Dashboard",
                    style=styles["title"],
                ),
                html.P(
                    "Explore total Pink Morsel sales over time and compare performance across regions.",
                    style=styles["subtitle"],
                ),

                html.Div(
                    style=styles["controlsCard"],
                    children=[
                        html.Label("Filter by region", style=styles["label"]),
                        dcc.RadioItems(
                            id="region-filter",
                            options=[
                                {"label": "All", "value": "all"},
                                {"label": "North", "value": "north"},
                                {"label": "East", "value": "east"},
                                {"label": "South", "value": "south"},
                                {"label": "West", "value": "west"},
                            ],
                            value="all",
                            inline=True,
                            style=styles["radioGroup"],
                            labelStyle=styles["radioLabel"],
                            inputStyle=styles["radioInput"],
                        ),
                    ],
                ),

                html.Div(
                    style=styles["chartCard"],
                    children=[
                        dcc.Graph(
                            id="sales-chart",
                            figure=build_figure("all"),
                            config={"displayModeBar": False},
                        )
                    ],
                ),
            ],
        )
    ],
)


@app.callback(
    Output("sales-chart", "figure"),
    Input("region-filter", "value"),
)
def update_chart(selected_region):
    return build_figure(selected_region)


styles = {
    "page": {
        "minHeight": "100vh",
        "margin": "0",
        "padding": "40px 20px",
        "background": "linear-gradient(135deg, #eff6ff 0%, #dbeafe 35%, #bfdbfe 100%)",
        "fontFamily": "Arial, sans-serif",
    },
    "container": {
        "maxWidth": "1200px",
        "margin": "0 auto",
    },
    "title": {
        "textAlign": "center",
        "fontSize": "2.5rem",
        "fontWeight": "700",
        "color": "#111827",
        "marginBottom": "10px",
    },
    "subtitle": {
        "textAlign": "center",
        "fontSize": "1.05rem",
        "color": "#4b5563",
        "marginBottom": "30px",
    },
    "controlsCard": {
        "backgroundColor": "white",
        "padding": "20px 24px",
        "borderRadius": "18px",
        "boxShadow": "0 10px 30px rgba(0, 0, 0, 0.08)",
        "marginBottom": "24px",
    },
    "label": {
        "display": "block",
        "fontSize": "1rem",
        "fontWeight": "600",
        "color": "#1f2937",
        "marginBottom": "14px",
    },
    "radioGroup": {
        "display": "flex",
        "gap": "18px",
        "flexWrap": "wrap",
    },
    "radioLabel": {
        "marginRight": "16px",
        "fontSize": "0.95rem",
        "color": "#374151",
        "backgroundColor": "#f9fafb",
        "padding": "10px 14px",
        "borderRadius": "999px",
        "border": "1px solid #e5e7eb",
        "cursor": "pointer",
    },
    "radioInput": {
        "marginRight": "8px",
    },
    "chartCard": {
        "backgroundColor": "white",
        "padding": "20px",
        "borderRadius": "18px",
        "boxShadow": "0 10px 30px rgba(0, 0, 0, 0.08)",
    },
}


if __name__ == "__main__":
    app.run(debug=True)
# This creates the page for displaying data visualizations.
import json
from pathlib import Path

import pandas as pd
import plotly.express as px
import streamlit as st

BASE_DIR = Path(__file__).resolve().parent.parent
with open(BASE_DIR / "data.json", "r", encoding="utf-8") as f:
    data = json.load(f)
    
df = pd.DataFrame(data["data_points"])
# PAGE CONFIGURATION
st.set_page_config(
    page_title="Visuals",
    page_icon="📈",
)

# PAGE TITLE
st.title("Data Visualizations 📈")




# PART 1: GRAPHS FROM data.json
# --- YOUR CODE GOES HERE ---
prices = df.pivot(index="ticker", columns="year", values="price")
first_price = prices.bfill(axis=1).iloc[:, 0]   # first available price (handles Sandisk's missing 2024)
change = ((prices["2026 YTD"] / prices["2025"] - 1) * 100).round(2)
st.subheader("Price Change from Jan 1, 2025 to 2026 YTD (%)")
st.caption("Prices as of 10/10/2026. Source: Yahoo Finance.")
st.bar_chart(change)
st.subheader("Details:")
st.write("As seen in the bar chart, the leading stock performer from Jan 1, 2025 to 2026 YTD is Micron, with a YTD return 1133.07%. This is due to hyperscale data centers needing massive amounts of high-capacity enterprise solid-state drives (SSDs) and flash memory for AI model training and data storage, which is what Micron produces")
st.write("Microsoft lagged despite its YTD return of 10.6%. This is due to massive capital expenditures(as high as 190 billion), and high reliance on OpenAI, which just announced a revenue that was $20 billion short of expected revenue.")


st.subheader("Compare Cumulative Stock Prices Over Time")

tickers = sorted(df["ticker"].unique())

# Set the default selection once
if "selected_tickers" not in st.session_state:
    st.session_state.selected_tickers = tickers[:3]

# The key links the widget to session state, so the choice persists across reruns
st.multiselect("Choose stocks to compare:", tickers, key="selected_tickers")

filtered = df[df["ticker"].isin(st.session_state.selected_tickers)]

if filtered.empty:
    st.info("Pick at least one stock to see the chart.")
else:
    fig = px.line(
        filtered,
        x="year",
        y="price",
        color="ticker",
        markers=True,
        title="Stock Price by Period",
        labels = {"year": "Period", "price": "Stock Price (USD)", "ticker": "Ticker"}
    )
    fig.update_xaxes(type="category")  # show whole years only
    st.plotly_chart(fig)




# PART 2: GRAPHS FROM data.csv
# --- YOUR CODE GOES HERE ---
st.header("Community Predictions (from the Survey)")

crowd = pd.read_csv(BASE_DIR / "data.csv")

if crowd.empty:
    st.info("No survey responses yet. Submit one on the Survey page!")
else:
    # ---------- STATIC visualization: scatter plot, no widgets ----------
    st.subheader("All Responses: Prediction vs. Conviction")
    fig_scatter = px.scatter(
        crowd,
        x="conviction",
        y="predicted_return",
        color="sector",
        hover_name="ticker",
        title="Predicted 12-Month Return vs. Conviction",
        labels={
            "conviction": "Conviction (1-5)",
            "predicted_return": "Predicted 12-Month Return (%)",
            "sector": "Sector",
        },
    )
    fig_scatter.update_xaxes(dtick=1)
    st.plotly_chart(fig_scatter)

    # ---------- DYNAMIC visualization: bar chart with widgets + session state ----------
    st.subheader("Explore Results by Ticker")
    sectors = sorted(crowd["sector"].unique())

    if "crowd_sectors" not in st.session_state:
        st.session_state.crowd_sectors = sectors
    if "crowd_metric" not in st.session_state:
        st.session_state.crowd_metric = "Average predicted return (%)"

    st.multiselect("Filter by sector:", sectors, key="crowd_sectors")
    st.radio(
        "Chart shows:",
        ["Average predicted return (%)", "Average conviction (1-5)", "Number of responses"],
        key="crowd_metric",
    )

    filtered = crowd[crowd["sector"].isin(st.session_state.crowd_sectors)]

    if filtered.empty:
        st.info("Pick at least one sector to see the chart.")
    else:
        summary = filtered.groupby("ticker").agg(
            avg_prediction=("predicted_return", "mean"),
            avg_conviction=("conviction", "mean"),
            responses=("ticker", "count"),
        ).reset_index()

        column_for = {
            "Average predicted return (%)": "avg_prediction",
            "Average conviction (1-5)": "avg_conviction",
            "Number of responses": "responses",
        }
        y_col = column_for[st.session_state.crowd_metric]

        fig_crowd = px.bar(
            summary,
            x="ticker",
            y=y_col,
            color="ticker",
            title="Community Survey Results by Ticker",
            labels={"ticker": "Ticker", y_col: st.session_state.crowd_metric},
        )
        st.plotly_chart(fig_crowd)
        fig_scatter = px.scatter(
            crowd, x="conviction", y="predicted_return", color="sector", hover_name="ticker",
            title="Predicted Return vs. Conviction (All Responses)",
            labels={"conviction": "Conviction (1-5)", "predicted_return": "Predicted 12-Month Return (%)"},
        )
        st.plotly_chart(fig_scatter)

    # ---------- ANALYSIS (computed from the CSV, so it stays accurate) ----------
    st.subheader("Analysis")
    avg_by_ticker = crowd.groupby("ticker")["predicted_return"].mean()
    most_bullish = avg_by_ticker.idxmax()
    most_bearish = avg_by_ticker.idxmin()
    st.write(
        f"Across {len(crowd)} survey responses, the most bullish ticker is {most_bullish} "
        f"(average prediction {avg_by_ticker[most_bullish]:.1f}%), while {most_bearish} is the "
        f"most bearish ({avg_by_ticker[most_bearish]:.1f}%). Average conviction overall is "
        f"{crowd['conviction'].mean():.1f} out of 5."
    )
    # Add 1-2 sentences of your own interpretation of the scatter plot here.

import streamlit as st
import pandas as pd
import plotly.express as px

# Page Config
st.set_page_config(
    page_title="Mutual Fund Analysis Dashboard",
    page_icon="📈",
    layout="wide"
)

# Title
st.title("📈 Mutual Fund Analysis Dashboard")
st.markdown("Analyze Mutual Funds AMC-wise")

# Load Data
@st.cache_data
def load_data():
    df = pd.read_csv("mutual_funds_india.csv")
    return df

df = load_data()

# Sidebar
st.sidebar.header("Filters")

amc_list = sorted(df["AMC_name"].dropna().unique())

selected_amc = st.sidebar.selectbox(
    "Select AMC",
    amc_list
)

# Filter Data
filtered_df = df[df["AMC_name"] == selected_amc]

# Header
st.subheader(f"Analysis for {selected_amc}")

# KPIs
col1, col2, col3, col4 = st.columns(4)

with col1:
    st.metric(
        "Total Funds",
        filtered_df.shape[0]
    )

with col2:
    st.metric(
        "Avg 1 Year Return",
        f"{filtered_df['return_1yr'].mean():.2f}%"
    )

with col3:
    st.metric(
        "Avg 3 Year Return",
        f"{filtered_df['return_3yr'].mean():.2f}%"
    )

with col4:
    st.metric(
        "Avg 5 Year Return",
        f"{filtered_df['return_5yr'].mean():.2f}%"
    )

st.divider()

# Return Analysis
tab1, tab2, tab3, tab4 = st.tabs(
    ["1 Year Return", "5 Year Return", "Fund Ratings", "Categories"]
)

with tab1:
    st.subheader("1 Year Return Analysis")

    fig = px.bar(
        filtered_df.sort_values("return_1yr", ascending=False),
        x="Mutual Fund Name",
        y="return_1yr",
        color="return_1yr",
        title="1 Year Returns"
    )

    fig.update_layout(
        xaxis_tickangle=-90,
        height=600
    )

    st.plotly_chart(fig, use_container_width=True)

with tab2:
    st.subheader("5 Year Return Analysis")

    fig = px.bar(
        filtered_df.sort_values("return_5yr", ascending=False),
        x="Mutual Fund Name",
        y="return_5yr",
        color="return_5yr",
        title="5 Year Returns"
    )

    fig.update_layout(
        xaxis_tickangle=-90,
        height=600
    )

    st.plotly_chart(fig, use_container_width=True)

with tab3:
    st.subheader("Fund Rating Distribution")

    rating_counts = (
        filtered_df["fund_rating"]
        .value_counts()
        .reset_index()
    )

    rating_counts.columns = ["Rating", "Count"]

    fig = px.pie(
        rating_counts,
        names="Rating",
        values="Count",
        title="Fund Ratings"
    )

    st.plotly_chart(fig, use_container_width=True)

with tab4:
    st.subheader("Category Distribution")

    category_counts = (
        filtered_df["category"]
        .value_counts()
        .reset_index()
    )

    category_counts.columns = ["Category", "Count"]

    fig = px.bar(
        category_counts,
        x="Category",
        y="Count",
        color="Count"
    )

    fig.update_layout(
        xaxis_tickangle=-45
    )

    st.plotly_chart(fig, use_container_width=True)

st.divider()

# Top Performers
st.subheader("🏆 Top 10 Funds")

return_type = st.selectbox(
    "Select Return Type",
    ["return_1yr", "return_3yr", "return_5yr"]
)

top_funds = (
    filtered_df
    .sort_values(return_type, ascending=False)
    .head(10)
)

fig = px.bar(
    top_funds,
    x="Mutual Fund Name",
    y=return_type,
    color=return_type
)

fig.update_layout(
    xaxis_tickangle=-45,
    height=500
)

st.plotly_chart(fig, use_container_width=True)

st.divider()

# Raw Data
st.subheader("📋 Mutual Fund Data")

search = st.text_input(
    "Search Fund Name"
)

if search:
    display_df = filtered_df[
        filtered_df["Mutual Fund Name"]
        .str.contains(search, case=False, na=False)
    ]
else:
    display_df = filtered_df

st.dataframe(
    display_df,
    use_container_width=True
)

# Download Button
csv = display_df.to_csv(index=False)

st.download_button(
    "⬇ Download Filtered Data",
    csv,
    file_name=f"{selected_amc}_funds.csv",
    mime="text/csv"
)

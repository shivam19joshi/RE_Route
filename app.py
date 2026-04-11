import streamlit as st
import pandas as pd
import numpy as np
import folium
from streamlit_folium import st_folium
from sklearn.ensemble import RandomForestRegressor
import plotly.express as px

st.set_page_config(layout="wide")
st.title("🚍 RouteWise - AI Transport Optimization System")

# -----------------------------
# 1. Generate Smart Dataset
# -----------------------------
np.random.seed(42)

routes = ["Route A", "Route B", "Route C"]

data = pd.DataFrame({
    "hour": np.tile(np.arange(0, 24), 30),
    "day": np.repeat(np.arange(1, 31), 24),
    "route": np.random.choice(routes, 720),
    "lat": np.random.uniform(21.10, 21.20, 720),
    "lon": np.random.uniform(79.05, 79.15, 720),
    "passengers": np.random.randint(20, 200, 720)
})

# -----------------------------
# 2. Feature Engineering
# -----------------------------
data["is_peak"] = data["hour"].apply(lambda x: 1 if 7 <= x <= 10 or 17 <= x <= 20 else 0)

X = pd.get_dummies(data[["hour", "day", "route", "is_peak"]])
y = data["passengers"]

model = RandomForestRegressor()
model.fit(X, y)

# -----------------------------
# 3. Sidebar Controls
# -----------------------------
st.sidebar.header("🔍 Controls")

selected_route = st.sidebar.selectbox("Select Route", routes)
hour = st.sidebar.slider("Hour", 0, 23, 9)
day = st.sidebar.slider("Day", 1, 30, 5)

is_peak = 1 if (7 <= hour <= 10 or 17 <= hour <= 20) else 0

input_df = pd.DataFrame({
    "hour": [hour],
    "day": [day],
    "route": [selected_route],
    "is_peak": [is_peak]
})

input_encoded = pd.get_dummies(input_df)
input_encoded = input_encoded.reindex(columns=X.columns, fill_value=0)

prediction = model.predict(input_encoded)[0]

# -----------------------------
# 4. KPI Section
# -----------------------------
col1, col2, col3 = st.columns(3)

col1.metric("🧍 Predicted Demand", int(prediction))

def status(p):
    if p > 150:
        return "Overcrowded 🚨"
    elif p > 80:
        return "Moderate ⚠️"
    return "Low ✅"

col2.metric("🚦 Status", status(prediction))
col3.metric("⏰ Hour", hour)

# -----------------------------
# 5. Smart Suggestions
# -----------------------------
st.subheader("🧠 AI Recommendations")

if prediction > 150:
    st.error("👉 Add 2-3 extra buses & introduce express route.")
elif prediction > 80:
    st.warning("👉 Monitor demand & optimize stops.")
else:
    st.success("👉 Reduce frequency to save fuel cost.")

# -----------------------------
# 6. Map Visualization
# -----------------------------
st.subheader("🗺️ Live Route Map")

m = folium.Map(location=[21.1458, 79.0882], zoom_start=12)

filtered = data[data["route"] == selected_route].sample(50)

for _, row in filtered.iterrows():
    color = "red" if row["passengers"] > 150 else "green"
    folium.CircleMarker(
        location=[row["lat"], row["lon"]],
        radius=5,
        color=color,
        fill=True
    ).add_to(m)

st_folium(m, width=700)

# -----------------------------
# 7. Heatmap Chart
# -----------------------------
st.subheader("🔥 Demand Heatmap")

heat_data = data.groupby(["hour", "route"])["passengers"].mean().reset_index()

fig = px.density_heatmap(
    heat_data,
    x="hour",
    y="route",
    z="passengers",
    title="Passenger Density"
)

st.plotly_chart(fig)

# -----------------------------
# 8. What-If Simulation
# -----------------------------
st.subheader("🔮 What-If Simulation")

extra_buses = st.slider("Add Extra Buses", 0, 5, 1)

new_load = prediction / (1 + extra_buses * 0.6)

st.write(f"Adjusted Load: {int(new_load)} passengers")

if new_load < 80:
    st.success("✅ Overcrowding Solved")
else:
    st.error("❌ Still Needs Optimization")

# -----------------------------
# 9. Route Comparison
# -----------------------------
st.subheader("📊 Route Comparison")

route_avg = data.groupby("route")["passengers"].mean().reset_index()

fig2 = px.bar(route_avg, x="route", y="passengers", title="Avg Demand per Route")
st.plotly_chart(fig2)

# -----------------------------
# 10. Raw Data
# -----------------------------
with st.expander("📂 View Dataset"):
    st.dataframe(data)

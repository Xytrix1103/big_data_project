import streamlit as st
import plotly.express as px
import pandas as pd
import json

st.header("Vaccination")

# Load GeoJSON file
with open('geojson/malaysia.districts.geojson', 'r') as f:
    geojson_data = json.load(f)

# Sample data for demonstration (replace with your own data)
data = {
    'state': ['Johor', 'Selangor', 'Penang'],
    'value': [100, 200, 300]  # Example values for choropleth coloring
}

df = pd.DataFrame(data)

# Sidebar filter by states (replace with actual list of states from your GeoJSON)
selected_state = st.sidebar.selectbox("Select State", df['state'].unique())

# Filter data by selected state
state_data = df[df['state'] == selected_state]

# Plotly Choropleth map
fig = px.choropleth_mapbox(
    state_data,
    geojson=geojson_data,
    locations='state',
    featureidkey='properties.name',  # GeoJSON property that identifies regions
    color='value',
    hover_name='state',
    hover_data={'value': True, 'state': False},
    mapbox_style="carto-positron",
    center={"lat": 4.2105, "lon": 101.9758},  # Centered roughly on Malaysia
    zoom=5,
    opacity=0.7,
    labels={'value': 'Value'},
    color_continuous_scale=px.colors.sequential.Plasma
)

fig.update_layout(margin={"r":0,"t":0,"l":0,"b":0})

st.plotly_chart(fig)

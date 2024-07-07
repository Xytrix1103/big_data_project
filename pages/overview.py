from data.mongodb import vax_district, population_district
import streamlit as st
import plotly.express as px
import pandas as pd
import json

# Load Malaysia district GeoJSON data
with open('data/geojson/malaysia.districts.geojson') as f:
    malaysia_district_geojson = json.load(f)

# Calculate vaccination rates
def calculate_vaccination_rates(vax_district, population_district):
    # Merge the data on the 'district' column
    merged_data = pd.merge(vax_district, population_district, on='district')
    
    # Multiply population by 1000
    merged_data['population'] = merged_data['population'] * 1000
    
    # Calculate vaccination rate
    merged_data['vaccination_rate'] = (merged_data['cumul_full'] / merged_data['population']) * 100
    
    # Return relevant columns
    return merged_data[['state_x', 'district', 'vaccination_rate']]

# Extract state and district dataframes
def extract_states_and_districts(vax_district):
    # Initialize an empty dictionary to store states and districts
    states_districts = {}

    # Iterate over unique states in the DataFrame
    for state in vax_district['state'].unique():
        # Filter districts for the current state
        districts = list(vax_district[vax_district['state'] == state]['district'])
        
        # Append the state and its districts to the dictionary
        states_districts[state] = districts

    # Return the dictionary
    return states_districts

# Create a choropleth map
def plot_vaccination_rates(vaccination_rates_df, geojson_data):
    fig = px.choropleth_mapbox(
        vaccination_rates_df,
        geojson=geojson_data,
        locations='district',
        featureidkey='properties.NAME_2',
        color='vaccination_rate',
        color_continuous_scale='Viridis',
        range_color=(0, 100),
        mapbox_style='carto-positron',
        zoom=5,
        center={'lat': 4.2105, 'lon': 101.9758},
        opacity=0.5,
        labels={'vaccination_rate': 'Vaccination Rate (%)'}
    )

    # Update the layout
    fig.update_layout(margin={"r":0,"t":0,"l":0,"b":0})
    st.plotly_chart(fig)
    
# Sidebar selection
all_states = ["All States"] + list(vax_district['state'].unique())
selected_state = st.sidebar.selectbox("Select State", all_states)

# Filter data based on selected state
if selected_state == "All States":
    state_data = vax_district
else:
    state_data = vax_district[vax_district['state'] == selected_state]

# Display the title and description
st.title("Vaccination Rates by District in each State in Malaysia")
st.markdown("This page displays the vaccination rates by district in each state in Malaysia.")

# Calculate vaccination rates
vaccination_rates_df = calculate_vaccination_rates(state_data, population_district)

# Display the vaccination rates DataFrame
plot_vaccination_rates(vaccination_rates_df, malaysia_district_geojson)
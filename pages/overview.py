from data.mongodb import vax_district, population_district
import streamlit as st
import numpy as np
import pandas as pd
import plotly.express as px
import json
from data.mongodb import cases_malaysia, hospital, icu, deaths_malaysia, vax_malaysia, cases_state

# Set page configuration
st.set_page_config(
    page_title='Overview Dashboard',
    page_icon='📊',
    layout='wide'
)

# Title and description
st.header('COVID-19', divider='rainbow')
st.markdown('This page provides a summarised view of the pandemic in Malaysia.')

st.divider()

# Load data from MongoDB
cases_malaysia['date'] = pd.to_datetime(cases_malaysia['date'])
hospital['date'] = pd.to_datetime(hospital['date'])
icu['date'] = pd.to_datetime(icu['date'])
deaths_malaysia['date'] = pd.to_datetime(deaths_malaysia['date'])
vax_malaysia['date'] = pd.to_datetime(vax_malaysia['date'])
cases_state['date'] = pd.to_datetime(cases_state['date'])

# Calculate total cases
total_cases = cases_malaysia['cases_new'].sum()
# Calculate total covid admissions
total_admissions = hospital['admitted_covid'].sum()
# Calculate total ICU admissions
total_icu = icu['icu_covid'].sum()
# Calculate total deaths
total_deaths = deaths_malaysia['deaths_new'].sum()
# Calculate total full vaccinations
total_vax = vax_malaysia['cumul_full'].max()
# Get the latest date 
latest_date = cases_malaysia['date'].max().strftime('%Y-%m-%d')
# Get sum of discharged COVID patients
total_discharged = cases_malaysia['cases_recovered'].sum()
# Get sum of cases_unvax
total_unvax = cases_malaysia['cases_unvax'].sum()
# Get sum of cases_partial
total_partial = cases_malaysia['cases_pvax'].sum()
# Get sum of cases_full
total_full = cases_malaysia['cases_fvax'].sum()
# Get the sum of cases_new for each state
cases_sum_by_state = cases_state.groupby('state')['cases_new'].sum()

# Format numbers with commas
total_cases = f"{total_cases:,}"
total_admissions = f"{total_admissions:,}"
total_icu = f"{total_icu:,}"
total_deaths = f"{total_deaths:,}"
total_vax = f"{total_vax:,}"
total_discharged = f"{total_discharged:,}"
total_unvax = f"{total_unvax:,}"
total_partial = f"{total_partial:,}"
total_full = f"{total_full:,}"

# List of Malaysian states
states = [
    'Johor', 'Kedah', 'Kelantan', 'Melaka', 'Negeri Sembilan', 'Pahang', 'Pulau Pinang', 
    'Perak', 'Perlis', 'Sabah', 'Sarawak', 'Selangor', 'Terengganu', 'W.P. Kuala Lumpur', 
    'W.P. Labuan', 'W.P. Putrajaya'
]

# Filtered data for progress bars
def get_filtered_data(data_category):
    return cases_state.groupby('state')[data_category].sum().reindex(states)

with st.container():
    col1, col2, = st.columns([0.80, 0.20], gap='medium', vertical_alignment='bottom')
    with col1:
        st.subheader('Summary of COVID-19 situation in Malaysia', divider='blue')
    with col2:
        st.write(f'Last updated: {latest_date}')

with st.container(border=True):
    malaysiaCol, statesCol = st.columns([0.6, 0.4], gap='medium', vertical_alignment='center')
    with malaysiaCol:
        with st.container():
            col1, col2, col3, col4, col5 = st.columns([1, 0.3, 1, 0.3, 1], gap='medium', vertical_alignment='center')
            with col1:
                st.metric(':face_with_thermometer: Total Cases', total_cases)
                with st.expander('Details'):
                    st.metric('Unvaccinated Cases', total_unvax)
                    st.metric('Partially Vaccinated Cases', total_partial)
                    st.metric('Fully Vaccinated Cases', total_full)
            with col2:
                st.header(':arrow_right:')
            with col3:
                st.metric(':hospital: Total Hospital Admissions', total_admissions)
                st.metric(':bed: Total ICU Admissions', total_icu)
                st.metric(':syringe: Total Full Vaccinations', total_vax)
            with col4:
                st.header(':arrow_right:')
                st.header(':arrow_right:')
            with col5:
                st.metric(':shield: Total Recovered', total_discharged)
                st.metric(':skull: Total Deaths', total_deaths)
    with statesCol:
        # Selected data category (default is 'cases_new')
        category_labels = {
            'cases_new': 'New Cases',
            'cases_recovered': 'Recovered Cases',
            'cases_unvax': 'Unvaccinated Cases',
            'cases_pvax': 'Partially Vaccinated Cases',
            'cases_fvax': 'Fully Vaccinated Cases'
        }
        selected_category = st.radio(
            "Select Data Category", 
            list(category_labels.keys()), 
            format_func=lambda x: category_labels[x],
            index=0, 
            horizontal=True
        )
        # Get data for selected category
        filtered_data = get_filtered_data(selected_category)

        # Sort states by descending order of values
        sorted_states = filtered_data.sort_values(ascending=False).index.tolist()

        max_value = filtered_data.max() if filtered_data.max() != 0 else 1 
        for state in sorted_states:
            state_row = st.columns([0.20, 0.20, 0.6])
            state_row[0].markdown(f"<span style='color:yellow'>{state}</span>", unsafe_allow_html=True)
            value = filtered_data[state]
            state_row[1].write(f"{value:,}")
            state_row[2].progress(value / max_value)
        
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

# Display the title and description
st.subheader("Vaccination Rates by District in each State in Malaysia", divider='blue')

with st.container():
    col1, col2 = st.columns([0.3, 0.7], gap='medium', vertical_alignment='center')
    with col1:
        all_states = ["All States"] + list(vax_district['state'].unique())
        selected_state = st.selectbox("Select State", all_states)

# Filter data based on selected state
if selected_state == "All States":
    state_data = vax_district
else:
    state_data = vax_district[vax_district['state'] == selected_state]

# Calculate vaccination rates
vaccination_rates_df = calculate_vaccination_rates(state_data, population_district)

# Display the vaccination rates DataFrame
plot_vaccination_rates(vaccination_rates_df, malaysia_district_geojson)

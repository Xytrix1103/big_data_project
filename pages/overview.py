import streamlit as st
import numpy as np
import pandas as pd
from data.mongodb import cases_malaysia, hospital, icu, deaths_malaysia, vax_malaysia, cases_state, vax_state

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
   col1, col2, = st.columns([0.85, 0.15], gap='medium', vertical_alignment='bottom')
   with col1:
      st.subheader('Summary of COVID-19 situation in Malaysia', divider='blue')
   with col2:
      st.write(f'Last updated: {latest_date}')

with st.container(border=True):
   malaysiaCol, statesCol = st.columns([0.6, 0.4], gap='medium', vertical_alignment='center')
   with malaysiaCol:
      with st.container():
         col1, col2, col3, col4, col5 = st.columns([1, 0.5, 1, 0.5, 1], gap='medium', vertical_alignment='center')
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

      max_value = filtered_data.max() if filtered_data.max() != 0 else 1  # To avoid division by zero
      for state in states:
         state_row = st.columns([0.25, 0.15, 0.6])
         state_row[0].markdown(f"<span style='color:yellow'>{state}</span>", unsafe_allow_html=True)
         value = filtered_data[state]
         state_row[1].write(f"{value:,}")
         state_row[2].progress(value / max_value)
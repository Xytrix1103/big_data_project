import joblib
import pandas as pd
import plotly.express as px
import streamlit as st
from plotly.graph_objs import Figure

from data.mongodb import cases_malaysia, cases_state

# Set page configuration
st.set_page_config(
    page_title='COVID-19 Cases Dashboard',
    page_icon='🦠',
    layout='wide'
)

# Title and description
st.header('COVID-19 Cases Dashboard', divider='rainbow')
st.markdown('This page displays the new COVID-19 cases by date for each state and the whole of Malaysia.')

# Plot the Malaysia data
fig_malaysia = px.line(cases_malaysia, x='date', y='cases_new', title='New COVID-19 Cases in Malaysia')
fig_malaysia.update_layout(xaxis_title='Date', yaxis_title='New Cases')

# Calculate summary statistics for Malaysia
total_cases_malaysia = cases_malaysia['cases_new'].sum()
average_daily_cases_malaysia = cases_malaysia['cases_new'].mean()
max_daily_cases_malaysia = cases_malaysia['cases_new'].max()

# Plot the Malaysia data and statistics for new cases
with st.container():
    st.subheader('Malaysia COVID-19 Cases Overview')
    col1, col2 = st.columns([3, 1], gap='medium', vertical_alignment='center')
    with col1:
        st.plotly_chart(fig_malaysia, use_container_width=True)
    with col2:
        st.subheader('Malaysia Statistics')
        st.metric('Total Cases', f'{total_cases_malaysia:,}')
        st.metric('Average Daily Cases', f'{average_daily_cases_malaysia:.2f}')
        st.metric('Highest Single-Day Increase', f'{max_daily_cases_malaysia:,}')

st.divider()

# Add bar chart for age groups below Malaysia cases graph
age_groups = ['cases_0_4', 'cases_5_11', 'cases_12_17', 'cases_18_29', 'cases_30_39', 'cases_40_49', 'cases_50_59', 'cases_60_69',
              'cases_70_79', 'cases_80']
total_cases_by_age = cases_malaysia[age_groups].sum().reset_index()
total_cases_by_age.columns = ['Age Group', 'Total Cases']
# Mapping dictionary for age group labels
age_group_labels = {
    'cases_0_4': '0-4',
    'cases_5_11': '5-11',
    'cases_12_17': '12-17',
    'cases_18_29': '18-29',
    'cases_30_39': '30-39',
    'cases_40_49': '40-49',
    'cases_50_59': '50-59',
    'cases_60_69': '60-69',
    'cases_70_79': '70-79',
    'cases_80': '80+'
}

# Define the order of age groups
age_group_order = ['0-4', '5-11', '12-17', '18-29', '30-39', '40-49', '50-59', '60-69', '70-79', '80+']

# Update the Age Group column using the mapping dictionary
total_cases_by_age['Age Group'] = total_cases_by_age['Age Group'].map(age_group_labels)

fig_age = px.bar(total_cases_by_age, x='Age Group', y='Total Cases', title='Total New Cases by Age Group in Malaysia')
fig_age.update_layout(xaxis_title='Age Group', yaxis_title='Total Cases')

# Calculate percentages
total_cases_by_age['Percentage'] = (total_cases_by_age['Total Cases'] / total_cases_by_age['Total Cases'].sum()) * 100

# Sort data by Age Group
total_cases_by_age = total_cases_by_age.sort_values(by='Age Group')

# Plot pie chart
fig_pie = px.pie(total_cases_by_age, values='Percentage', names='Age Group', title='Percentage of Total Cases by Age Group',
                 category_orders={'Age Group': age_group_order})
fig_pie.update_traces(textposition='inside', textinfo='percent+label')

# Plot the Malaysia data and statistics by age group
with st.container():
    st.subheader('Malaysia COVID-19 Cases by Age Group Overview')
    col1, col2 = st.columns([3, 2], gap='medium', vertical_alignment='center')
    with col1:
        st.plotly_chart(fig_age, use_container_width=True)
    with col2:
        st.plotly_chart(fig_pie, use_container_width=True)

st.divider()

# State selection filter
st.subheader('Filter by State')
states = cases_state['state'].unique()

with st.container():
    col1, col2 = st.columns([0.3, 0.7], gap='medium', vertical_alignment='center')
    with col1:
        selected_state = st.selectbox('Select a state to view the COVID-19 cases data.', states)

# Filter data based on selected state
filtered_state_data = cases_state[cases_state['state'] == selected_state]

# Plot the state data
fig_state = px.line(filtered_state_data, x='date', y='cases_new', title=f'New COVID-19 Cases in {selected_state}')
fig_state.update_layout(xaxis_title='Date', yaxis_title='New Cases')

# Calculate summary statistics for the selected state
total_cases_state = filtered_state_data['cases_new'].sum()
average_daily_cases_state = filtered_state_data['cases_new'].mean()
max_daily_cases_state = filtered_state_data['cases_new'].max()

# Plot the state data and statistics for new cases
with st.container():
    st.subheader('COVID-19 Cases by States Overview')
    col1, col2 = st.columns([3, 1], gap='medium', vertical_alignment='center')
    with col1:
        st.plotly_chart(fig_state, use_container_width=True)
    with col2:
        st.subheader(f'{selected_state} Statistics')
        st.metric('Total Cases', f'{total_cases_state:,}')
        st.metric('Average Daily Cases', f'{average_daily_cases_state:.2f}')
        st.metric('Highest Single-Day Increase', f'{max_daily_cases_state:,}')

# Plot the state data by vaccination status
with st.container():
    col1, col2, col3 = st.columns([2, 2, 1], gap='medium', vertical_alignment='center')
    with col1:
        fig_unvax = px.line(filtered_state_data, x='date', y='cases_unvax', title=f'New Unvaccinated COVID-19 Cases in {selected_state}')
        fig_unvax.update_layout(xaxis_title='Date', yaxis_title='Unvaccinated Cases')
        st.plotly_chart(fig_unvax, use_container_width=True)
    with col2:
        fig_fvax = px.line(filtered_state_data, x='date', y='cases_fvax', title=f'New Fully Vaccinated COVID-19 Cases in {selected_state}')
        fig_fvax.update_layout(xaxis_title='Date', yaxis_title='Fully Vaccinated Cases')
        st.plotly_chart(fig_fvax, use_container_width=True)
    with col3:
        st.subheader(f'Impact of Vaccination')
        total_cases_unvax = filtered_state_data['cases_unvax'].sum()
        average_daily_cases_unvax = filtered_state_data['cases_unvax'].mean()
        total_cases_fvax = filtered_state_data['cases_fvax'].sum()
        average_daily_cases_fvax = filtered_state_data['cases_fvax'].mean()
        st.metric('Total Unvaccinated Cases', f'{total_cases_unvax:,}')
        st.metric('Avg Daily Unvaccinated Cases', f'{average_daily_cases_unvax:.2f}')
        st.metric('Total Fully Vaccinated Cases', f'{total_cases_fvax:,}')
        st.metric('Avg Daily Fully Vaccinated Cases', f'{average_daily_cases_fvax:.2f}')

# Load the joblib model
model = joblib.load('models/new_cases.joblib')

# Set the number of days to forecast
forecast_days = 7

# Get the last 14 days of data
last_14_days = cases_malaysia.tail(14)

# Prepare the data for forecasting
data = pd.DataFrame(cases_malaysia)
data['date'] = pd.to_datetime(data['date'])
data['timestamp'] = (data['date'] - data['date'].min()).dt.days

# Create a dataframe for the next 7 days to forecast
next_days = pd.DataFrame({'timestamp': range(data['timestamp'].max() + 1, data['timestamp'].max() + 1 + forecast_days)})

# Predict the number of cases for the next 7 days
forecast = model.predict(next_days)
forecast = forecast.astype(int)  # Convert the forecasted values to integers

# Create a dataframe for the forecasted data
forecast_data = pd.DataFrame({
    'date': pd.date_range(start=data['date'].max() + pd.Timedelta(days=1), periods=forecast_days),
    'cases_new': forecast
})

# Plot the forecasted data with the last 14 days of data in different colors for comparison
fig_forecast = Figure()
fig_forecast.add_trace(
    px.line(
        pd.concat([last_14_days, forecast_data.head(1)]),
        x='date',
        y='cases_new',
        title='New COVID-19 Cases in Malaysia',
        color_discrete_sequence=['blue']
    ).data[0]
)
fig_forecast.add_trace(
    px.line(
        forecast_data,
        x='date',
        y='cases_new',
        title='New COVID-19 Cases in Malaysia',
        color_discrete_sequence=['red']
    ).data[0]
)
fig_forecast.update_traces(connectgaps=True)
fig_forecast.update_layout(xaxis_title='Date', yaxis_title='New Cases')

# Render the plot for the forecasted data
with st.container():
    st.subheader('7-Day Forecast of New COVID-19 Cases in Malaysia')
    st.plotly_chart(fig_forecast, use_container_width=True)

st.divider()

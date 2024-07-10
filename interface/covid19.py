import plotly.express as px
import streamlit as st

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
age_groups = ['cases_0_4', 'cases_5_11', 'cases_12_17', 'cases_18_29', 'cases_30_39', 'cases_40_49', 'cases_50_59',
              'cases_60_69',
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
fig_pie = px.pie(total_cases_by_age, values='Percentage', names='Age Group',
                 title='Percentage of Total Cases by Age Group',
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

# Function to calculate percentage change
def calculate_percentage_change(new, old):
    if old == 0:
        return "N/A"  # or some other handling for division by zero
    change = ((new - old) / old) * 100
    return f"{change:.2f}%"

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
    col1, col2, col3 = st.columns([2, 2, 1], gap='medium')
    with col1:
        fig_unvax = px.line(filtered_state_data, x='date', y='cases_unvax',
                            title=f'New Unvaccinated COVID-19 Cases in {selected_state}')
        fig_unvax.update_layout(xaxis_title='Date', yaxis_title='Unvaccinated Cases')
        st.plotly_chart(fig_unvax, use_container_width=True)

        fig_pvax = px.line(filtered_state_data, x='date', y='cases_pvax',
                            title=f'New Partially Vaccinated COVID-19 Cases in {selected_state}')
        fig_pvax.update_layout(xaxis_title='Date', yaxis_title='Partially Vaccinated Cases')
        st.plotly_chart(fig_pvax, use_container_width=True)
    with col2:
        fig_fvax = px.line(filtered_state_data, x='date', y='cases_fvax',
                           title=f'New Fully Vaccinated COVID-19 Cases in {selected_state}')
        fig_fvax.update_layout(xaxis_title='Date', yaxis_title='Fully Vaccinated Cases')
        st.plotly_chart(fig_fvax, use_container_width=True)

        fig_boost = px.line(filtered_state_data, x='date', y='cases_boost',
                            title=f'New Booster Dose COVID-19 Cases in {selected_state}')
        fig_boost.update_layout(xaxis_title='Date', yaxis_title='Booster Dose Cases')
        st.plotly_chart(fig_boost, use_container_width=True)
    with col3:
        # Display metrics with comparisons
        st.subheader(f'Impact of Vaccination in {selected_state}')
        total_cases_unvax = filtered_state_data['cases_unvax'].sum()
        average_daily_cases_unvax = filtered_state_data['cases_unvax'].mean()
        total_cases_fvax = filtered_state_data['cases_fvax'].sum()
        average_daily_cases_fvax = filtered_state_data['cases_fvax'].mean()
        total_cases_pvax = filtered_state_data['cases_pvax'].sum()
        average_daily_cases_pvax = filtered_state_data['cases_pvax'].mean()
        total_cases_boost = filtered_state_data['cases_boost'].sum()
        average_daily_cases_boost = filtered_state_data['cases_boost'].mean()

        # Calculate percentage changes
        change_pvax = calculate_percentage_change(total_cases_pvax, total_cases_unvax)
        change_fvax = calculate_percentage_change(total_cases_fvax, total_cases_unvax)
        change_boost = calculate_percentage_change(total_cases_boost, total_cases_unvax)

        st.metric('Total Unvaccinated Cases', f'{total_cases_unvax:,}')
        st.metric('Avg Daily Unvaccinated Cases', f'{average_daily_cases_unvax:.2f}')
        st.metric('Total Partially Vaccinated Cases', f'{total_cases_pvax:,}', delta=change_pvax)
        st.metric('Avg Daily Partially Vaccinated Cases', f'{average_daily_cases_pvax:.2f}')
        st.metric('Total Fully Vaccinated Cases', f'{total_cases_fvax:,}', delta=change_fvax)
        st.metric('Avg Daily Fully Vaccinated Cases', f'{average_daily_cases_fvax:.2f}')
        st.metric('Total Booster Dose Cases', f'{total_cases_boost:,}', delta=change_boost)
        st.metric('Avg Daily Booster Dose Cases', f'{average_daily_cases_boost:.2f}')

with st.container():
    col1, col2 = st.columns([3, 2], gap='medium', vertical_alignment='center')

    # Add bar chart for age groups below Malaysia cases graph
    total_state_cases_by_age = filtered_state_data[age_groups].sum().reset_index()
    total_state_cases_by_age.columns = ['Age Group', 'Total Cases']

    # Update the Age Group column using the mapping dictionary
    total_state_cases_by_age['Age Group'] = total_state_cases_by_age['Age Group'].map(age_group_labels)

    # Plot the state data by age group
    fig_state_age = px.bar(total_state_cases_by_age, x='Age Group', y='Total Cases', title=f'COVID-19 Cases by Age Group in {selected_state}')
    fig_state_age.update_layout(xaxis_title='Date', yaxis_title='Total Cases')

    # Plot the pie chart state data by age group
    total_cases_by_age_state = filtered_state_data[age_groups].sum().reset_index()
    total_cases_by_age_state.columns = ['Age Group', 'Total Cases']
    total_cases_by_age_state['Age Group'] = total_cases_by_age_state['Age Group'].map(age_group_labels)
    total_cases_by_age_state['Percentage'] = (total_cases_by_age_state['Total Cases'] / total_cases_by_age_state['Total Cases'].sum()) * 100
    total_cases_by_age_state = total_cases_by_age_state.sort_values(by='Age Group')

    fig_pie_state = px.pie(total_cases_by_age_state, values='Percentage', names='Age Group',
                           title=f'Percentage of Total Cases by Age Group in {selected_state}',
                           category_orders={'Age Group': age_group_order})
    fig_pie_state.update_traces(textposition='inside', textinfo='percent+label')

    with col1:
        st.plotly_chart(fig_state_age, use_container_width=True)
    with col2:
        st.plotly_chart(fig_pie_state, use_container_width=True)

st.divider()

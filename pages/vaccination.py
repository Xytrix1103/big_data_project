import streamlit as st
import plotly.graph_objects as go
import plotly.express as px
import pandas as pd
from data.mongodb import vax_malaysia, cases_malaysia, vax_demog_age

# Set page configuration
st.set_page_config(
    page_title='Vaccination Dashboard',
    page_icon='💉',
    layout='wide'
)

# Title and description
st.title('Vaccination Dashboard')
st.markdown('This page displays the vaccination progress in Malaysia.')

# Load data from MongoDB and convert date columns to datetime
vax_malaysia['date'] = pd.to_datetime(vax_malaysia['date'])
cases_malaysia['date'] = pd.to_datetime(cases_malaysia['date'])

# Merge datasets on date to synchronize data
merged_data = pd.merge(vax_malaysia, cases_malaysia, on='date', how='inner')

# Create a line plot for cumulative full vaccinations
fig_vaccination = px.line(merged_data, x='date', y='cumul_full',
                          title='Cumulative Full Vaccinations in Malaysia',
                          labels={'date': 'Date', 'cumul_full': 'Cumulative Full Vaccinations'},
                          template='plotly_dark')

# Create a dual-axis plot for vaccinations and new cases
fig_dual = go.Figure()

# Add vaccination data to the plot
fig_dual.add_trace(go.Scatter(x=merged_data['date'], y=merged_data['cumul_full'], name='Cumulative Full Vaccinations', yaxis='y1'))

# Add new cases data to the plot
fig_dual.add_trace(go.Scatter(x=merged_data['date'], y=merged_data['cases_new'], name='New Cases', yaxis='y2', line=dict(color='firebrick')))

# Customize the layout for dual-axis
fig_dual.update_layout(
    title='Vaccination vs New Cases Trends',
    xaxis=dict(title='Date'),
    yaxis=dict(title='Cumulative Full Vaccinations', side='left', showgrid=False),
    yaxis2=dict(title='New Cases', side='right', overlaying='y', showgrid=False),
    legend=dict(title='Data', x=1.1, y=1),
    template='plotly_dark',
    hovermode='x unified'
)

# Load data from MongoDB and convert necessary columns
vax_demog_age['date'] = pd.to_datetime(vax_demog_age['date'])

# Display the plots and summary statistics
with st.container():
    st.subheader('Cumulative Full Vaccinations')
    col1, col2 = st.columns([3, 1], gap='medium', vertical_alignment='center')

    # Plotly chart for cumulative full vaccinations
    with col1:
        st.plotly_chart(fig_vaccination, use_container_width=True)

    # Summary statistics for cumulative full vaccinations
    with col2:
        st.subheader('Summary Statistics')
        st.write(f'Highest Cumulative Full Vaccinations: {merged_data["cumul_full"].max():,.0f}')
        st.write(f'Lowest Cumulative Full Vaccinations: {merged_data["cumul_full"].min():,.0f}')
        st.write(f'Mean Cumulative Full Vaccinations: {merged_data["cumul_full"].mean():,.0f}')

st.divider()

# Display the dual-axis line chart for vaccinations and new cases
with st.container():
    st.subheader('Vaccination vs New Cases Trends')
    st.plotly_chart(fig_dual, use_container_width=True)

st.divider()

col1, col2 = st.columns([0.3, 0.7])
with col1:
    # Filter data by state (example: selecting data for a specific state)
    state = st.selectbox('Select State', vax_demog_age['state'].unique())

filtered_data = vax_demog_age[vax_demog_age['state'] == state]

# Define the age group columns to visualize
age_groups = [
    {'group': '5-11', 'columns': ['partial_5_11', 'full_5_11', 'booster_5_11', 'booster2_5_11']},
    {'group': '12-17', 'columns': ['partial_12_17', 'full_12_17', 'booster_12_17', 'booster2_12_17']},
    {'group': '18-29', 'columns': ['partial_18_29', 'full_18_29', 'booster_18_29', 'booster2_18_29']},
    {'group': '30-39', 'columns': ['partial_30_39', 'full_30_39', 'booster_30_39', 'booster2_30_39']},
    {'group': '40-49', 'columns': ['partial_40_49', 'full_40_49', 'booster_40_49', 'booster2_40_49']},
    {'group': '50-59', 'columns': ['partial_50_59', 'full_50_59', 'booster_50_59', 'booster2_50_59']},
    {'group': '60-69', 'columns': ['partial_60_69', 'full_60_69', 'booster_60_69', 'booster2_60_69']},
    {'group': '70-79', 'columns': ['partial_70_79', 'full_70_79', 'booster_70_79', 'booster2_70_79']},
    {'group': '80+', 'columns': ['partial_80', 'full_80', 'booster_80', 'booster2_80']}
]

# Aggregate data to get the total sum by state
summed_data = filtered_data.groupby('state')[[col for grp in age_groups for col in grp['columns']]].sum().reset_index()

# Melt the aggregated data to create a long format suitable for plotting
melted_data = pd.melt(summed_data, id_vars=['state'], value_vars=[col for grp in age_groups for col in grp['columns']],
                      var_name='Vaccination Type', value_name='Number of Vaccinations')

# Extract the age group from the 'Vaccination Type' column
melted_data['Age Group'] = melted_data['Vaccination Type'].apply(lambda x: x.split('_')[1])

# Map the age groups for better labeling
age_group_map = {grp['columns'][0].split('_')[1]: grp['group'] for grp in age_groups}

# Define custom colors for each vaccination status
colors = {
    'partial': '#7f24ff', 'full': '#ff24e5', 'booster': '#ff2424', 'booster2': '#ff8724',
    'partial_5_11': '#7f24ff', 'full_5_11': '#ff24e5', 'booster_5_11': '#ff2424', 'booster2_5_11': '#ff8724',
    'partial_12_17': '#7f24ff', 'full_12_17': '#ff24e5', 'booster_12_17': '#ff2424', 'booster2_12_17': '#ff8724',
    'partial_18_29': '#7f24ff', 'full_18_29': '#ff24e5', 'booster_18_29': '#ff2424', 'booster2_18_29': '#ff8724',
    'partial_30_39': '#7f24ff', 'full_30_39': '#ff24e5', 'booster_30_39': '#ff2424', 'booster2_30_39': '#ff8724',
    'partial_40_49': '#7f24ff', 'full_40_49': '#ff24e5', 'booster_40_49': '#ff2424', 'booster2_40_49': '#ff8724',
    'partial_50_59': '#7f24ff', 'full_50_59': '#ff24e5', 'booster_50_59': '#ff2424', 'booster2_50_59': '#ff8724',
    'partial_60_69': '#7f24ff', 'full_60_69': '#ff24e5', 'booster_60_69': '#ff2424', 'booster2_60_69': '#ff8724',
    'partial_70_79': '#7f24ff', 'full_70_79': '#ff24e5', 'booster_70_79': '#ff2424', 'booster2_70_79': '#ff8724',
    'partial_80': '#7f24ff', 'full_80': '#ff24e5', 'booster_80': '#ff2424', 'booster2_80': '#ff8724'
}

# Initialize Plotly figure object
fig_stacked_bar = px.bar(template="plotly_dark")

# Add each bar as an individual trace
for col in melted_data['Vaccination Type'].unique():
    group_name = col.split('_')[0]
    if group_name in ['partial', 'full', 'booster', 'booster2']:
        fig_stacked_bar.add_bar(
            x=melted_data[melted_data['Vaccination Type'] == col]['Age Group'],
            y=melted_data[melted_data['Vaccination Type'] == col]['Number of Vaccinations'],
            name=col,
            marker_color=colors[col],
            legendgroup=group_name
        )

# Update layout and labels
fig_stacked_bar.update_layout(
    title=f'Vaccination Distribution by Age Group in {state}',
    xaxis_title='Age Group',
    yaxis_title='Number of Vaccinations',
    xaxis={'categoryorder': 'array', 'categoryarray': list(age_group_map.values())}
)

# Update the x-axis tick labels to display the age groups
fig_stacked_bar.update_xaxes(ticktext=list(age_group_map.values()), tickvals=list(age_group_map.keys()))

# Rename legend labels for clarity and show only for the first 4 categories
legend_labels = {'partial': 'Partial', 'full': 'Full', 'booster': 'Booster', 'booster2': 'Booster 2'}
fig_stacked_bar.for_each_trace(lambda trace: trace.update(name=legend_labels[trace.name.split('_')[0]]) if trace.name.split('_')[0] in legend_labels else trace.update(showlegend=False))

# Display the stacked bar chart for vaccination distribution by age group
with st.container():
    st.subheader('Vaccination Distribution by Age Group')
    st.plotly_chart(fig_stacked_bar, use_container_width=True)
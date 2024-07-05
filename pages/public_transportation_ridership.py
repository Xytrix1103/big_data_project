import streamlit as st
import plotly.graph_objects as go
import plotly.express as px
import pandas as pd
from data.mongodb import ridership_headline, vax_malaysia

# Set page configuration
st.set_page_config(
    page_title='Public Transportation Ridership and Vaccination Trends',
    page_icon='🚇',
    layout='wide'
)

# Title and description
st.title('Public Transportation Ridership and Vaccination Trends Dashboard')
st.markdown('This page displays the ridership data for public transportation in Malaysia alongside the vaccination trends.')

# Load data from MongoDB and convert date columns to datetime
ridership_headline['date'] = pd.to_datetime(ridership_headline['date'])
vax_malaysia['date'] = pd.to_datetime(vax_malaysia['date'])

# Select columns for the ridership multi-line plot
columns_to_plot = ['date', 'rail_lrt_ampang', 'rail_mrt_kajang', 'rail_lrt_kj']

# Filter and prepare ridership data for the plot
plot_data = ridership_headline[columns_to_plot]

# Melt the ridership data to long format for multi-line plot
plot_data_melted = plot_data.melt(id_vars=['date'], var_name='Rail Category', value_name='Ridership')

# Create a line plot using Plotly Express
fig_ridership = px.line(plot_data_melted, x='date', y='Ridership', color='Rail Category',
                        title='Daily Public Transportation Ridership Trends',
                        labels={'date': 'Date', 'Ridership': 'Ridership Count', 'Rail Category': 'Rail Category'},
                        template='plotly_dark',
                        hover_name='Rail Category')

# Customize layout
fig_ridership.update_layout(xaxis_title='Date', yaxis_title='Ridership Count',
                            legend_title='Rail Category',
                            hovermode='x unified')

# Update trace names in the legend
fig_ridership.for_each_trace(lambda t: t.update(name=t.name.replace('_', ' ').title()))

# Filter daily ridership for the three rail categories
rail_categories = ['rail_lrt_ampang', 'rail_mrt_kajang', 'rail_lrt_kj']
daily_ridership_filtered = ridership_headline[['date'] + rail_categories]

# Find dates with lowest and highest ridership
max_ridership_index = daily_ridership_filtered[rail_categories].sum(axis=1).idxmax()
min_ridership_index = daily_ridership_filtered[rail_categories].sum(axis=1).idxmin()

max_ridership_date = daily_ridership_filtered.iloc[max_ridership_index]['date']
min_ridership_date = daily_ridership_filtered.iloc[min_ridership_index]['date']

max_ridership_value = daily_ridership_filtered.loc[max_ridership_index, rail_categories].sum()
min_ridership_value = daily_ridership_filtered.loc[min_ridership_index, rail_categories].sum()

# Merge daily ridership and vaccination data
merged_data = pd.merge(ridership_headline, vax_malaysia[['date', 'cumul_full']], on='date')

# Create a dual-axis plot for ridership and vaccination data
fig_dual = go.Figure()

# Add ridership data to the plot
for category in rail_categories:
    fig_dual.add_trace(go.Scatter(x=merged_data['date'], y=merged_data[category], name=category.replace('_', ' ').title(), yaxis='y1'))

# Add vaccination data to the plot
fig_dual.add_trace(go.Scatter(x=merged_data['date'], y=merged_data['cumul_full'], name='Cumulative Full Vaccination', yaxis='y2', line=dict(color='firebrick', dash='dot')))

# Customize the layout for dual-axis
fig_dual.update_layout(
    title='Daily Ridership and Vaccination Trends',
    xaxis=dict(title='Date'),
    yaxis=dict(title='Ridership Count', side='left', showgrid=False),
    yaxis2=dict(title='Cumulative Full Vaccination', side='right', overlaying='y', showgrid=False),
    legend=dict(title='Category', x=1.1, y=1),
    template='plotly_dark',
    hovermode='x unified'
)

# Display the plots and statistics summary for ridership data
with st.container():
    st.subheader('Public Transportation Ridership Overview')
    col1, col2 = st.columns([3, 1], gap='medium', vertical_alignment='center')
    
    # Plotly ridership chart in the first column
    with col1:
        st.plotly_chart(fig_ridership, use_container_width=True)
    
    # Statistics summary in the second column
    with col2:
        st.subheader('Ridership Peaks')
        st.metric(f'Maximum Ridership ({max_ridership_date.strftime("%B %d, %Y")})', f'{max_ridership_value:,.0f}')
        st.metric(f'Minimum Ridership ({min_ridership_date.strftime("%B %d, %Y")})', f'{min_ridership_value:,.0f}')

st.divider()

# Display the dual-axis line chart for ridership and vaccination data
with st.container():
    st.subheader('Public Transportation Ridership and Vaccination Trends')
    st.plotly_chart(fig_dual, use_container_width=True)

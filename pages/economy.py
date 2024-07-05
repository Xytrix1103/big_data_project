import streamlit as st
import plotly.express as px
import plotly.graph_objects as go
import pandas as pd
from data.mongodb import cases_malaysia, interest_rates

# Set page configuration
st.set_page_config(
    page_title='Economy Dashboard',
    page_icon='💰',
    layout='wide'
)

# Title and description
st.title('Economy Dashboard')
st.markdown('This page displays the impact of COVID-19 on bank interest rates.')

# Convert date columns to datetime
interest_rates['date'] = pd.to_datetime(interest_rates['date'])
cases_malaysia['date'] = pd.to_datetime(cases_malaysia['date'])

# Aggregate cases_malaysia data to monthly totals
cases_malaysia['month_year'] = cases_malaysia['date'].dt.to_period('M')
monthly_cases_malaysia = cases_malaysia.groupby('month_year')['cases_new'].sum().reset_index()

# Filter interest rates data
filtered_interest_rates = interest_rates[(interest_rates['bank'] == 'commercial') &
                                         (interest_rates['date'].dt.year >= 2018) &
                                         (interest_rates['rate'] == 'fdr_1mo')]

# Aggregate interest rates data to monthly averages
filtered_interest_rates['month_year'] = filtered_interest_rates['date'].dt.to_period('M')

# Merge monthly cases and interest rates data
merged_data = pd.merge(monthly_cases_malaysia, filtered_interest_rates, on='month_year', how='inner')

# Convert 'month_year' to string for Plotly serialization
merged_data['month_year'] = merged_data['month_year'].astype(str)

# Create figure with secondary y-axis
fig_dual_axis = go.Figure()

# Add traces for monthly cases
fig_dual_axis.add_trace(go.Scatter(x=merged_data['month_year'], y=merged_data['cases_new'], 
                                   mode='lines', name='Monthly Cases',
                                   yaxis='y', line=dict(color='blue')))

# Add traces for interest rates
fig_dual_axis.add_trace(go.Scatter(x=merged_data['month_year'], y=merged_data['value'], 
                                   mode='lines', name='FDR 1-Month Interest Rate',
                                   yaxis='y2', line=dict(color='red')))

# Update layout
fig_dual_axis.update_layout(
    title='Monthly Cases vs. FDR 1-Month Interest Rates in Malaysia',
    xaxis_title='Month-Year',
    yaxis_title='Monthly Cases',
    yaxis=dict(title='Monthly Cases', color='blue'),
    yaxis2=dict(title='FDR 1-Month Interest Rate (%)', overlaying='y', side='right', color='red'),
)

# Display the dual-axis line chart
with st.container():
    st.subheader('Monthly Cases vs. FDR 1-Month Interest Rates Overview (since 2020)')
    st.plotly_chart(fig_dual_axis, use_container_width=True)

st.divider()

with st.container():
    col1, col2 = st.columns([3, 1], gap='medium', vertical_alignment='center') 
    with col1:
        # Display the line graph for monthly interest rates separately
        st.subheader('Fixed Deposit Rate 1-Month Interest Rates in Malaysia')
        st.plotly_chart(px.line(filtered_interest_rates, x='date', y='value', 
                                title='FDR 1-Month Interest Rates in Malaysia', 
                                labels={'date': 'Date', 'value': 'Interest Rate (%)'}), 
                        use_container_width=True)    
    with col2:
        # Calculate summary statistics for interest rates
        lowest_interest_rate = filtered_interest_rates.loc[filtered_interest_rates['value'].idxmin()]
        highest_interest_rate = filtered_interest_rates.loc[filtered_interest_rates['value'].idxmax()]

        # Display summary statistics
        st.subheader('Interest Rates Summary')
        st.write(f'Lowest Interest Rate: {lowest_interest_rate["value"]:.2f}% in {lowest_interest_rate["month_year"].strftime("%B %Y")}')
        st.write(f'Highest Interest Rate: {highest_interest_rate["value"]:.2f}% in {highest_interest_rate["month_year"].strftime("%B %Y")}')

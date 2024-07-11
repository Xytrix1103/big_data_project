import pandas as pd
import matplotlib.pyplot as plt
from scipy.stats import spearmanr

# Load data
df_interest = pd.read_csv('https://storage.data.gov.my/finsector/interest_rates.csv')
df_cases = pd.read_csv('https://raw.githubusercontent.com/MoH-Malaysia/covid19-public/main/epidemic/cases_malaysia.csv')

# Select relevant columns
df_interest = df_interest[['date', 'bank', 'rate', 'value']]
df_cases = df_cases[['date', 'cases_new']]

# Convert date columns to datetime
df_interest['date'] = pd.to_datetime(df_interest['date'])
df_cases['date'] = pd.to_datetime(df_cases['date'])

# Before dropping missing values
initial_interest_count = len(df_interest)
initial_cases_count = len(df_cases)

df_drop_missing_interest = df_interest.dropna()
df_drop_missing_cases = df_cases.dropna()

# After dropping missing values
final_interest_count = len(df_drop_missing_interest)
final_cases_count = len(df_drop_missing_cases)

# Check number of rows before and after dropping missing values
print(f'Initial number of rows in interest data: {initial_interest_count}')
print(f'Final number of rows in interest data: {final_interest_count}')
print(f'Initial number of rows in cases data: {initial_cases_count}')
print(f'Final number of rows in cases data: {final_cases_count}')

# Make sure the date range is the same, and drop missing values
common_min_date = max(df_interest['date'].min(), df_cases['date'].min())
common_max_date = min(df_interest['date'].max(), df_cases['date'].max())

df_interest = df_interest[(df_interest['date'] >= common_min_date) & (df_interest['date'] <= common_max_date)]
df_cases = df_cases[(df_cases['date'] >= common_min_date) & (df_cases['date'] <= common_max_date)].dropna()

# Change all cases dates to day 1 of the original month
df_cases['date'] = df_cases['date'].dt.to_period('M').dt.to_timestamp()
df_cases = df_cases.groupby('date').sum().reset_index()

# Filter interest rates data to only include commercial banks with fdr_1mo rates
df_interest = df_interest[(df_interest['bank'] == 'commercial') & (df_interest['rate'] == 'fdr_1mo')]

# Only keep the relevant columns
df_interest = df_interest[['date', 'value']]
df_cases = df_cases[['date', 'cases_new']]

# Merge the two dataframes
df = pd.merge(df_interest, df_cases, on='date', how='inner')

# Calculate Spearman correlation and p-value
corr_spearman, p_value_spearman = spearmanr(df['cases_new'], df['value'])
print(f'Spearman correlation coefficient: {corr_spearman}, p-value: {p_value_spearman}')

# Plot the data
plt.figure(figsize=(10, 6))
plt.scatter(df['cases_new'], df['value'])
plt.xlabel('Monthly cases')
plt.ylabel('Interest rates')
plt.title('Correlation between number of cases and interest rates')
plt.show()
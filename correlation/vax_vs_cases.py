import pandas as pd
import matplotlib.pyplot as plt
from scipy.stats import spearmanr

# Load data
df_cases = pd.read_csv('https://raw.githubusercontent.com/MoH-Malaysia/covid19-public/main/epidemic/cases_malaysia.csv')
df_vax = pd.read_csv('https://raw.githubusercontent.com/MoH-Malaysia/covid19-public/main/vaccination/vax_malaysia.csv')

# Select relevant columns
df_cases = df_cases[['date', 'cases_new']]  # Select date and daily new cases
df_vax = df_vax[['date', 'cumul_full']]  # Select date and full vaccinations

# Convert date columns to datetime
df_cases['date'] = pd.to_datetime(df_cases['date'])
df_vax['date'] = pd.to_datetime(df_vax['date'])

# Make sure the date range is the same, and drop missing values
common_min_date = max(df_cases['date'].min(), df_vax['date'].min())
common_max_date = min(df_cases['date'].max(), df_vax['date'].max())
df_cases = df_cases[(df_cases['date'] >= common_min_date) & (df_cases['date'] <= common_max_date)].dropna()
df_vax = df_vax[(df_vax['date'] >= common_min_date) & (df_vax['date'] <= common_max_date)].dropna()

# Merge the two dataframes
df = pd.merge(df_cases, df_vax, on='date', how='inner')
print(df)

# Calculate Spearman correlation and p-value
corr_spearman, p_value_spearman = spearmanr(df['cumul_full'], df['cases_new'])
print(f'Spearman correlation coefficient: {corr_spearman}, p-value: {p_value_spearman}')

# Plot the data
plt.figure(figsize=(10, 6))
plt.scatter(df['cumul_full'], df['cases_new'])
plt.xlabel('Cumulative full vaccinations')
plt.ylabel('Daily new cases')
plt.title('Correlation between cumulative number of fully vaccinated individuals and daily new cases')
plt.show()

import pandas as pd
import matplotlib.pyplot as plt
from scipy.stats import spearmanr

# Load data
df_rides = pd.read_csv('https://storage.data.gov.my/transportation/ridership_headline.csv')
df_vax = pd.read_csv('https://raw.githubusercontent.com/MoH-Malaysia/covid19-public/main/vaccination/vax_malaysia.csv')

# Select relevant columns
df_rides = df_rides[['date', 'rail_lrt_ampang', 'rail_mrt_kajang', 'rail_lrt_kj', 'rail_monorail']]
df_vax = df_vax[['date', 'cumul_full']]

# Convert date columns to datetime
df_rides['date'] = pd.to_datetime(df_rides['date'])
df_vax['date'] = pd.to_datetime(df_vax['date'])

# Rename cumulative vaccination column
df_vax = df_vax.rename(columns={'cumul_full': 'cumul_vaxxed'})

# Before dropping missing values
initial_rides_count = len(df_rides)
initial_vax_count = len(df_vax)

df_drop_missing_rides = df_rides.dropna()
df_drop_missing_vax = df_vax.dropna()

# After dropping missing values
final_rides_count = len(df_drop_missing_rides)
final_vax_count = len(df_drop_missing_vax)

# Check number of rows before and after dropping missing values
print(f'Initial number of rows in ridership data: {initial_rides_count}')
print(f'Final number of rows in ridership data: {final_rides_count}')
print(f'Initial number of rows in vaccination data: {initial_vax_count}')
print(f'Final number of rows in vaccination data: {final_vax_count}')


# Make sure the date range is the same, and drop missing values
common_min_date = max(df_rides['date'].min(), df_vax['date'].min())
common_max_date = min(df_rides['date'].max(), df_vax['date'].max())

df_rides = df_rides[(df_rides['date'] >= common_min_date) & (df_rides['date'] <= common_max_date)].dropna()
df_vax = df_vax[(df_vax['date'] >= common_min_date) & (df_vax['date'] <= common_max_date)].dropna()

# Calculate total ridership
df_rides['daily_ridership'] = (
    df_rides['rail_lrt_ampang'] +
    df_rides['rail_mrt_kajang'] +
    df_rides['rail_lrt_kj'] +
    df_rides['rail_monorail']
)

# Only keep the relevant columns
df_rides = df_rides[['date', 'daily_ridership']]
df_vax = df_vax[['date', 'cumul_vaxxed']]

# Merge the two dataframes
df = pd.merge(df_rides, df_vax, on='date', how='inner')

print(df)

corr_spearman, p_value_spearman = spearmanr(df['cumul_vaxxed'], df['daily_ridership'])
print(f'Spearman correlation coefficient: {corr_spearman}, p-value: {p_value_spearman}')

# Plot the data
plt.figure(figsize=(10, 6))
plt.scatter(df['cumul_vaxxed'], df['daily_ridership'])
plt.xlabel('Cumulative vaccination')
plt.ylabel('Daily ridership')
plt.title('Correlation between cumulative number of fully vaccinated individuals and daily ridership')
plt.show()

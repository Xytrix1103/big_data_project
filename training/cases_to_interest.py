# Import libraries
import joblib
import pandas as pd
from matplotlib import pyplot as plt
from sklearn.model_selection import GridSearchCV

# Load data
df_interest = pd.read_csv('https://storage.data.gov.my/finsector/interest_rates.csv')
df_cases = pd.read_csv('https://raw.githubusercontent.com/MoH-Malaysia/covid19-public/main/epidemic/cases_malaysia.csv')

# Select relevant columns
df_interest = df_interest[['date', 'bank', 'rate', 'value']]
df_cases = df_cases[['date', 'cases_new']]

# Convert date columns to datetime
df_interest['date'] = pd.to_datetime(df_interest['date'])
df_cases['date'] = pd.to_datetime(df_cases['date'])
df_interest['month'] = df_interest['date'].dt.month
df_interest['year'] = df_interest['date'].dt.year
df_cases['month'] = df_cases['date'].dt.month
df_cases['year'] = df_cases['date'].dt.year

# Make sure the date range is the same, and drop missing values
common_min_date = max(df_interest['date'].min(), df_cases['date'].min())
common_max_date = min(df_interest['date'].max(), df_cases['date'].max())
df_interest = df_interest[(df_interest['date'] >= common_min_date) & (df_interest['date'] <= common_max_date)].dropna()
df_cases = df_cases[(df_cases['date'] >= common_min_date) & (df_cases['date'] <= common_max_date)].dropna()

df_interest = df_interest[(df_interest['bank'] == 'commercial') & (df_interest['rate'] == 'fdr_1mo')]

df_interest = df_interest[['month', 'year', 'value']]
df_cases = df_cases[['month', 'year', 'cases_new']]

# Group by month and year
df_cases = df_cases.groupby(['month', 'year']).sum().reset_index()

# Merge the two dataframes
df = pd.merge(df_interest, df_cases, on=['month', 'year'], how='inner')

# Calculate correlation
correlation = df['cases_new'].corr(df['value'], method='spearman')

print(f'Spearman Correlation between interest rates and daily new cases: {correlation}')

# Plot the data
plt.figure(figsize=(10, 6))
plt.scatter(df['value'], df['cases_new'])
plt.xlabel('Interest Rate')
plt.ylabel('Daily new cases')
plt.title('Correlation between interest rates and daily new cases')
plt.show()

# Perform prediction
from sklearn.ensemble import RandomForestRegressor

# Declare the model inputs and outputs
X = df[['cases_new']]
y = df['value']

# Create a random forest model
model = RandomForestRegressor()

param_grid = {
    'n_estimators': [100, 200, 300, 400, 500],
    'max_depth': [None, 10, 20, 30, 40, 50],
    'min_samples_split': [2, 5, 10],
    'min_samples_leaf': [1, 2, 4]
}

grid_search = GridSearchCV(estimator=model, param_grid=param_grid, n_jobs=-1, verbose=1, cv=5)
grid_search.fit(X, y)

print(grid_search.best_params_)
model = grid_search.best_estimator_

# Fit the model to the data
model.fit(X, y)

y_pred = model.predict(X)

from sklearn.metrics import mean_squared_error, mean_absolute_error

mse = mean_squared_error(y, y_pred)
mae = mean_absolute_error(y, y_pred)

print(f'Mean Squared Error: {mse}')
print(f'Mean Absolute Error: {mae}')

# save the model to disk
# Save the model
joblib.dump(model, '../models/cases_to_interest.joblib')

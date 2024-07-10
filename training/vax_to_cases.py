# Import libraries
import joblib
import matplotlib.pyplot as plt
import pandas as pd
from sklearn.metrics import mean_squared_error, mean_absolute_error
from sklearn.model_selection import GridSearchCV

# Load data
df_cases = pd.read_csv('https://raw.githubusercontent.com/MoH-Malaysia/covid19-public/main/epidemic/cases_malaysia.csv')
df_vax = pd.read_csv('https://raw.githubusercontent.com/MoH-Malaysia/covid19-public/main/vaccination/vax_malaysia.csv')

# Select relevant columns
df_cases = df_cases[['date', 'cases_new']]  # Select date and daily new cases
df_vax = df_vax[['date', 'cumul_full']]  # Select date and full vaccinations

df_cases = df_cases.dropna()
df_vax = df_vax.dropna()

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

# Calculate correlation
correlation = df['cumul_full'].corr(df['cases_new'], method='spearman')

# Plot the data
plt.figure(figsize=(10, 6))
plt.scatter(df['cumul_full'], df['cases_new'])
plt.xlabel('Cumulative full vaccinations')
plt.ylabel('Daily new cases')
plt.title('Correlation between cumulative number of fully vaccinated individuals and daily new cases')
plt.show()

print(
    f'Spearman Correlation between cumulative number of fully vaccinated individuals and daily new cases: {correlation}')

# Perform prediction
from sklearn.ensemble import RandomForestRegressor

# Declare the model inputs and outputs
X = df[['cumul_full']]
y = df['cases_new']

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

mse = mean_squared_error(y, y_pred)
mae = mean_absolute_error(y, y_pred)

print(f'Mean Squared Error: {mse}')
print(f'Mean Absolute Error: {mae}')

# Save the model
joblib.dump(model, '../models/vax_to_cases.joblib')

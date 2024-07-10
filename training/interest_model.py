# Import libraries
import pandas as pd
import joblib

from sklearn.ensemble import RandomForestRegressor

# Load data
df_interest = pd.read_csv('https://storage.data.gov.my/finsector/interest_rates.csv')

# Select relevant columns
df_interest = df_interest[['date', 'bank', 'rate', 'value']]

# Convert date columns to datetime
df_interest['date'] = pd.to_datetime(df_interest['date'])

df_interest = df_interest[(df_interest['date'] >= '2020-01-01')]

# train random forest model to predict interest rates based on month and year
df_interest['month'] = df_interest['date'].dt.month
df_interest['year'] = df_interest['date'].dt.year

df_interest = df_interest[(df_interest['bank'] == 'commercial') & (df_interest['rate'] == 'fdr_1mo')]

X = df_interest[['month', 'year']]
y = df_interest['value']

model = RandomForestRegressor(
    n_estimators=100,
    verbose=3,
    n_jobs=-1,
)

model.fit(X, y)

# save the model to disk
filename = '../models/interest_rates.joblib'
joblib.dump(model, filename)
print('Model saved successfully')


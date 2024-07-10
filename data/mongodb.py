import time
import pandas as pd
from pymongo import MongoClient

# Export data from MongoDB
uri = "mongodb+srv://admin:admin@bigdataproject.zcgwhyg.mongodb.net/?retryWrites=true&w=majority&appName=BigDataProject"
client = MongoClient(uri)

# Get all collections
db = client['data']
collections = db.list_collection_names()

def query_collection(collection_name, projection=None):
    start_time = time.time()
    data = pd.DataFrame(list(db[collection_name].find({}, projection)))
    end_time = time.time()
    print(f"{collection_name} query time: {end_time - start_time:.2f} seconds")
    return data

# Projections for collections
projections = {
    'cases_malaysia': {'_id': 0, 'date': 1, 'cases_new': 1, 'cases_recovered': 1, 'cases_unvax': 1, 'cases_pvax': 1, 'cases_fvax': 1,
                       'cases_0_4': 1, 'cases_5_11': 1, 'cases_12_17': 1, 'cases_18_29': 1, 'cases_30_39': 1, 'cases_40_49': 1,
                       'cases_50_59': 1, 'cases_60_69': 1, 'cases_70_79': 1, 'cases_80': 1},
    'cases_state': {'_id': 0, 'date': 1, 'state': 1, 'cases_new': 1, 'cases_unvax': 1, 'cases_fvax': 1, 'cases_recovered': 1,
                    'cases_pvax': 1, 'cases_boost': 1, 'cases_0_4': 1, 'cases_5_11': 1, 'cases_12_17': 1, 'cases_18_29': 1, 'cases_30_39': 1, 
                    'cases_40_49': 1, 'cases_50_59': 1, 'cases_60_69': 1, 'cases_70_79': 1, 'cases_80': 1},
    'interest_rates': {'_id': 0, 'date': 1, 'bank': 1, 'rate': 1, 'value': 1},
    'ridership_headline': {'_id': 0, 'date': 1, 'rail_lrt_ampang': 1, 'rail_mrt_kajang': 1, 'rail_lrt_kj': 1, 'rail_monorail': 1},
    'vax_malaysia': {'_id': 0, 'date': 1, 'cumul_full': 1},
    'vax_district': {'_id': 0, 'date': 1, 'state': 1, 'district': 1, 'cumul_full': 1},
    'vax_demog_age': {'_id': 0, 'date': 1, 'state': 1, 'partial_5_11': 1, 'full_5_11': 1, 'booster_5_11': 1, 'booster2_5_11': 1,
                      'partial_12_17': 1, 'full_12_17': 1, 'booster_12_17': 1, 'booster2_12_17': 1, 'partial_18_29': 1, 'full_18_29': 1,
                      'booster_18_29': 1, 'booster2_18_29': 1, 'partial_30_39': 1, 'full_30_39': 1, 'booster_30_39': 1, 'booster2_30_39': 1,
                      'partial_40_49': 1, 'full_40_49': 1, 'booster_40_49': 1, 'booster2_40_49': 1, 'partial_50_59': 1, 'full_50_59': 1,
                      'booster_50_59': 1, 'booster2_50_59': 1, 'partial_60_69': 1, 'full_60_69': 1, 'booster_60_69': 1, 'booster2_60_69': 1,
                      'partial_70_79': 1, 'full_70_79': 1, 'booster_70_79': 1, 'booster2_70_79': 1, 'partial_80': 1, 'full_80': 1,
                      'booster_80': 1, 'booster2_80': 1},
    'population_district': {'_id': 0, 'state': 1, 'district': 1, 'population': 1},
    'deaths_malaysia': {'_id': 0, 'date': 1, 'deaths_new': 1},
    'deaths_state': {'_id': 0, 'date': 1, 'state': 1, 'deaths_new': 1},
    'hospital': {'_id': 0, 'date': 1, 'state': 1, 'admitted_covid': 1},
    'icu': {'_id': 0, 'date': 1, 'state': 1, 'icu_covid': 1}
}

# Start time for all queries
total_start_time = time.time()

# Query data normally
cases_malaysia = query_collection('cases_malaysia', projections['cases_malaysia'])
cases_state = query_collection('cases_state', projections['cases_state'])
interest_rates = query_collection('interest_rates', projections['interest_rates'])
ridership_headline = query_collection('ridership_headline', projections['ridership_headline'])
vax_malaysia = query_collection('vax_malaysia', projections['vax_malaysia'])
vax_district = query_collection('vax_district', projections['vax_district'])
vax_demog_age = query_collection('vax_demog_age', projections['vax_demog_age'])
hospital = query_collection('hospital', projections['hospital'])
icu = query_collection('icu', projections['icu'])
deaths_malaysia = query_collection('deaths_malaysia', projections['deaths_malaysia'])
deaths_state = query_collection('deaths_state', projections['deaths_state'])
population_district = query_collection('population_district', projections['population_district'])

# End time for all queries
total_end_time = time.time()

# Print total query time
print(f"Total query time: {total_end_time - total_start_time:.2f} seconds")

# Close the connection
client.close()

# Preprocessing function
def preprocess_data(df, name):
    print(f"\nProcessing {name}...")

    # Initial count
    initial_count = len(df)
    print(f"Initial count: {initial_count}")

    # Check for missing values
    missing_values = df.isnull().sum().sum()
    print(f"Missing values: {missing_values}")

    # Drop rows with missing values
    df = df.dropna()

    # Check for duplicates
    duplicates = df.duplicated().sum()
    print(f"Duplicates: {duplicates}")

    # Drop duplicates
    df = df.drop_duplicates()

    # Final count
    final_count = len(df)
    print(f"Final count: {final_count}")

    return df

# Preprocess each dataset
cases_malaysia = preprocess_data(cases_malaysia, 'cases_malaysia')
cases_state = preprocess_data(cases_state, 'cases_state')
interest_rates = preprocess_data(interest_rates, 'interest_rates')
ridership_headline = preprocess_data(ridership_headline, 'ridership_headline')
vax_malaysia = preprocess_data(vax_malaysia, 'vax_malaysia')
vax_district = preprocess_data(vax_district, 'vax_district')
vax_demog_age = preprocess_data(vax_demog_age, 'vax_demog_age')
hospital = preprocess_data(hospital, 'hospital')
icu = preprocess_data(icu, 'icu')
deaths_malaysia = preprocess_data(deaths_malaysia, 'deaths_malaysia')
deaths_state = preprocess_data(deaths_state, 'deaths_state')
population_district = preprocess_data(population_district, 'population_district')

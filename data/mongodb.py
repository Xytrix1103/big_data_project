import pandas as pd
from pymongo import MongoClient
import time
from concurrent.futures import ThreadPoolExecutor, as_completed

cases_malaysia, cases_state, interest_rates, ridership_headline, vax_malaysia, vax_district, vax_demog_age, hospital, icu, deaths_malaysia, population_district = None, None, None, None, None, None, None, None, None, None, None

# Export data from MongoDB
uri = "mongodb+srv://admin:admin@bigdataproject.zcgwhyg.mongodb.net/?retryWrites=true&w=majority&appName=BigDataProject"
client = MongoClient(uri)

# Get all collections
db = client['data']
collections = db.list_collection_names()

def query_collection(collection_name, projection=None, skip=0, limit=0):
    start_time = time.time()
    data = pd.DataFrame(list(db[collection_name].find({}, projection).skip(skip).limit(limit)))
    end_time = time.time()
    print(f"{collection_name} query time (skip: {skip}, limit: {limit}): {end_time - start_time:.2f} seconds")
    return data

# Projections for collections
projections = {
    'cases_malaysia': {'_id': 0, 'date': 1, 'cases_new': 1, 'cases_recovered': 1, 'cases_unvax': 1, 'cases_pvax': 1, 'cases_fvax': 1, 'cases_0_4': 1, 'cases_5_11': 1, 'cases_12_17': 1, 'cases_18_29': 1, 'cases_30_39': 1, 'cases_40_49': 1, 'cases_50_59': 1, 'cases_60_69': 1, 'cases_70_79': 1, 'cases_80': 1},
    'cases_state': {'_id': 0, 'date': 1, 'state': 1, 'cases_new': 1, 'cases_unvax': 1, 'cases_fvax': 1, 'cases_recovered': 1, 'cases_pvax': 1},
    'interest_rates': {'_id': 0, 'date': 1, 'bank': 1, 'rate': 1, 'value': 1},
    'ridership_headline': {'_id': 0, 'date': 1, 'rail_lrt_ampang': 1, 'rail_mrt_kajang': 1, 'rail_lrt_kj': 1, 'rail_monorail': 1},
    'vax_malaysia': {'_id': 0, 'date': 1, 'cumul_full': 1},
    'vax_district': {'_id': 0, 'date': 1, 'state': 1, 'district': 1, 'cumul_full': 1},
    'vax_demog_age': {'_id': 0, 'date': 1, 'state': 1, 'partial_5_11': 1, 'full_5_11': 1, 'booster_5_11': 1, 'booster2_5_11': 1, 'partial_12_17': 1, 'full_12_17': 1, 'booster_12_17': 1, 'booster2_12_17': 1, 'partial_18_29': 1, 'full_18_29': 1, 'booster_18_29': 1, 'booster2_18_29': 1, 'partial_30_39': 1, 'full_30_39': 1, 'booster_30_39': 1, 'booster2_30_39': 1, 'partial_40_49': 1, 'full_40_49': 1, 'booster_40_49': 1, 'booster2_40_49': 1, 'partial_50_59': 1, 'full_50_59': 1, 'booster_50_59': 1, 'booster2_50_59': 1, 'partial_60_69': 1, 'full_60_69': 1, 'booster_60_69': 1, 'booster2_60_69': 1, 'partial_70_79': 1, 'full_70_79': 1, 'booster_70_79': 1, 'booster2_70_79': 1, 'partial_80': 1, 'full_80': 1, 'booster_80': 1, 'booster2_80': 1},
    'population_district': {'_id': 0, 'state': 1, 'district': 1, 'population': 1},
    'deaths_malaysia': {'_id': 0, 'date': 1, 'deaths_new': 1},
    'hospital': {'_id': 0, 'date': 1, 'state': 1, 'admitted_covid': 1},
    'icu': {'_id': 0, 'date': 1, 'state': 1, 'icu_covid': 1}
}

# Split data for multi-threaded queries
def split_query(collection_name, projection, num_splits=8):
    total_docs = db[collection_name].count_documents({})
    limit = total_docs // num_splits
    ranges = [(i * limit, limit) for i in range(num_splits)]
    ranges[-1] = (ranges[-1][0], total_docs - ranges[-1][0])  # Adjust the last range to cover all documents
    return ranges

# Start time for all queries
total_start_time = time.time()

# Using ThreadPoolExecutor to run queries concurrently
with ThreadPoolExecutor() as executor:
    future_to_collection = {executor.submit(query_collection, collection, projections.get(collection)): collection for collection in collections if collection in projections and collection not in ['cases_state', 'vax_demog_age', 'malaysia_district_geojson']}
    
    if 'cases_state' in collections:
        ranges = split_query('cases_state', projections['cases_state'])
        for skip, limit in ranges:
            future_to_collection[executor.submit(query_collection, 'cases_state', projections['cases_state'], skip, limit)] = 'cases_state'

    if 'vax_demog_age' in collections:
        ranges = split_query('vax_demog_age', projections['vax_demog_age'])
        for skip, limit in ranges:
            future_to_collection[executor.submit(query_collection, 'vax_demog_age', projections['vax_demog_age'], skip, limit)] = 'vax_demog_age'

    cases_state_parts = []
    vax_demog_age_parts = []

    for future in as_completed(future_to_collection):
        collection_name = future_to_collection[future]
        result = future.result()
        if collection_name == 'cases_malaysia':
            cases_malaysia = result
        elif collection_name == 'interest_rates':
            interest_rates = result
        elif collection_name == 'ridership_headline':
            ridership_headline = result
        elif collection_name == 'vax_malaysia':
            vax_malaysia = result
        elif collection_name == 'vax_district':
            vax_district = result
        elif collection_name == 'population_district':
            population_district = result
        elif collection_name == 'deaths_malaysia':
            deaths_malaysia = result
        elif collection_name == 'hospital':
            hospital = result
        elif collection_name == 'icu':
            icu = result
        elif collection_name == 'cases_state':
            cases_state_parts.append(result)
        elif collection_name == 'vax_demog_age':
            vax_demog_age_parts.append(result)

    # Combine parts for split queries
    if cases_state_parts:
        cases_state = pd.concat(cases_state_parts, ignore_index=True)
    if vax_demog_age_parts:
        vax_demog_age = pd.concat(vax_demog_age_parts, ignore_index=True)

# Close the connection
client.close()

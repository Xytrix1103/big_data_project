import pandas as pd
from pymongo import MongoClient

cases_malaysia, cases_state, interest_rates, ridership_headline, vax_malaysia, vax_district = None, None, None, None, None, None

# export data from MongoDB
uri = "mongodb+srv://admin:admin@bigdataproject.zcgwhyg.mongodb.net/?retryWrites=true&w=majority&appName=BigDataProject"
client = MongoClient(uri)

# Get all collections
db = client['data']

collections = db.list_collection_names()

if 'cases_malaysia' in collections:
    cases_malaysia = pd.DataFrame(list(db['cases_malaysia'].find()))
    cases_malaysia = cases_malaysia.drop('_id', axis=1)

if 'cases_state' in collections:
    cases_state = pd.DataFrame(list(db['cases_state'].find()))
    cases_state = cases_state.drop('_id', axis=1)

if 'interest_rates' in collections:
    interest_rates = pd.DataFrame(list(db['interest_rates'].find()))
    interest_rates = interest_rates.drop('_id', axis=1)

if 'ridership_headline' in collections:
    ridership_headline = pd.DataFrame(list(db['ridership_headline'].find()))
    ridership_headline = ridership_headline.drop('_id', axis=1)

if 'vax_malaysia' in collections:
    vax_malaysia = pd.DataFrame(list(db['vax_malaysia'].find()))
    vax_malaysia = vax_malaysia.drop('_id', axis=1)

if 'vax_district' in collections:
    vax_district = pd.DataFrame(list(db['vax_district'].find()))
    vax_district = vax_district.drop('_id', axis=1)

# Close the connection
client.close()

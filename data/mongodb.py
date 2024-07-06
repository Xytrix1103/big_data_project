import pandas as pd
from pymongo import MongoClient
import geojson

cases_malaysia, cases_state, interest_rates, ridership_headline, vax_malaysia, vax_district, vax_demog_age = None, None, None, None, None, None, None

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

if 'vax_demog_age' in collections:
    vax_demog_age = pd.DataFrame(list(db['vax_demog_age'].find()))
    vax_demog_age = vax_demog_age.drop('_id', axis=1)
    
if 'population_district' in collections:
    population_district = pd.DataFrame(list(db['population_district'].find()))
    population_district = population_district.drop('_id', axis=1)

if 'malaysia_district_geojson' in collections:
    geojson_document = db['malaysia_district_geojson'].find_one({}, {'_id': 0}) 
    if geojson_document and geojson_document.get('type') == "FeatureCollection" and 'features' in geojson_document:
        malaysia_district_geojson = geojson.loads(geojson.dumps(geojson_document)) 
    else:
        raise Exception("GeoJSON data not found or invalid format.")
else:
    raise Exception("Collection 'malaysia_district_geojson' not found in the database.")

# Close the connection
client.close()

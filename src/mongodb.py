
import pandas as pd
import requests
import json
from pymongo import MongoClient
from pprint import pprint
from pathlib import Path
import globals
import datetime

current_path = Path(__file__).parent
data_url = current_path.parent.joinpath('data')

def load_flights(db):
  
  # Load the CSV data into a pandas DataFrame
  # at the moment df_all_flights.csv is not avl in data folder, 
  # please change it to your local path to run this code

  csv_files = ['df_flights_BER_PAR_MUC_20230326_20230402.csv']
  
  collection = db.flights
  # in case you need to delete all flights data
  # collection.delete_many({})
  num_docs = collection.count_documents({})
  if num_docs == 0:
    print('\nAll documents in flights collection have been deleted')

  for file in csv_files:
    df = pd.read_csv(data_url.joinpath(file), delimiter=';')

    # Convert the DataFrame to a JSON formatted string
    json_data = json.loads(df.to_json(orient='records'))
    collection.insert_many(json_data)

  # count the total number of documents in the collection
  num_docs = collection.count_documents({})

  print(num_docs," documents have been inserted into flights collection")


def get_flights_from_db(db):

  # Find a document by a query and retrieve it
  # query = {'_id': 1}

  collection = db.flights
  document = collection.find_one()

  # Print the retrieved document
  pprint(document,  indent=4)


def load_positions(db):

  collection = db.positions

  collection.delete_many({})
  num_docs = collection.count_documents({})
  if num_docs == 0:
    print('\nAll documents in positions collection have been deleted')

  # Load the CSV data into a pandas DataFrame
  df = pd.read_csv(data_url.joinpath('airlabs_response.csv'))
  # Convert the DataFrame to a JSON formatted string
  json_data = json.loads(df.to_json(orient='records'))

  collection.insert_many(json_data)

  # count the total number of documents in the collection
  num_docs = collection.count_documents({})

  print(num_docs," documents have been inserted into positions collection")

  
def get_positions_from_db(db):

  collection = db.positions
  document = collection.find_one()

  # Print the retrieved document
  pprint(document,  indent=4)

def get_geopositions_from_airlabs(export=0):

  globals.initialize()

  my_params = {'api_key': globals.airlabs_token}

  method = 'flights'
  api_base = 'http://airlabs.co/api/v9/'

  r = requests.get(api_base + method, params = my_params).json()
  resp_list = r.get("response")
  df = pd.json_normalize(resp_list)
  df["last_update"] = df.shape[0] * [datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S")]

  if export == 1:
    df.to_csv(data_url.joinpath('airlabs_response.csv'), sep=",", index=False)

  return resp_list, df

def load_positions_from_airlabs(db):

  # Load the response of Airlabs into a pandas DataFrame
  _, df = get_geopositions_from_airlabs()

  # Convert the DataFrame to a JSON formatted string
  json_data = json.loads(df.to_json(orient='records'))

  collection = db.positions
  collection.delete_many({})
  collection.insert_many(json_data)

def main_connect_mongodb(db_name: str, function, *args, **kwargs):

  # INPUT function, *args, **kwargs
  # Connect to the MongoDB client and insert the data into a collection
  # with clause makes sure client is properly closed after it has been used

  with MongoClient("mongodb://"+ globals.mongohost +":"+globals.mongoport+"/") as client:

    db = getattr(client, db_name) # equal to db = client.air_traffic_system
    
    function(db=db, *args, **kwargs)
    # get_flights_from_db(db)
    # load_flights(db)
    # load_positions(db)
    # get_positions_from_db(db)

def _connect_mongo(host, port, username, password, db):
  """ A util for making a connection to mongo """
  
  # connecting to mongodb container
  #conn = MongoClient("mongodb://mongodb:27017/")
  #db = conn["air_traffic_system"]

  if username and password:
    mongo_uri = 'mongodb://%s:%s@%s:%s/%s' % (username, password, host, port, db)
    conn = MongoClient(mongo_uri)
  else:
    conn = MongoClient(host, port)

  return conn[db]
  #return db


def read_mongo(db, collection, query={}, host='mongodb', port=27017, username=None, password=None, no_id=True):
  """ Read from Mongo and Store into DataFrame """

  # Connect to MongoDB
  db = _connect_mongo(host=host, port=port, username=username, password=password, db=db)

  # Make a query to the specific DB and Collection
  cursor = db[collection].find(query)

  # Expand the cursor and construct the DataFrame
  df =  pd.DataFrame(list(cursor))

  # Delete the _id
  if no_id:
      del df['_id']

  return df

def write_mongo(df, db, collection, query={}, host='mongodb', port=27017, username=None, password=None):
  # Connect to MongoDB
  db = _connect_mongo(host=host, port=port, username=username, password=password, db=db)

  # Convert the DataFrame to a JSON formatted string
  json_data = json.loads(df.to_json(orient='records'))

  # Make a query to the specific DB and Collection
  cursor = db[collection]

  # delete all
  cursor.delete_many({})

  # insert DataFrame to mongodb
  cursor.insert_many(json_data)

def print_one_flight_from_mongo(db, collection, query={}, host='mongodb', port=27017, username=None, password=None):

  # Connect to MongoDB
  db = _connect_mongo(host=host, port=port, username=username, password=password, db=db)

  # Make a query to the specific DB and Collection
  cursor = db[collection].find_one(query)

  # Print the retrieved document
  pprint(cursor,  indent=4)

if __name__ == '__main__':
  globals.initialize()
  #print_one_flight_from_mongo(db='air_traffic_system', collection='flights')
  main_connect_mongodb("air_traffic_system", load_flights)
  main_connect_mongodb("air_traffic_system", load_positions_from_airlabs)


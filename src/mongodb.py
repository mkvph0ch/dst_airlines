
import pandas as pd
import requests
import json
from pymongo import MongoClient
from pprint import pprint
from pathlib import Path
import globals

current_path = Path(__file__).parent
data_url = current_path.parent.joinpath('data')

def load_flights(db):
  
  # Load the CSV data into a pandas DataFrame
  # at the moment df_all_flights.csv is not avl in data folder, 
  # please change it to your local path to run this code

  csv_files = ['df_flights_BER_PAR_MUC_20230326_20230402.csv']
  
  collection = db.flights
  # in case you need to delete all flights data
  collection.delete_many({})
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

  # Load the CSV data into a pandas DataFrame
  df = pd.read_csv(data_url.joinpath('airlabs_response.csv'))

  # Convert the DataFrame to a JSON formatted string
  json_data = json.loads(df.to_json(orient='records'))

  collection = db.positions
  collection.insert_many(json_data)

  
def get_positions_from_db(db):

  collection = db.positions
  document = collection.find_one()

  # Print the retrieved document
  pprint(document,  indent=4)

def get_geopositions_from_airlabs(airlabs_token):
  my_params = {'api_key': airlabs_token}

  method = 'flights'
  api_base = 'http://airlabs.co/api/v9/'

  r = requests.get(api_base + method, params = my_params).json()
  resp_list = r.get("response")
  df = pd.json_normalize(resp_list)

  return resp_list, df

def export_airlabs_response(resp_list):
  df = pd.json_normalize(resp_list)
  df.to_csv(data_url.joinpath('airlabs_response.csv'), sep=",", index=False)


def main():

  # Connect to the MongoDB client and insert the data into a collection
  # with clause makes sure client is properly closed after it has been used

  with MongoClient("mongodb://localhost:27017/") as client:

    db = client.air_traffic_system

    load_flights(db)
    # get_flights_from_db(db)

    # load_positions(db)
    # get_positions_from_db(db)


if __name__ == '__main__':
  globals.initialize()
  main()



import pandas as pd
import json
from pymongo import MongoClient
from pprint import pprint

data_url = '../data/'

def load_flights(db):
  
  # Load the CSV data into a pandas DataFrame
  # at the moment df_all_flights.csv is not avl in data folder, 
  # please change it to your local path to run this code

  csv_files = ['df_flights_20232303_06.csv', 'df_flights_20232303_10.csv', 
               'df_flights_20232303_14.csv']
  
  collection = db.flights
  # in case you need to delete all flights data
  collection.delete_many({})
  num_docs = collection.count_documents({})
  if num_docs == 0:
    print('\nAll documents in flights collection have been deleted')

  for file in csv_files:
    df = pd.read_csv(data_url + file, delimiter=';')

    # Convert the DataFrame to a JSON formatted string
    json_data = json.loads(df.to_json(orient='records'))
    collection.insert_many(json_data)

  # count the total number of documents in the collection
  num_docs = collection.count_documents({})

  print("\n", num_docs, " documents have been inserted into flights collection")


def get_flights_from_db(db):

  # Find a document by a query and retrieve it
  # query = {'_id': 1}

  collection = db.flights
  document = collection.find_one()

  # Print the retrieved document
  pprint(document,  indent=4)


def load_positions(db):

  # Load the CSV data into a pandas DataFrame
  df = pd.read_csv('data/airlabs_response.csv')

  # Convert the DataFrame to a JSON formatted string
  json_data = json.loads(df.to_json(orient='records'))

  collection = db.positions
  collection.insert_many(json_data)

  
def get_positions_from_db(db):

  collection = db.positions
  document = collection.find_one()

  # Print the retrieved document
  pprint(document,  indent=4)


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
  main()


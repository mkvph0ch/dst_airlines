mongodb.py
----------

This code is a Python script that interacts with a MongoDB database to load and retrieve data related to flight positions and information. 
Here is a breakdown of the functions and their purpose:

.. code-block:: python

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

The "load_flights(db)" below: loads flight information from a CSV file into a MongoDB collection. 
The function reads the CSV file using Pandas, converts it to a JSON formatted string, and inserts it into the specified collection in the MongoDB database.

.. code-block:: python

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

The line "get_flights_from_db(db)" below: retrieves flight information from the MongoDB collection and prints it to the console. 
The function uses the "find_one()" method to retrieve the first document in the collection.

.. code-block:: python

  def get_flights_from_db(db):

    # Find a document by a query and retrieve it
    # query = {'_id': 1}

    collection = db.flights
    document = collection.find_one()

    # Print the retrieved document
    pprint(document,  indent=4)

The line "load_positions(db)" below: loads flight position data from a CSV file into a MongoDB collection. 
The function reads the CSV file using Pandas, converts it to a JSON formatted string, and inserts it into the specified collection in the MongoDB database.

.. code-block:: python

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

The line "get_positions_from_db(db)" below: retrieves flight position data from the MongoDB collection and prints it to the console. 
The function uses the "find_one()" method to retrieve the first document in the collection.

.. code-block:: python

  def get_positions_from_db(db):

    collection = db.positions
    document = collection.find_one()

    # Print the retrieved document
    pprint(document,  indent=4)

The line "get_geopositions_from_airlabs(export=0)" below: retrieves flight position data from the Airlabs API and returns it as a Pandas DataFrame. 
The function sends a GET request to the API, extracts the response data, and normalizes it using Pandas. 
If the export parameter is set to 1, the function "exports" the DataFrame to a CSV file.

.. code-block:: python

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

The line "load_positions_from_airlabs(db)" below: loads flight position data from the Airlabs API into a MongoDB collection. 
The function calls the "get_geopositions_from_airlabs()" function to retrieve the data, converts it to a JSON formatted string, and inserts it into the specified collection in the MongoDB database.

.. code-block:: python

  def load_positions_from_airlabs(db):

    # Load the response of Airlabs into a pandas DataFrame
    _, df = get_geopositions_from_airlabs()

    # Convert the DataFrame to a JSON formatted string
    json_data = json.loads(df.to_json(orient='records'))

    collection = db.positions
    collection.delete_many({})
    collection.insert_many(json_data)

The line "main_connect_mongodb(collection: str, function, *args, **kwargs)" below: 
Is a wrapper function that connects to a MongoDB database and executes a specified function with optional arguments. 
The function takes in the name of the MongoDB collection, the function to be executed, and any additional arguments and keyword arguments to be passed to the function. 
It uses the "MongoClient" class from the "pymongo" library to connect to the MongoDB database and the "getattr()" function to retrieve the specified database collection.

.. code-block:: python

  def main_connect_mongodb(collection: str, function, *args, **kwargs):

    # INPUT function, *args, **kwargs
    # Connect to the MongoDB client and insert the data into a collection
    # with clause makes sure client is properly closed after it has been used

    with MongoClient("mongodb://localhost:27017/") as client:

      db = getattr(client, collection) # equal to db = client.air_traffic_system
      
      function(db=db, *args, **kwargs)
      # get_flights_from_db(db)
      # load_flights(db)
      # load_positions(db)
      # get_positions_from_db(db)

The line "_connect_mongo(host, port, username, password, db)" below: a utility function that connects to a MongoDB database and returns a connection object. 
The function takes in the hostname, port number, username, password, and database name as parameters, and uses them to create a connection URI to the MongoDB database. 
It then returns a connection object that can be used to interact with the database.

.. code-block:: python

  def _connect_mongo(host, port, username, password, db):
      """ A util for making a connection to mongo """

      if username and password:
          mongo_uri = 'mongodb://%s:%s@%s:%s/%s' % (username, password, host, port, db)
          conn = MongoClient(mongo_uri)
      else:
          conn = MongoClient(host, port)


      return conn[db]

The line "read_mongo(db, collection, query={}, host='localhost', port=27017, username=None, password=None, no_id=True)" below: It is a utility function that reads data from a MongoDB database and returns it as a Pandas DataFrame. 
The function takes in the database name, collection name, query parameters, and optional hostname, port number, username, password, and "no_id" parameter. 
It uses the "_connect_mongo()" function to create a connection to the MongoDB database, and the "find()" method to retrieve data from the specified collection. 
It then converts the retrieved data to a Pandas DataFrame, and deletes the "_id" column if the "no_id" parameter is set to True.

.. code-block:: python

  def read_mongo(db, collection, query={}, host='localhost', port=27017, username=None, password=None, no_id=True):
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

The line "if __name__ == '__main__'" below: Is a  statement that ensures that the following code is executed only if the script is run directly, and not when it is imported as a module. 
The code initializes global variables and calls the "main_connect_mongodb()" function to load flight data into the MongoDB database.

.. code-block:: python

  if __name__ == '__main__':
    globals.initialize()
    main_connect_mongodb("air_traffic_system", load_flights)
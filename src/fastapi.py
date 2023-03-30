
from pymongo import MongoClient
from fastapi import FastAPI, HTTPException
import psycopg2
import globals
from datetime import datetime
import random
from typing import Dict

globals.initialize()

# create api
api = FastAPI(title='My API')

@api.get('/')
def get_index():
    return {'Hello!'}

@api.get('/airport_location/{airport_code:str}')
def get_airport_location(airport_code):
    
    if len(airport_code) != 3:
        raise HTTPException(status_code=400, detail='Airport code must be 3 characters long')
    
    try:
        # create a connection to the PostgreSQL database
        conn = psycopg2.connect(host=globals.hostname,
                            dbname=globals.database,
                            user=globals.username,
                            password=globals.pwd,
                            port=globals.port_id)

        cur = conn.cursor()
        sql_query = f"SELECT CountryName, CityName, AirportName, LocationType FROM v_airports_detailed WHERE AirportCode = upper('{airport_code}');"
        cur.execute(sql_query)
        results = cur.fetchall()

        if len(results) == 0:
           return('Please enter another code, no data found by this parameter')

        results_dict = {'country': results[0][0],
                        'city': results[0][1],
                        'Airport name': results[0][2],
                        'Location type': results[0][3]
                        }
        cur.close()
        conn.close()

        return {"data": results_dict}
    except Exception as e:
        return {"error": str(e)}
    

@api.get('/flights/count/{airport_code:str}/{date:str}')
def get_flights_count(airport_code,date) -> Dict[str, int]:
    # date_obj = datetime.strptime(date, "%Y-%m-%d")

    with MongoClient("mongodb://localhost:27017/") as client:
        db = client.air_traffic_system

        collection = db.flights
        docs = collection.find()

        result = []
        for doc in docs:
            doc['_id'] = str(doc['_id'])
            if (doc['Departure.AirportCode'] == airport_code) & (doc['Departure.Scheduled.Date']== date):
              result.append(doc)

        count = len(result)
        
    client.close()
    return {"flights_count": count}


@api.get("/flights/random")
def get_random_flight():
    with MongoClient("mongodb://localhost:27017/") as client:
        db = client.air_traffic_system
        collection = db.flights
        count = collection.count_documents({}) # Get total number of documents
        random_index = random.randint(0, count - 1) # Get a random index
        random_doc = collection.find().limit(1).skip(random_index)[0] # Get a random document
        random_doc['_id'] = str(random_doc['_id']) # Convert ObjectId to string
    return (random_doc)

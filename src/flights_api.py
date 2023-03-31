
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
    if len(airport_code) != 3:
        raise HTTPException(status_code=400, detail='Airport code must be 3 characters long')
    
    try:
        date_obj = datetime.strptime(date, "%Y-%m-%d")
    except ValueError:
        # The date string is not in the expected format
        raise HTTPException(status_code=400, detail="Incorrect date format, should be YYYY-MM-DD")

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


@api.get("/flights/departure/{departure_airportcode:str}/{actual_departure_date:str}")
def get_flights_info_by_departure_airportcode_and_date(departure_airportcode, actual_departure_date):
    # test BER 2023-03-26

    if len(departure_airportcode) != 3:
        raise HTTPException(status_code=400, detail='Airport code must be 3 characters long')

    try:
        date_obj = datetime.strptime(actual_departure_date, "%Y-%m-%d")
    except ValueError:
        # The date string is not in the expected format
        raise HTTPException(status_code=400, detail="Incorrect date format, should be YYYY-MM-DD")

    with MongoClient("mongodb://localhost:27017/") as client:
        db = client.air_traffic_system
        collection = db.flights
        documents = collection.find()
        result = []
        for document in documents:
                print(document)
                if (document['Departure.AirportCode'] == departure_airportcode) and (document['Departure.Actual.Date'] == actual_departure_date):
                    result.append({'Departure.AirportCode': document['Departure.AirportCode'],
                                   'Departure.Actual.Date': document['Departure.Actual.Date'],
                                   'Departure.Actual.Time': document['Departure.Actual.Time'],
                                   'Arrival.AirportCode': document['Arrival.AirportCode'],
                                   'Arrival.Actual.Date': document['Arrival.Actual.Date'],
                                   'Arrival.Actual.Time': document['Arrival.Actual.Time'],
                                   'FlightNumber': document['OperatingCarrier.AirlineID'] + str(document['OperatingCarrier.FlightNumber'])
                    })

    if len(result) == 0:
        return('Please enter another code, no data found by provided parameters')
    else:
      return result

@api.get("/flights/arrival/{arrival_airportcode:str}/{actual_arrival_date:str}")
def get_flights_info_by_arrival_airportcode_and_date(arrival_airportcode,  actual_arrival_date):
    # test FRA 2023-03-26

    if len(arrival_airportcode) != 3:
        raise HTTPException(status_code=400, detail='Airport code must be 3 characters long')
    try:
        date_obj = datetime.strptime(actual_arrival_date, "%Y-%m-%d")
    except ValueError:
        # The date string is not in the expected format
        raise HTTPException(status_code=400, detail="Incorrect date format, should be YYYY-MM-DD")


    with MongoClient("mongodb://localhost:27017/") as client:
        db = client.air_traffic_system
        collection = db.flights
        documents = collection.find()
        result = []

        for document in documents:
                if (document['Arrival.AirportCode'] == arrival_airportcode) & (document['Arrival.Actual.Date'] == actual_arrival_date):
                    result.append({'Departure.AirportCode': document['Departure.AirportCode'],
                                   'Departure.Actual.Date': document['Departure.Actual.Date'],
                                   'Departure.Actual.Time': document['Departure.Actual.Time'],
                                   'Arrival.AirportCode': document['Arrival.AirportCode'],
                                   'Arrival.Actual.Date': document['Arrival.Actual.Date'],
                                   'FlightNumber': document['OperatingCarrier.AirlineID'] + str(document['OperatingCarrier.FlightNumber'])
                    })
    if len(result) == 0:
        return('Please enter another code, no data found by provided parameters')
    else:
      return result

@api.get("/flights/{flight_number:str}")
def get_flights_info_by_flight_number(flight_number):
    # LH1676 - example for test

    import re
    flight_number_pattern = re.compile(r'^[A-Z]{2}\d{4}$')

    if not flight_number_pattern.match(flight_number.upper()):
        # The flight number does not match the required pattern
        raise HTTPException(status_code=400, detail="Invalid flight number, should be in the format of 2 letters followed by 4 digits")

    with MongoClient("mongodb://localhost:27017/") as client:
        db = client.air_traffic_system
        collection = db.flights
        documents = collection.find()
        result = []

        for document in documents:
            if (document['OperatingCarrier.AirlineID'] + str(document['OperatingCarrier.FlightNumber'])) == flight_number.upper():
                result.append({'Departure.AirportCode': document['Departure.AirportCode'],
                               'Departure.Scheduled.Date': document['Departure.Scheduled.Date'],
                               'Departure.Scheduled.Time': document['Departure.Scheduled.Time'],
                               'Arrival.AirportCode': document['Arrival.AirportCode'],
                               'Arrival.Scheduled.Date': document['Arrival.Scheduled.Date'],
                               'Arrival.Scheduled.Time': document['Arrival.Scheduled.Time']
                })
    if len(result) == 0:
        return('Please enter another code, no data found by provided parameters')
    else:
      return result

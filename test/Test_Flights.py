import re
import json
import random
import psycopg2
import globals

import pandas as pd
from typing import Dict
from pprint import pprint
from datetime import datetime

from pymongo import MongoClient
from fastapi import FastAPI, HTTPException

# create api
api = FastAPI(title='My API')


def insert_flight(db, flight_number: str):
    collection = db.flights
      # Create a document to insert
    dict_flight = { "Departure.AirportCode": "BER", 
              "Departure.Scheduled.Date": "2023-03-26",
              "Departure.Scheduled.Time": "06:20", 
              "Departure.Terminal.Name": 1000, 
              "Departure.Status.Code": "NO",
              
              
              "Departure.Status.Description": "No Status",
              "Arrival.AirportCode": "MUC", 
              "Arrival.Scheduled.Date": "2023-03-26",
              "Arrival.Scheduled.Time": "07:30", 
              
              "Arrival.Terminal.Name": "2",
              "Arrival.Status.Code": "NO",
              "Arrival.Status.Description": "No Status",
              "MarketingCarrierList.MarketingCarrier": "[{'AirlineID': 'A3', 'FlightNumber': '1451'}, {'AirlineID': 'OU', 'Fli…",
              
               "OperatingCarrier.AirlineID": "LH",
               "OperatingCarrier.FlightNumber": flight_number,
               "Equipment.AircraftCode": "32N",
               "Status.Code":"CD",
               "Status.Description":"Flight Cancelled",
                   
               "Departure.Actual.Date": "2023-03-26",
               "Departure.Actual.Time": "09:59",
               "Departure.Terminal.Gate": "B07",
               "Arrival.Actual.Date": "2023-03-26",
               "Arrival.Actual.Time": "11:04",
               "Arrival.Terminal.Gate": "A01"
             }
    new_flight = collection.insert_one(dict_flight)
    if new_flight.acknowledged:
        print({"message": f"Flight {dict_flight['OperatingCarrier.FlightNumber']} created"})
    else:
        print({"message": "error occured while creating flight"})
        
def insert_flight_arrival_airportcode_and_date(db, flight_number, arrival_airportcode, arrival_actual_date):
    collection = db.flights
      # Create a document to insert
    dict_flight = { "Departure.AirportCode": "BER", 
              "Departure.Scheduled.Date": "2023-03-26",
              "Departure.Scheduled.Time": "06:20", 
              "Departure.Terminal.Name": 1000, 
              "Departure.Status.Code": "NO",
              
              
              "Departure.Status.Description": "No Status",
              "Arrival.AirportCode": arrival_airportcode, 
              "Arrival.Scheduled.Date": "2023-03-26",
              "Arrival.Scheduled.Time": "07:30", 
              
              "Arrival.Terminal.Name": "2",
              "Arrival.Status.Code": "NO",
              "Arrival.Status.Description": "No Status",
              "MarketingCarrierList.MarketingCarrier": "[{'AirlineID': 'A3', 'FlightNumber': '1451'}, {'AirlineID': 'OU', 'Fli…",
              
               "OperatingCarrier.AirlineID": "LH",
               "OperatingCarrier.FlightNumber": flight_number,
               "Equipment.AircraftCode": "32N",
               "Status.Code":"CD",
               "Status.Description":"Flight Cancelled", 
                
               "Departure.Actual.Date": "2023-03-26",
               "Departure.Actual.Time": "09:59",
               "Departure.Terminal.Gate": "B07",
               "Arrival.Actual.Date": arrival_actual_date,
               "Arrival.Actual.Time": "11:04",
               "Arrival.Terminal.Gate": "A01"
             }
    new_flight = collection.insert_one(dict_flight)
    if new_flight.acknowledged:
        print({"message": f"Flight {dict_flight['OperatingCarrier.FlightNumber']} created"})
    else:
        print({"message": "error occured while creating flight"})

def insert_flight_departure_airportcode_and_date(db, flight_number, departure_airportcode, departure_actual_date):
    collection = db.flights
      # Create a document to insert
    dict_flight = { "Departure.AirportCode": departure_airportcode, 
              "Departure.Scheduled.Date": "2023-03-26",
              "Departure.Scheduled.Time": "06:20", 
              "Departure.Terminal.Name": 1000, 
              "Departure.Status.Code": "NO",
              
              
              "Departure.Status.Description": "No Status",
              "Arrival.AirportCode": "BER", 
              "Arrival.Scheduled.Date": "2023-03-26",
              "Arrival.Scheduled.Time": "07:30", 
              
              "Arrival.Terminal.Name": "2",
              "Arrival.Status.Code": "NO",
              "Arrival.Status.Description": "No Status",
              "MarketingCarrierList.MarketingCarrier": "[{'AirlineID': 'A3', 'FlightNumber': '1451'}, {'AirlineID': 'OU', 'Fli…",
              
               "OperatingCarrier.AirlineID": "LH",
               "OperatingCarrier.FlightNumber": flight_number,
               "Equipment.AircraftCode": "32N",
               "Status.Code":"CD",
               "Status.Description":"Flight Cancelled", 
                
               "Departure.Actual.Date": departure_actual_date,
               "Departure.Actual.Time": "09:59",
               "Departure.Terminal.Gate": "B07",
               "Arrival.Actual.Date": "2023-03-26",
               "Arrival.Actual.Time": "11:04",
               "Arrival.Terminal.Gate": "A01"
             }
    new_flight = collection.insert_one(dict_flight)
    if new_flight.acknowledged:
        print({"message": f"Flight {dict_flight['OperatingCarrier.FlightNumber']} created"})
    else:
        print({"message": "error occured while creating flight"})
 
def insert_flight_departure_airportcode_and_scheduled_date(db, flight_number, departure_airportcode, departure_scheduled_date):
    collection = db.flights
      # Create a document to insert
    dict_flight = { "Departure.AirportCode": departure_airportcode, 
              "Departure.Scheduled.Date": departure_scheduled_date,
              "Departure.Scheduled.Time": "06:20", 
              "Departure.Terminal.Name": 1000, 
              "Departure.Status.Code": "NO",
              
              
              "Departure.Status.Description": "No Status",
              "Arrival.AirportCode": "BER", 
              "Arrival.Scheduled.Date": "2023-03-26",
              "Arrival.Scheduled.Time": "07:30", 
              
              "Arrival.Terminal.Name": "2",
              "Arrival.Status.Code": "NO",
              "Arrival.Status.Description": "No Status",
              "MarketingCarrierList.MarketingCarrier": "[{'AirlineID': 'A3', 'FlightNumber': '1451'}, {'AirlineID': 'OU', 'Fli…",
              
               "OperatingCarrier.AirlineID": "LH",
               "OperatingCarrier.FlightNumber": flight_number,
               "Equipment.AircraftCode": "32N",
               "Status.Code":"CD",
               "Status.Description":"Flight Cancelled", 
                
               "Departure.Actual.Date": "2023-03-26",
               "Departure.Actual.Time": "09:59",
               "Departure.Terminal.Gate": "B07",
               "Arrival.Actual.Date": "2023-03-26",
               "Arrival.Actual.Time": "11:04",
               "Arrival.Terminal.Gate": "A01"
             }
    new_flight = collection.insert_one(dict_flight)
    if new_flight.acknowledged:
        print({"message": f"Flight {dict_flight['OperatingCarrier.FlightNumber']} created"})
    else:
        print({"message": "error occured while creating flight"})
        

def delete_flight(db, flight_number: str):
    collection = db.flights
    documents = collection.find()
    result = []
    result_count = 0
    for document in documents:
        if document['OperatingCarrier.FlightNumber'] == flight_number:
            collection.delete_many({"_id": document['_id']})
            result_count+=1
    if result_count >= 1:
        print({"message": "Flights deleted"})
    else:
        print({"message": "could not delete"})

    
    
def get_flights(db, flight_number):
    collection = db.flights
    documents = collection.find()
    result = []
    for document in documents:
        if document['OperatingCarrier.FlightNumber'] == flight_number:
            result.append({'OperatingCarrier.FlightNumber': document['OperatingCarrier.FlightNumber']})
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
            if (document['Arrival.AirportCode'] == arrival_airportcode) and (document['Arrival.Actual.Date'] == actual_arrival_date):
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
                #print(document)
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

from fastapi.testclient import TestClient

def test_flights_info_by_flight_number(db):
    client = TestClient(api)
    
    # Delete the documents from the collection
    delete_flight(db, "LH1676")
    
    # Insert the document into the collection
    insert_flight(db, "LH1676")
    
    response = client.get("/flights/LH1676")
    
    assert response.status_code == 200


from fastapi.testclient import TestClient

def test_flights_info_by_arrival_airportcode_and_date(db):
    client = TestClient(api)
    
    # Delete the documents from the collection
    delete_flight(db, "LH1677")
    delete_flight(db, "LH1678")
    delete_flight(db, "LH1679")
    
    # Insert the documents into the collection
    insert_flight_arrival_airportcode_and_date(db, "LH1677", "AAA", "2030-03-26")
    insert_flight_arrival_airportcode_and_date(db, "LH1678", "AAA", "2030-03-26")
    insert_flight_arrival_airportcode_and_date(db, "LH1679", "AAA", "2030-03-26")
    response = client.get("/flights/arrival/AAA/2030-03-26")
    
    assert response.status_code == 200
    assert len(response.json()) == 3


from fastapi.testclient import TestClient

def test_flights_info_by_departure_airportcode_and_date(db):
    client = TestClient(api)
    
    # Delete the documents from the collection
    delete_flight(db, "LH1677")
    delete_flight(db, "LH1678")
    delete_flight(db, "LH1679")
    
    # Insert the documents into the collection
    insert_flight_departure_airportcode_and_date(db, "LH1677", "AAA", "2030-03-26")
    insert_flight_departure_airportcode_and_date(db, "LH1678", "AAA", "2030-03-26")
    insert_flight_departure_airportcode_and_date(db, "LH1679", "AAA", "2030-03-26")
    
    response = client.get("/flights/departure/AAA/2030-03-26")
    
    assert response.status_code == 200
    assert len(response.json()) == 3


def test_flights_count(db):
    client = TestClient(api)
    
    # Delete the documents from the collection
    delete_flight(db, "LH1677")
    delete_flight(db, "LH1678")
    delete_flight(db, "LH1679")
    
    # Insert the documents into the collection
    insert_flight_departure_airportcode_and_scheduled_date(db, "LH1677", "AAA", "2030-03-26")
    insert_flight_departure_airportcode_and_scheduled_date(db, "LH1678", "AAA", "2030-03-26")
    insert_flight_departure_airportcode_and_scheduled_date(db, "LH1679", "AAA", "2030-03-26")
    
    response = client.get("/flights/count/AAA/2030-03-26")

    assert int(response.json()['flights_count']) == 3
    assert response.status_code == 200
 

def main():

  # Connect to the MongoDB client and insert the data into a collection
  # with clause makes sure client is properly closed after it has been used

  with MongoClient("mongodb://localhost:27017/") as client:

    db = client.air_traffic_system
    print("\ntest_flights_info_by_flight_number:\n")
    test_flights_info_by_flight_number(db)
    print("\ntest_flights_info_by_arrival_airportcode_and_date:\n")
    test_flights_info_by_arrival_airportcode_and_date(db)
    print("\ntest_flights_info_by_departure_airportcode_and_date:\n")
    test_flights_info_by_departure_airportcode_and_date(db)
    print("\ntest_flights_count:\n")
    test_flights_count(db)

if __name__ == '__main__':
  main()
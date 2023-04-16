get_lh_data.py 
--------------

This python file is required to make a request to the Lufthansa API
The code below import the neccesary modules:

.. code-block:: python

    import requests
    import pandas as pd
    import globals

DESCRIPTION:The code below
    Converts a nested json response into a pandas DataFrame
INPUT
    lst: list of json objects
OUTPUT
    df: pandas DataFrame

.. code-block:: python

    def list_to_dataframe(lst):

        df = pd.json_normalize(lst)

        return df

DESCRIPTION:The code below
    Fetch all data from LH Public API 
INPUT
    function: An implemented function to fetch a certain data type from the LH Public API.
OUTPUT
    result: return object of the called function

.. code-block:: python

    def get_lh_data(function, *args, **kwargs):
        
        condition = True
        result = []
        init_offset = 0

        while condition:
            try:
                result.extend(function(offset=init_offset, *args, **kwargs))
                init_offset += 100
            except AttributeError:
                condition = False
                break

        return result

DESCRIPTION:The code below
    List all countries or one specific country. It is possible to request the response in a specific language.
INPUT
    countryCode: 2-letter ISO 3166-1 country code
    lang: 2 letter ISO 3166-1 language code (default en)
    limit: Number of records returned per request. Defaults to 20, maximum is 100 (if a value bigger than 100 is given, 100 will be taken)
    offset: Number of records skipped. Defaults to 0
OUTPUT
    list of json objects.

.. code-block:: python

    def request_countries(countryCode="", lang="en", limit=100, offset=0):
        
        country_url = "v1/mds-references/countries/"

        my_params = {
            "countryCode": countryCode, # 2-letter ISO 3166-1 country code
            "lang": lang,
            "limit": limit, # only 100 possible
            "offset": offset
        }

        r = requests.get(lh_api_base_url+country_url, headers=head, params=my_params).json()

        return r.get('CountryResource').get('Countries').get('Country')

DESCRIPTION:The code below
    List all cities or one specific city. It is possible to request the response in a specific language.
INPUT
    cityCode: 3-letter IATA city code
    lang: 2 letter ISO 3166-1 language code (default en)
    limit: Number of records returned per request. Defaults to 20, maximum is 100 (if a value bigger than 100 is given, 100 will be taken)
    offset: Number of records skipped. Defaults to 0
OUTPUT
    list of json objects.

.. code-block:: python

    def request_cities(cityCode="", lang="en", limit=100, offset=0):
        
        city_url = "v1/mds-references/cities/" 

        my_params = {
            "cityCode": cityCode, # 3-letter IATA city code
            "lang": lang,
            "limit": limit, # only 100 possible
            "offset": offset
        }

        r = requests.get(lh_api_base_url+city_url, headers=head, params=my_params).json()

        return r.get('CityResource').get('Cities').get('City')

DESCRIPTION:The code below
    List all airports or one specific airport. All airports response is very large. It is possible to request the response in a specific language.
INPUT
    airportCode: 3-letter IATA airport code
    lang: 2 letter ISO 3166-1 language code (default en)
    limit: Number of records returned per request. Defaults to 20, maximum is 100 (if a value bigger than 100 is given, 100 will be taken)
    offset: Number of records skipped. Defaults to 0
    LHoperated: Restrict the results to locations with flights operated by LH (false=0, true=1)
    group: Restrict the results to locations with flights operated by group
OUTPUT
    list of json objects

.. code-block:: python

    def request_airports(airportCode="", lang="en", limit=100, offset=0, LHoperated=0, group="AllAirports"):
        
        airports_url = "v1/mds-references/airports/" #{airportCode} 3-letter IATA airport code

        my_params = {
            "airportCode": airportCode,
            "lang": lang,
            "limit": limit, # only 100 possible
            "offset": offset,
            "LHoperated": LHoperated,
            "group": group
        }

        r = requests.get(lh_api_base_url+airports_url, headers=head, params=my_params).json()

        return r.get('AirportResource').get('Airports').get('Airport')

DESCRIPTION:The code below
    List the 5 closest airports to the given latitude and longitude, irrespective of the radius of the reference point.
INPUT
    latitude: Latitude in decimal format to at most 3 decimal places
    longitude: Longitude in decimal format to at most 3 decimal places
    lang: 2 letter ISO 3166-1 language code (default en)
OUTPUT
    list of json objects

.. code-block:: python

    def request_nearest_airports(latitude, longitude, lang="en"):
        
        nearest_airports_url = "v1/mds-references/airports/nearest/" 

        my_params = {
            "latitude": latitude, # decimal format to at most 3 decimal places
            "longitude": longitude, # decimal format to at most 3 decimal places
            "lang": lang
        }

        r = requests.get(lh_api_base_url+nearest_airports_url, headers=head, params=my_params).json()

        return r.get('NearestAirportResource').get('Airports').get('Airport')

DESCRIPTION:The code below
    List all airlines or one specific airline.
INPUT
    airlineCode: 2-character IATA airline/carrier code
    limit: Number of records returned per request. Defaults to 20, maximum is 100 (if a value bigger than 100 is given, 100 will be taken)
    offset: Number of records skipped. Defaults to 0
OUTPUT
    list of json objects.

.. code-block:: python

    def request_airlines(airlineCode="", limit=100, offset=0):
        
        airlines_url = "v1/mds-references/airlines/" #{airlineCode} 2-character IATA airline/carrier code

        my_params = {
            "airlineCode": airlineCode,
            "limit": limit, # only 100 possible
            "offset": offset
        }

        r = requests.get(lh_api_base_url+airlines_url, headers=head, params=my_params).json()

        return r.get('AirlineResource').get('Airlines').get('Airline')

DESCRIPTION:The code below
    List all aircraft types or one specific aircraft type.
INPUT
    aircraftCode: 3-character IATA aircraft code
    limit: Number of records returned per request. Defaults to 20, maximum is 100 (if a value bigger than 100 is given, 100 will be taken)
    offset: Number of records skipped. Defaults to 0
OUTPUT
    list of json objects

.. code-block:: python

    def request_aircraft(aircraftCode="", limit=100, offset=0):
        
        aircraft_url = "v1/mds-references/aircraft/" 

        my_params = {
            "aircraftCode": aircraftCode, # 3-character IATA aircraft code
            "limit": limit, # only 100 possible
            "offset": offset
        }

        r = requests.get(lh_api_base_url+aircraft_url, headers=head, params=my_params).json()

        return r.get('AircraftResource').get('AircraftSummaries').get('AircraftSummary')

DESCRIPTION:The code below
    Status of a particular flight (boarding, delayed, etc.)
INPUT
    flightNumber: Flight number including carrier code and any suffix (e.g. 'LH400')
    date: The departure date (YYYY-MM-DD) in the local time of the departure airport
    limit: Number of records returned per request. Defaults to 20, maximum is 100 (if a value bigger than 100 is given, 100 will be taken)
    offset: Number of records skipped. Defaults to 0
OUTPUT
    list of json objects
 
.. code-block:: python

    def request_customer_flight_info(flightNumber, date, limit=100, offset=0):
        
        cust_flight_info_url = f"v1/operations/customerflightinformation/{flightNumber}/{date}"

        my_params = {
            "limit": limit, # only 100 possible
            "offset": offset
        }

        r = requests.get(lh_api_base_url+cust_flight_info_url , headers=head, params=my_params).json()

        return r.get('FlightInformation').get('Flights').get('Flight')

DESCRIPTION:The code below
    Status of flights between a given origin and destination on a given date.
INPUT
    origin: 3-letter IATA airport (e.g. 'FRA')
    destination: 3-letter IATA airport code (e.g. 'JFK')
    date: Departure date (YYYY-MM-DD) in local time of departure airport
    limit: Number of records returned per request. Defaults to 20, maximum is 100 (if a value bigger than 100 is given, 100 will be taken)
    offset: Number of records skipped. Defaults to 0
OUTPUT
    list of json objects

.. code-block:: python

    def request_customer_flight_info_by_route(origin, destination, date, limit=100, offset=0):
       
        cust_flight_info_by_route_url = f"v1/operations/customerflightinformation/route/{origin}/{destination}/{date}"

        my_params = {
            "limit": limit, # only 100 possible
            "offset": offset
        }

        r = requests.get(lh_api_base_url+cust_flight_info_by_route_url, headers=head, params=my_params).json()

        return r.get('FlightInformation').get('Flights').get('Flight')

DESCRIPTION:The code below
    Status of all arrivals at a given airport up to 4 hours from the provided date time.
INPUT
    airportCode: 3-letter IATA aiport code (e.g. 'ZRH')
    fromDateTime: Start of time range in local time of arrival airport (YYYY-MM-DDTHH:mm)
    limit: Number of records returned per request. Defaults to 20, maximum is 100 (if a value bigger than 100 is given, 100 will be taken)
    offset: Number of records skipped. Defaults to 0
OUTPUT
    list of json objects.

.. code-block:: python

    def request_customer_flight_info_at_arrival(airportCode, fromDateTime, limit=100, offset=0):
        
        cust_flight_info_by_arrival_airport_url = f"v1/operations/customerflightinformation/departures/{airportCode}/{fromDateTime}"

        my_params = {
            "limit": limit, # only 100 possible
            "offset": offset
        }

        r = requests.get(lh_api_base_url+cust_flight_info_by_arrival_airport_url, headers=head, params=my_params).json()

        return r.get('FlightInformation').get('Flights').get('Flight')

DESCRIPTION:The code below
    Status of all departures from a given airport up to 4 hours from the provided date time.
INPUT
    airportCode: 3-letter IATA aiport code (e.g. 'ZRH')
    fromDateTime: Start of time range in local time of arrival airport (YYYY-MM-DDTHH:mm)
    limit: Number of records returned per request. Defaults to 20, maximum is 100 (if a value bigger than 100 is given, 100 will be taken)
    offset: Number of records skipped. Defaults to 0
OUTPUT
    list of json objects

.. code-block:: python

    def request_customer_flight_info_at_departure(airportCode, fromDateTime, limit=100, offset=0):
        
        cust_flight_info_by_departure_airport_url = f"v1/operations/customerflightinformation/departures/{airportCode}/{fromDateTime}"

        my_params = {
            "limit": limit, # only 100 possible
            "offset": offset
        }

        r = requests.get(lh_api_base_url+cust_flight_info_by_departure_airport_url, headers=head, params=my_params).json()

        return r.get('FlightInformation').get('Flights').get('Flight')

DESCRIPTION:The code below
    Scheduled flights between given airports on a given date.
INPUT
    origin: Departure airport. 3-letter IATA airport code (e.g. 'ZRH')
    destination: Destination airport. 3-letter IATA airport code (e.g. 'FRA')
    fromDateTime: Local departure date and optionally departure time (YYYY-MM-DD or YYYY-MM-DDTHH:mm). When not provided, time is assumed to be 00:01
    directFlights: Show only direct flights (false=0, true=1). Default is false
    limit: Number of records returned per request. Defaults to 20, maximum is 100 (if a value bigger than 100 is given, 100 will be taken)
    offset: Number of records skipped. Defaults to 0
OUTPUT
    list of json objects

.. code-block:: python

    def request_flight_schedules(origin, destination, fromDateTime, directFlights=0, limit=100, offset=0):
    
        flight_schedules_url = f"v1/operations/schedules/{origin}/{destination}/{fromDateTime}"

        my_params = {
            "directFlights": directFlights,
            "limit": limit, # only 100 possible
            "offset": offset
        }

        r = requests.get(lh_api_base_url+flight_schedules_url, headers=head, params=my_params).json()

        return r.get('FlightInformation').get('Flights').get('Flight')

    if __name__ == "__main__": 
        globals.initialize() 
        head = {'Authorization': 'Bearer {}'.format(globals.my_token)} # header is described here https://developer.lufthansa.com/docs/read/api_basics/HTTP_request_headers
        lh_api_base_url = "https://api.lufthansa.com/" # base url of Lufthansa Public API
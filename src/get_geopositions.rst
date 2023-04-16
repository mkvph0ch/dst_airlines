
get_geopositions.py
-------------------

This Python script performs the following functions:

Imports the necessary libraries: requests for making HTTP requests and pandas for data manipulation.
Initializes global variables by calling the initialize() function from the globals module.
Defines a dictionary called my_params with a single key-value pair: api_key and the value of the airlabs_token global variable.
Sets the method variable to the string 'flights'.
Sets the api_base variable to the base URL of the AirLabs API.
Sends an HTTP GET request to the AirLabs API endpoint with the URL constructed by concatenating api_base and method, along with the my_params dictionary. The response is returned as a JSON object and stored in the r variable.
Extracts the response key from the JSON object and stores the corresponding value (a list of dictionaries) in the resp_list variable.
Converts the list of dictionaries into a Pandas DataFrame called df using the pd.json_normalize() function.
Writes the contents of the df DataFrame to a CSV file named airlabs_response.csv with comma-separated values and no index.
Prints the first five rows of the df DataFrame using the head() function.
Code

.. code-block:: python

    python
    Copy code
    import requests
    import pandas as pd
    import globals

    globals.initialize()

    my_params = {'api_key': globals.airlabs_token}

    method = 'flights'
    api_base = 'http://airlabs.co/api/v9/'

    r = requests.get(api_base + method, params=my_params).json()

    resp_list = r.get("response")

    df = pd.json_normalize(resp_list)
    df.to_csv('airlabs_response.csv', sep=",", index=False)
    print(df.head())


Explanation

The code imports the necessary libraries, initializes global variables, defines a dictionary with a single key-value pair, sets the method and api_base variables, sends an HTTP GET request to the AirLabs API endpoint, extracts the response key and stores the corresponding value, converts the list of dictionaries into a Pandas DataFrame, writes the contents of the DataFrame to a CSV file, and prints the first five rows of the DataFrame using the head() function.
The code can be run by executing the script in a Python environment or from the command line.
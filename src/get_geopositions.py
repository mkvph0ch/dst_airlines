import requests
import pandas as pd
import globals


globals.initialize()


my_params = {'api_key': globals.airlabs_token}

method = 'flights'
api_base = 'http://airlabs.co/api/v9/'

r = requests.get(api_base + method, params = my_params).json()

resp_list = r.get("response")

df = pd.json_normalize(resp_list)
df.to_csv('airlabs_response.csv', sep=",", index=False)
print(df.head())


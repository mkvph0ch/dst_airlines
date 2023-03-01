import requests
import time
import csv


current_time = int(time.time())

root_url = "https://opensky-network.org/api"
all_states_url = "/states/all"

# list_of_codes = ['3c675a', '3c6444', '3e1bf9', '3c4b26']
# https://opensky-network.org/api/states/all?time=1458564121&icao24=3c6444


with open('output.csv', 'w', newline='') as file:
    writer = csv.writer(file)
    # Write the header row
    writer.writerow(['icao24', 'callsign', 'origin_country', 'time_position','last_contact',
                    'longitude','latitude','baro_altitude','on_ground','velocity','true_track'
                    ,'vertical_rate','sensors','geo_altitude','squawk','spi','position_source',
                    'category'])

    r1 = requests.get(root_url+all_states_url, params = {"time":current_time})

    r1 = r1.json()
    states = r1['states']
    if states is not None:

      # Write the data rows
      for row in states:
          writer.writerow(row)


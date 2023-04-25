# dst_airlines
final project for data engineering bootcamp jan2023 datascientest

# Instruction
In order to run the code properly, please provide a globals.py inside "./src" folder in this form

```py
import os

def initialize(): 
    global my_token
    global hostname
    global database
    global username
    global pwd
    global port_id
    global airlabs_token
    global mapbox_token
    global mongohost
    global mongoport

    # LH Token
    my_token = 'your_personal_LH_token' 
    
    # PostreSQL
    database = 'dst_airlines'
    username = 'postgres'
    pwd = 'postgres'

    # Airlabs
    airlabs_token = 'your_personal_airlabs_token'

    # MongoDB
    mongoport = '27017'

    if os.environ.get('platform') == "docker":
        mongohost = 'mongodb' # hostname MongoDB
        hostname = 'postgres' # hostname pSQL
        port_id = '5432' # port pSQL
    else:
        mongohost = 'localhost' # hostname MongoDB
        hostname = 'localhost' # hostname pSQL
        port_id = '8001' # port pSQL
```


# Documentation for DST_Airlines Dashboard and FastAPI. 


## 1. Introduction: 


Welcome to the DST_Airlines Dashboard and FastAPI documentation. This guide is designed to help you get started with our dashboard quickly and easily. Our dashboard is a powerful tool that allows you to track aircraft in real-time and access information about flights all over the world. The dashboard is designed to work well on different operating systems. Our FastAPI allows you to get more information on flights. 


## 2. Source Code: 


All of our source code can be found on Github at 


https://github.com/mkvph0ch/dst_airlines. You can access our code and contribute to it if you like. 


## 3. Setup: 


### Step 1: Cloning Github Repo 


To get started with our dashboard, you need to clone our Github repository to your local machine. Open your terminal and run the command: 


```
<p style="text-align: right">
git clone https://github.com/mkvph0ch/dst_airlines.git
</p>
```



This will download our code to your local machine. 


### Step 2: Using Docker Compose 


Our dashboard uses Docker Compose to manage its containers. Open your terminal and navigate to the dst_airlines directory. Then run the following command: 


```
    sudo docker-compose up --build -d 
```



This will start the containers. It may take some time to complete. 


### Step 3: Checking Containers 


Run the following command to check if all 6 containers are up and running:


```
    docker ps 
```



You should see containers: my_mongo, my_postgres, my_dash, my_fastapi, mongo-express, pgadmin.


### Step 4: Loading Initial Data 

Now that the containers are running, you need to load the initial data into the databases. For that, you need to run two Python scripts: _pandas_to_sql.py _and _mongodb.py_. Change the hostname for databases in globals.py if needed.


Run the following commands to load initial data into the databases: 


```
    python pandas_to_sql.py 
    python mongodb.py 
```



These scripts will load static data like cities, countries, airports, etc. into the Postgres database and flights and positions data into the MongoDB database. All data will be stored in volumes locally. You need to do it only once.


### Step 5: Accessing container locally from a web-browser:


Dashboard:      localhost:8050 

FastAPI:        localhost:8000/docs

mongo-express:  localhost:8081

pgAdmin:        localhost:8085
                User: postgres@postgres.com
                PW: postgres

PostgreSQL:     localhost:8001
                User: postgres
                PW: postgres
                db: dst_airlines

## 4. Usage: 


### Dashboard. 


Our dashboard allows you to track flights in real-time and access information about flights all over the world. By hovering over each point on the map, you can see the flight number and current geopositions. 

For more interesting info on each flight, you can copy flight number from the dashboard and use it in our fastapi.


### FastAPI. 


All endpoints are described in docs/flights_api.rst. 


```
    / 
    /airport_location/{airport_code:str} 
    /flights/count/{airport_code:str}
    /flights/random 
    /flights/departure/{departure_airportcode:str}/{ac tual_departure_date:str} 
    /flights/arrival/{arrival_airportcode:str}/{actual _arrival_date:str} 
```



## 5. Conclusion: 


We hope this guide has helped you get started with our DST_Airlines Dashboard and FastAPI. If you have any questions or feedback, please contact us by email <span style="text-decoration:underline;">support@dst_flights_official.de</span>


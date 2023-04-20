# dst_airlines
final project for data engineering bootcamp jan2023 datascientest

# Instruction
In order to run the code properly, please provide a globals.py inside "./src" folder in this form

```py
def initialize(): 
    global my_token
    global hostname
    global database
    global username
    global pwd
    global port_id
    global airlabs_token

    my_token = 'your_personal_LH_token'
    hostname = 'your_hostname'
    database = 'your_database_name' # e.g. dst_airlines
    username = 'your_psql_username'
    pwd = 'your_psql_password'
    port_id = 'your_psql_code'
    airlabs_token = 'your_airlabs_token'
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


After the containers are running, you need to check if all 4 containers are up and running. Run the following command: 


```
    docker ps 
```



This will list all the running containers. You should see 4 containers running. 


### Step 4: Loading Initial Data 

Now that the containers are running, you need to load the initial data into the databases. For that, you need to run two Python scripts: _pandas_to_sql.py _and _mongodb.py_. Change the hostname for databases in globals.py if needed.


Run the following commands to load initial data into the databases: 


```
    python pandas_to_sql.py 
    python mongodb.py 
```



These scripts will load static data like cities, countries, airports, etc. into the Postgres database and flights and positions data into the MongoDB database. 


### Step 5: Running the Dashboard 


After the data is loaded, you need to find the IP address used by the dashboard. Run the following command: 


```
    docker inspect my_dashboard | grep IPAddress 
```



This will give you the IP address used by the dashboard. Open your web browser and go to _dash_container_IP:8050 _to access our dashboard. 


### Step 6: Running the FastAPI 


`docker inspect my_fastapi | grep IPAddress `

Open your web browser and go to DASH_IP:8000 to access our FastAPI.


## 4. Usage: 


### Dashboard. 


Our dashboard allows you to track flights in real-time and access information about flights all over the world. By clicking on each point on the map, you can see the flight number and current geopositions. 


### FastAPI. 


All endpoints are described in docs/flights_api.rst. 


```
    / 
    /airport_location/{airport_code:str} 
    /flights/count/{airport_code:str}/{date:str} /flights/random 
    /flights/departure/{departure_airportcode:str}/{ac tual_departure_date:str} 
    /flights/arrival/{arrival_airportcode:str}/{actual _arrival_date:str} 
```



## 5. Conclusion: 


We hope this guide has helped you get started with our DST_Airlines Dashboard and FastAPI. If you have any questions or feedback, please contact us by email <span style="text-decoration:underline;">support@dst_flights_official.de</span>


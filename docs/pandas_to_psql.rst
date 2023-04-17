pandas_to_psql.py
-----------------

This python code is responsible for creating and populating tables for the PostgreSQL database, based on clean data from CSV files. 
Below is the documentation for each function in the code:

.. code-block:: python

    import psycopg2
    import pandas as pd
    import numpy as np
    from sqlalchemy import create_engine
    import sqlalchemy.types
    from pathlib import Path
    import globals

The line "delete_tables(cur, conn)" function below takes two arguments, the "cur" parameter is the cursor object, and the "conn" parameter is the connection object, which is used to interact with the PostgreSQL database. 
This function deletes the existing tables from the database: 
"mv_airports_detailed", "airports", "cities", "countries", "airlines", and "aircrafts". It is used to clear any existing data before creating new tables.

.. code-block:: python

    def delete_tables(cur, conn):
        cur.execute("""
            DROP VIEW IF EXISTS mv_airports_detailed;
            DROP TABLE IF EXISTS airports;
            DROP TABLE IF EXISTS cities;
            DROP TABLE IF EXISTS countries;
            DROP TABLE IF EXISTS airlines;
            DROP TABLE IF EXISTS aircrafts;
        """)

        conn.commit()

The line "create_airlines_table_(cursor)" function below takes a cursor object as a parameter. 
It is used to create a new table "airlines" in the database. 
The table contains columns like "AirlineID", "AirlineID_ICAO", "AirlineName", with "AirlineID" as a primary key.

.. code-block:: python

    def create_airlines_table_(cursor) -> None:
        cursor.execute("""
            DROP TABLE IF EXISTS airlines;
            CREATE TABLE airlines (
                AirlineID char(3) NOT NULL,
                AirlineID_ICAO char(3),
                AirlineName text,
                PRIMARY KEY (AirlineID)
            ); 
            """)

The line "create_aircrafts_table_(cursor)" function below takes a cursor object as a parameter. 
It is used to create a new table aircrafts in the database. 
The table contains columns like "AircraftCode", "AirlineEquipCode", "AircraftName", with "AircraftCode" as a primary key.

.. code-block:: python

    def create_aircrafts_table_(cursor) -> None:
        cursor.execute("""
            DROP TABLE IF EXISTS aircrafts;
            CREATE TABLE aircrafts (
                AircraftCode char(3) NOT NULL,
                AirlineEquipCode char(4),
                AircraftName text,
                PRIMARY KEY (AircraftCode)
            ); 
            """)

The line "create_countries_table_(cursor)" function below takes a cursor object as a parameter. 
It is used to create a new table countries in the database. 
The table contains columns like "CountryCode", "CountryName", with "CountryCode" as a primary key.

.. code-block:: python

    def create_countries_table_(cursor) -> None:
        cursor.execute("""
            DROP TABLE IF EXISTS countries;
            CREATE TABLE countries (
                CountryCode char(2) NOT NULL,
                CountryName text,
                PRIMARY KEY (CountryCode)
            );
            """)

The line "create_cities_table_(cursor)" function below takes a cursor object as a parameter. 
It is used to create a new table cities in the database. 
The table contains columns like "CityCode", "CountryCode", "UtcOffset", "TimeZoneId", "CityName", with "CityCode" as a primary key. 
The function also adds a foreign key reference to the countries table.

.. code-block:: python

    def create_cities_table_(cursor) -> None:
        cursor.execute("""
            DROP TABLE IF EXISTS cities;
            CREATE TABLE cities (
                CityCode char(3) NOT NULL,
                CountryCode char(2) NOT NULL,
                UtcOffset interval,
                TimeZoneId text,
                CityName text,
                PRIMARY KEY (CityCode),
                FOREIGN KEY (CountryCode) REFERENCES countries (CountryCode)
            ); 
            """)

The line "create_airports_table_(cursor)" function below takes a cursor object as a parameter. 
It is used to create a new table airports in the database. 
The table contains columns like "AirportCode", "CityCode", "CountryCode", "LocationType", "UtcOffset", "TimeZoneId", "Latitude", "Longitude", "AirportName", with "AirportCode" as a primary key. 
The function also adds foreign key references to both the "countries" and "cities" tables.

.. code-block:: python

    def create_airports_table_(cursor) -> None:
        cursor.execute("""
            DROP TABLE IF EXISTS airports;
            CREATE TABLE airports (
                AirportCode char(3) NOT NULL,
                CityCode char(3) NOT NULL,
                CountryCode char(2) NOT NULL,
                LocationType text,
                UtcOffset interval,
                TimeZoneId text,
                Latitude double precision,
                Longitude double precision,
                AirportName text,
                PRIMARY KEY (AirportCode),
                FOREIGN KEY (CountryCode) REFERENCES countries (CountryCode),
                FOREIGN KEY (CityCode) REFERENCES cities (CityCode)
            ); 
            """)

The line "create_airports_detailed_view(cur)" function below takes a cursor object as a parameter. 
It is used to create a materialized view "mv_airports_detailed" in the database. 
The view includes all columns from the "airports" table along with "CityName" and "CountryName". 
It is used to provide more detailed information about the airports.

.. code-block:: python

    def create_airports_detailed_view(cur) -> None:
        cur.execute("""
            DROP MATERIALIZED VIEW IF EXISTS mv_airports_detailed;
            CREATE OR REPLACE MATERIALIZED VIEW mv_airports_detailed as 
                SELECT a.*,
                    c.CityName, 
                    con.CountryName 
                FROM airports a 
                        JOIN cities c ON a.CityCode = c.CityCode 
                        JOIN countries con ON con.CountryCode = c.CountryCode;
                """  
                )

The line "insert_values(df, table, cur, conn)" function below takes four parameters, the "df" parameter is a pandas dataframe, "table" parameter is the name of the table in the database, "cur" parameter is the cursor object, and the "conn" parameter is the connection object. 
It is used to insert data from the pandas dataframe to the specified table in the database.

.. code-block:: python

    def insert_values(df, table, cur, conn):
        if len(df) > 0:
            df_columns = list(df)
            # create (col1,col2,...)
            columns = ",".join(df_columns)

            # create VALUES('%s', '%s",...) one '%s' per column
            values = "VALUES({})".format(",".join(["%s" for _ in df_columns])) 

            #create INSERT INTO table (columns) VALUES('%s',...)
            insert_stmt = "INSERT INTO {} ({}) {}".format(table,columns,values)
            cur.execute("truncate " + table + ";")  #avoiding uploading duplicate data!
            cur = conn.cursor()
            psycopg2.extras.execute_batch(cur, insert_stmt, df.values)
        conn.commit()

In the main section of the code below, the globals module is initialized, which contains global variables used to connect to the PostgreSQL database. 
The path to the data folder is also loaded. 
The code then creates a connection to the PostgreSQL database using the psycopg2 module and creates an engine for the connection using the create_engine function from the sqlalchemy module. 
The code then loads clean dataframes from the CSV files and calls the delete_tables function to clear any existing tables. 
Finally, the code calls the other functions to create and populate new tables in the database.

.. code-block:: python

    if __name__ == "__main__": 
        # load global variables
        globals.initialize()
        # load paths
        current_path = Path(__file__).parent
        data_path = current_path.parent.joinpath('data')

        # create a connection to the PostgreSQL database
        conn = psycopg2.connect(host=globals.hostname,
                                dbname=globals.database,
                                user=globals.username,
                                password=globals.pwd,
                                port=globals.port_id)

        # create an engine for the connection
        engine = create_engine(f'postgresql://{globals.username}:{globals.pwd}@{globals.hostname}:{globals.port_id}/{globals.database}')

        #Create a cursor
        cur = conn.cursor()

        # load clean dataframes
        df_countries = pd.read_csv(data_path.joinpath('df_countries_clean.csv'), sep=";", header=0, na_values=["",np.nan], keep_default_na=False)

        df_cities = pd.read_csv(data_path.joinpath('df_cities_clean.csv'), sep=";", header=0, na_values=["",np.nan], keep_default_na=False)

        df_airlines = pd.read_csv(data_path.joinpath('df_airlines_clean.csv'), sep=";", header=0, na_values=["",np.nan], keep_default_na=False)

        df_airports = pd.read_csv(data_path.joinpath('df_airports_clean.csv'), sep=";", header=0, na_values=["",np.nan], keep_default_na=False)

        df_aircrafts = pd.read_csv(data_path.joinpath('df_aircrafts_clean.csv'), sep=";", header=0, na_values=["",np.nan], keep_default_na=False)

        # delete existing tables
        delete_tables(cur, conn)

        # create airlines table and insert data from df
        with conn.cursor() as cursor:
            create_airlines_table_(cursor)

        insert_values(df_airlines,'airlines',cur,conn)

        # create aircrafts table and insert data from df
        with conn.cursor() as cursor:
            create_aircrafts_table_(cursor)

        insert_values(df_aircrafts,'aircrafts',cur,conn)

        # create countries table and insert data from df
        with conn.cursor() as cursor:
            create_countries_table_(cursor)

        insert_values(df_countries,'countries',cur,conn)

        # create cities table and insert data from df
        with conn.cursor() as cursor:
            create_cities_table_(cursor)

        insert_values(df_cities,'cities',cur,conn)

        # create airports table and insert data from df
        with conn.cursor() as cursor:
            create_airports_table_(cursor)

        insert_values(df_airports,'airports',cur,conn)

        # create airports detailed view

        create_airports_detailed_view(cur)
        conn.commit()
        
        #Close the cursor and the connection
        cur.close()
        conn.close()
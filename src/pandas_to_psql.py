import psycopg2
import pandas as pd
import numpy as np
from sqlalchemy import create_engine
import sqlalchemy.types
from pathlib import Path
import globals

def delete_tables(cur, conn):
    cur.execute("""
        DROP TABLE IF EXISTS airports;
        DROP TABLE IF EXISTS cities;
        DROP TABLE IF EXISTS countries;
        DROP TABLE IF EXISTS airlines;
        DROP TABLE IF EXISTS aircrafts;
    """)

    conn.commit()

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

def create_countries_table_(cursor) -> None:
    cursor.execute("""
        DROP TABLE IF EXISTS countries;
        CREATE TABLE countries (
            CountryCode char(2) NOT NULL,
            CountryName text,
            PRIMARY KEY (CountryCode)
        );
        """)

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

def create_airports_detailed_view(cur) -> None:
    cur.execute("""
        DROP TABLE IF EXISTS v_airports_detailed;
        CREATE OR REPLACE VIEW v_airports_detailed as 
            SELECT a.*,
                   c.CityName, 
                   con.CountryName 
            FROM airports a 
                    JOIN cities c ON a.CityCode = c.CityCode 
                    JOIN countries con ON con.CountryCode = c.CountryCode;
            """  
            )

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
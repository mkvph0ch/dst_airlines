create_tables.sql
----------------

This file contains SQL code to create multiple tables:

Countries Table:
----------------

The code below CREATE TABLE statement creates a table called "countries" with columns "CountryCode" and "CountryName". 
The "CountryCode" column is defined as a char(2) data type and is marked as NOT NULL, meaning it cannot be empty. 
The PRIMARY KEY constraint is applied to the "CountryCode" column, which means that each record in the table must have a unique value in that column.

.. code-block:: sql
    
    CREATE TABLE countries (
        CountryCode char(2) NOT NULL,
        CountryName text,
        PRIMARY KEY (CountryCode)
    );

Cities Table:
-------------

The code below CREATE TABLE statement creates a table called "cities" with columns "CityCode", "CountryCode", "UtcOffset", "TimeZoneId", and "CityName". 
The "CityCode" column is defined as a char(3) data type and is marked as NOT NULL. The "CountryCode" column is also defined as a char(2) data type and is marked as NOT NULL. 
The "UtcOffset" column is defined as an interval data type, which represents a duration of time. The "TimeZoneId" and "CityName" columns are defined as text data type. 
The PRIMARY KEY constraint is applied to the "CityCode" column, and two FOREIGN KEY constraints are applied to the "CountryCode" column. The FOREIGN KEY constraints ensure that each record in the "cities" table has a valid reference to a record in the "countries" table.

.. code-block:: sql

    CREATE TABLE cities (
        CityCode char(3) NOT NULL,
        CountryCode char(2) NOT NULL,
        UtcOffset interval,
        TimeZoneId text,
        CityName text,
        PRIMARY KEY (CityCode),
        FOREIGN KEY (CountryCode) REFERENCES countries (CountryCode)
    );

Airports Table:
---------------

The code below CREATE TABLE statement creates a table called "airports" with columns "AirportCode", "CityCode", "CountryCode", "LocationType", "UtcOffset", "TimeZoneId", "Latitude", "Longitude", and "AirportName". 
The "AirportCode" column is defined as a char(3) data type and is marked as NOT NULL. The "CityCode" and "CountryCode" columns are defined as char(3) and char(2) data types, respectively, and are marked as NOT NULL. 
The "LocationType" column is defined as text data type. 
The "UtcOffset" column is defined as an interval data type. 
The "TimeZoneId", "Latitude", "Longitude", and "AirportName" columns are defined as text, double precision, double precision, and text data types, respectively. 
The PRIMARY KEY constraint is applied to the "AirportCode" column, and two FOREIGN KEY constraints are applied to the "CountryCode" and "CityCode" columns. 
The FOREIGN KEY constraints ensure that each record in the "airports" table has valid references to records in the "countries" and "cities" tables.

.. code-block:: sql

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

Airlines Table
--------------

The code below CREATE TABLE statement creates a table called "airlines" with columns "AirlineID", "AirlineID_ICAO", and "AirlineName". 
The "AirlineID" column is defined as a char(3) data type and is marked as NOT NULL. The "AirlineID_ICAO" and "AirlineName" columns are defined as text data types. 
The PRIMARY KEY constraint is applied to the "AirlineID" column.

.. code-block:: sql

    CREATE TABLE airlines (
        AirlineID char(3) NOT NULL,
        AirlineID_ICAO char(3),
        AirlineName text,
        PRIMARY KEY (AirlineID)
    );

Aircrafts Table:
---------------

The code below CREATE TABLE statement creates a table called "aircrafts" with columns "AircraftCode", "AirlineEquipCode", and "AircraftName". 
The "AircraftCode" column is defined as a char(3) data type and is marked as NOT NULL. 
The "AirlineEquipCode" and "AircraftName" columns are defined as text data types. 
The PRIMARY KEY constraint is applied to the "AircraftCode" column.

.. code-block:: sql

    CREATE TABLE aircrafts (
        AircraftCode char(3) NOT NULL,
        AirlineEquipCode char(4),
        AircraftName text,
        PRIMARY KEY (AircraftCode)
    );

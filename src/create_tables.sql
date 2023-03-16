CREATE TABLE countries (
    CountryCode char(2) NOT NULL,
    CountryName text NOT NULL,
    PRIMARY KEY (CountryCode)
); 
CREATE TABLE cities (
    CityCode char(3) NOT NULL,
    CountryCode char(2) NOT NULL,
    UtcOffset interval NOT NULL,
    TimeZoneId text NOT NULL,
    CityName text NOT NULL,
    PRIMARY KEY (CityCode),
    FOREIGN KEY (CountryCode) REFERENCES countries (CountryCode)
); 
CREATE TABLE airports (
    AirportCode char(3) NOT NULL,
    CityCode char(3) NOT NULL,
    CountryCode char(2) NOT NULL,
    LocationType text,
    UtcOffset interval NOT NULL,
    TimeZoneId text NOT NULL,
    Latitude double precision NOT NULL,
    Longitude double precision NOT NULL,
    AirportName text NOT NULL,
    PRIMARY KEY (AirportCode),
    FOREIGN KEY (CityCode) REFERENCES cities (CounCityCodetryCode),
    FOREIGN KEY (CountryCode) REFERENCES countries (CountryCode)
); 
CREATE TABLE airlines (
    AirlineID char(2) NOT NULL,
    AirlineID_ICAO char(3),
    AirlineName text NOT NULL,
    PRIMARY KEY (AirlineID)
); 
CREATE TABLE aircrafts (
    AircraftCode char(3) NOT NULL,
    AirlineEquipCode char(4) NOT NULL,
    AircraftName text NOT NULL,
    PRIMARY KEY (AircraftCode)
); 

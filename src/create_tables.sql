CREATE TABLE countries (
    CountryCode char(2) NOT NULL,
    CountryName text,
    PRIMARY KEY (CountryCode)
); 
CREATE TABLE cities (
    CityCode char(3) NOT NULL,
    CountryCode char(2),
    UtcOffset interval,
    TimeZoneId text,
    CityName text,
    PRIMARY KEY (CityCode),
    FOREIGN KEY (CountryCode) REFERENCES countries (CountryCode)
); 
CREATE TABLE airports (
    AirportCode char(3) NOT NULL,
    CityCode char(3),
    CountryCode char(2),
    LocationType text,
    UtcOffset interval,
    TimeZoneId text,
    Latitude double precision,
    Longitude double precision,
    AirportName text,
    PRIMARY KEY (AirportCode),
    FOREIGN KEY (CityCode) REFERENCES cities (CounCityCodetryCode),
    FOREIGN KEY (CountryCode) REFERENCES countries (CountryCode)
); 
CREATE TABLE airlines (
    AirlineID char(2) NOT NULL,
    AirlineID_ICAO char(3),
    AirlineName text,
    PRIMARY KEY (AirlineID)
); 
CREATE TABLE aircrafts (
    AircraftCode char(3) NOT NULL,
    AirlineEquipCode char(4),
    AircraftName text,
    PRIMARY KEY (AircraftCode)
); 

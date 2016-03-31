BEGIN TRANSACTION;
CREATE TABLE Measurements(Mid integer primary key autoincrement, Timestamp datetime, Temperature real, Humidity real, AirPressure real, CO2level integer);
COMMIT;

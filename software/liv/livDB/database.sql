BEGIN TRANSACTION;
CREATE TABLE Measurements(Mid integer primary key autoincrement, Timestamp datetime, Temperature real, Humidity real, AirPressure real, CO2level integer);
INSERT INTO Measurements VALUES(1,'2014-01-31 10:11:12', 12.3, 45.6, 1234, 600);
COMMIT;
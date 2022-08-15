DDL = '''
    CREATE TABLE Dates (
    idDates INT NOT NULL PRIMARY KEY IDENTITY,
    year INT NULL,
    month INT NULL,
    day INT NULL
    );

    CREATE TABLE Countries (
    idCountries INT NOT NULL PRIMARY KEY IDENTITY,
    countryName VARCHAR(100) NULL,
    );

    CREATE TABLE Locations (
    idLocations INT NOT NULL PRIMARY KEY IDENTITY,
    locationName VARCHAR(150) NOT NULL,
    idCountry INT NULL,
    CONSTRAINT country_location
        FOREIGN KEY (idCountry)
        REFERENCES Countries (idCountries)
    );

    CREATE TABLE GeneralDamage (
    idGeneralDamage INT NOT NULL PRIMARY KEY IDENTITY,
    totalDamage INT NULL,
    totalDamageDesc INT NULL,
    );

    CREATE TABLE PeopleDamage (
    idPeopleDamage INT NOT NULL PRIMARY KEY IDENTITY,
    totalMissing INT NULL,
    totalDeaths INT NULL,
    );

    CREATE TABLE DamagedHouses (
    idDamagedHouses INT NOT NULL PRIMARY KEY IDENTITY,
    totalHousesDamaged INT NULL,
    );

    CREATE TABLE DestroyedHouses (
    idDestroyedHouses INT NOT NULL PRIMARY KEY IDENTITY,
    totalHousesDestroyed INT NULL,
    );

    CREATE TABLE Tsunamis (
        idTsunamis INT NOT NULL PRIMARY KEY IDENTITY,
        maxWaterHeight FLOAT NULL,
        idDates INT NULL,
        idLocations INT NULL,
        idDamagedHouses INT NULL,
        idDestroyedHouses INT NULL,
        idGeneralDamage INT NULL,
        idPeopleDamage INT NULL,
        CONSTRAINT tsunamiDate
            FOREIGN KEY (idDates)
            REFERENCES Dates (idDates),
        CONSTRAINT tsunamiLocation
            FOREIGN KEY (idLocations)
            REFERENCES Locations (idLocations),
        CONSTRAINT tsunamiGD
            FOREIGN KEY (idGeneralDamage)
            REFERENCES GeneralDamage (idGeneralDamage),
        CONSTRAINT tsunamiPD
            FOREIGN KEY (idPeopleDamage)
            REFERENCES PeopleDamage (idPeopleDamage),
        CONSTRAINT tsunamiDamagedH
            FOREIGN KEY (idDamagedHouses)
            REFERENCES DamagedHouses (idDamagedHouses),
        CONSTRAINT tsunamiHD
            FOREIGN KEY (idDestroyedHouses)
            REFERENCES DestroyedHouses (idDestroyedHouses)
    );

    INSERT INTO Countries(countryName)
        SELECT DISTINCT country FROM Temp

    INSERT INTO Dates(year, month, day)
        SELECT DISTINCT year, month, day FROM Temp;

    INSERT INTO PeopleDamage(totalDeaths)
        SELECT DISTINCT total_deaths FROM Temp;

    INSERT INTO GeneralDamage(totalDamage, totalDamageDesc)
        SELECT DISTINCT total_damage_mil, total_damage_desc FROM Temp;

    INSERT INTO DestroyedHouses(totalHousesDestroyed)
        SELECT DISTINCT total_houses_destroyed FROM Temp;


    INSERT INTO DamagedHouses(totalHousesDamaged)
    SELECT DISTINCT total_houses_damaged FROM Temp;

    INSERT INTO Locations(locationName, idCountry)
        SELECT DISTINCT t.location_name, c.idCountries
        FROM Temp t
        INNER JOIN Countries c
        ON t.country = c.countryName;


    INSERT INTO Tsunamis(maxWaterHeight, idDates, idLocations, idDamagedHouses, idDestroyedHouses, idGeneralDamage, idPeopleDamage)
        SELECT DISTINCT t.max_water_height, d.idDates, l.idLocations, damh.idDamagedHouses, desh.idDestroyedHouses, gd.idGeneralDamage,
        pd.idPeopleDamage
        FROM Temp t
        LEFT JOIN Dates d
        ON t.year = d.year
        LEFT JOIN Locations l
        ON t.location_name = l.locationName
        LEFT JOIN DamagedHouses damh
        ON t.total_houses_damaged = damh.totalHousesDamaged
        LEFT JOIN DestroyedHouses desh
        ON t.total_houses_destroyed = desh.totalHousesDestroyed
        LEFT JOIN GeneralDamage gd
        ON t.total_damage_mil = gd.totalDamage
        LEFT JOIN PeopleDamage pd
        ON t.total_deaths = pd.totalDeaths
        WHERE d.month = t.month AND d.year = t.year AND d.day = t.day AND l.locationName = t.location_name;


'''

table_drop = '''
    DROP TABLE IF EXISTS Tsunamis;
    DROP TABLE IF EXISTS Locations;
    DROP TABLE IF EXISTS Countries;
    DROP TABLE IF EXISTS Dates;
    DROP TABLE IF EXISTS GeneralDamage;
    DROP TABLE IF EXISTS DestroyedHouses;
    DROP TABLE IF EXISTS DamagedHouses;
    DROP TABLE IF EXISTS PeopleDamage;
    DROP TABLE IF EXISTS Temp;
'''

insert_bulk = '''
    CREATE TABLE Temp (
        year INT NULL,
        month INT NULL,
        day INT NULL,
        hour INT NULL,
        minute INT NULL,
        second FLOAT NULL,
        tsunami_event_validity INT NULL,
        tsunami_cause_code INT NULL,
        earthquake_magnitude FLOAT NULL,
        deposits INT NULL,
        latitude FLOAT NULL,
        lngitude FLOAT NULL,
        max_water_height FLOAT NULL,
        runups INT NULL,
        tsunami_magnitude_ida FLOAT NULL,
        intensity FLOAT NULL,
        total_deaths INT NULL,
        total_missing INT NULL,
        total_missing_desc INT NULL,
        total_injuries INT NULL,
        total_damage_mil FLOAT NULL,
        total_damage_desc INT NULL,
        total_houses_destroyed INT NULL,
        total_houses_damaged INT NULL,
        country VARCHAR(50) NULL,
        location_name VARCHAR(130) NULL,
    );

    BULK INSERT Temp
    FROM '/tsunamis.csv'
    WITH (
        DATAFILETYPE = 'char',
        FIRSTROW=3,
        FIELDTERMINATOR = ',',
        ROWTERMINATOR = '0x0a');

    select * from Temp;

'''

queries = [
    '''
        SELECT (SELECT COUNT(*) FROM Countries) as countries_count,
        (SELECT COUNT(*) FROM Locations) as locations_count,
        (SELECT COUNT(*) FROM Dates) as dates_count,
        (SELECT COUNT(*) FROM GeneralDamage) as general_damage_count,
        (SELECT COUNT(*) FROM PeopleDamage) as people_damage_count,
        (SELECT COUNT(*) FROM Tsunamis) as tsunamis_count,
        (SELECT COUNT(*) FROM Temp) as temp_count;
    ''',
    '''
        SELECT d.[year] as Year, COUNT(*) as 'Tsunami Count' FROM Tsunamis t
        INNER JOIN Dates d on t.idDates = d.idDates
        GROUP BY d.year
        ORDER BY d.year DESC;
    ''',
    '''
        SELECT c.countryName as Country, d.year as 'Year of Tsunami'
        FROM Tsunamis t
        INNER JOIN Dates d on t.idDates = d.idDates
        INNER JOIN Locations l on t.idLocations = l.idLocations
        INNER JOIN Countries c on c.idCountries = l.idCountry
        ORDER BY c.countryName;
    ''',
    '''
        SELECT c.countryName as Country, CAST(ROUND(AVG(gd.totalDamage),2) AS DEC(10,2)) as 'Total Damage AVG'
        FROM Tsunamis t
        INNER JOIN GeneralDamage gd on gd.idGeneralDamage = t.idGeneralDamage
        INNER JOIN Locations l on t.idLocations = l.idLocations
        INNER JOIN Countries c on c.idCountries = l.idCountry
        GROUP BY c.countryName
        ORDER BY c.countryName;
    ''',
    '''
        SELECT c.countryName as Country, SUM(pd.totalDeaths) as 'Total Deaths'
        FROM Tsunamis t
        INNER JOIN PeopleDamage pd on pd.idPeopleDamage = t.idPeopleDamage
        INNER JOIN Locations l on t.idLocations = l.idLocations
        INNER JOIN Countries c on c.idCountries = l.idCountry
        GROUP BY c.countryName
        ORDER BY 'Total Deaths' DESC
        OFFSET 0 ROWS
        FETCH NEXT 5 ROWS ONLY;
    ''',
    '''
        SELECT d.year as Year, SUM(pd.totalDeaths) as 'Total Deaths'
        FROM Tsunamis t
        INNER JOIN PeopleDamage pd on pd.idPeopleDamage = t.idPeopleDamage
        LEFT JOIN Dates d on d.idDates = t.idDates
        GROUP BY d.year
        ORDER BY 'Total Deaths' DESC
        OFFSET 0 ROWS
        FETCH NEXT 5 ROWS ONLY;
    ''',
    '''
        SELECT d.year as Year, COUNT(*) as 'Tsunamis'
        FROM Tsunamis t
        LEFT JOIN Dates d on d.idDates = t.idDates
        GROUP BY d.year
        ORDER BY 'Tsunamis' DESC
        OFFSET 0 ROWS
        FETCH NEXT 5 ROWS ONLY;
    ''',
    '''
        SELECT c.countryName as Country, SUM(dh.totalHousesDestroyed) as 'Total Houses Destroyed'
        FROM Tsunamis t
        INNER JOIN DestroyedHouses dh on dh.idDestroyedHouses = t.idDestroyedHouses
        INNER JOIN Locations l on t.idLocations = l.idLocations
        INNER JOIN Countries c on c.idCountries = l.idCountry
        GROUP BY c.countryName
        ORDER BY 'Total Houses Destroyed' DESC
        OFFSET 0 ROWS
        FETCH NEXT 5 ROWS ONLY;
    ''',
    '''
        SELECT c.countryName as Country, SUM(dh.totalHousesDamaged) as 'Total Houses Damaged'
        FROM Tsunamis t
        INNER JOIN DamagedHouses dh on dh.idDamagedHouses = t.idDamagedHouses
        INNER JOIN Locations l on t.idLocations = l.idLocations
        INNER JOIN Countries c on c.idCountries = l.idCountry
        GROUP BY c.countryName
        ORDER BY 'Total Houses Damaged' DESC
        OFFSET 0 ROWS
        FETCH NEXT 5 ROWS ONLY;
    ''',
    '''
        SELECT c.countryName as Country, CAST(ROUND(AVG(t.maxWaterHeight),2) AS DEC(10,2)) as 'Max Water Height AVG'
        FROM Tsunamis t
        INNER JOIN DamagedHouses dh on dh.idDamagedHouses = t.idDamagedHouses
        INNER JOIN Locations l on t.idLocations = l.idLocations
        INNER JOIN Countries c on c.idCountries = l.idCountry
        GROUP BY c.countryName
        HAVING 'Max Water Hight AVG' <> 'NULL'
        ORDER BY c.countryName ASC;
    '''
]

CREATE TABLE danousna_td_zone (
    tripduration int,
    starttime timestamp,
    stoptime timestamp,
    start_station_id int,
    start_station_name text,
    start_station_latitude text,
    start_station_longitude text,
    end_station_id int,
    end_station_name text,
    end_station_latitude text,
    end_station_longitude text,
    bikeid int,
    usertype text,
    birth_year int,
    gender boolean,
    PRIMARY KEY ((start_station_id, end_station_id), starttime, bikeid)
);

CREATE TABLE danousna_td_time (
    tripduration int,
    starttime timestamp,
    startday text,
    starthour text,
    stoptime timestamp,
    start_station_id int,
    start_station_name text,
    start_station_latitude text,
    start_station_longitude text,
    end_station_id int,
    end_station_name text,
    end_station_latitude text,
    end_station_longitude text,
    bikeid int,
    usertype text,
    birth_year int,
    gender boolean,
    PRIMARY KEY ((startday, starthour), starttime, bikeid)
);

CREATE TABLE danousna_td_day (
    tripduration int,
    starttime timestamp,
    dayofweek int,
    stoptime timestamp,
    start_station_id int,
    start_station_name text,
    start_station_latitude text,
    start_station_longitude text,
    end_station_id int,
    end_station_name text,
    end_station_latitude text,
    end_station_longitude text,
    bikeid int,
    usertype text,
    birth_year int,
    gender boolean,
    PRIMARY KEY ((dayofweek), start_station_id, end_station_id, starttime, bikeid)
);

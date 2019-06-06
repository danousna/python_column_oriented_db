import re
from csv import excel, DictReader
import cassandra
import cassandra.cluster

dial = excel
dial.delimiter = ','

def read_file_gen(file_name):
    with open(file_name) as f:
        reader = DictReader(f, dialect=dial)
        for r in reader:
            yield dict(r)

def store_by_zone(c):
    gen = read_file_gen('citibike-tripdata.csv')
    i = 0

    # We remove last char of time data because cassandra doesn't like precision 4 on seconds.
    for item in gen:
        if i < 10:
            query = """
                INSERT INTO danousna_td_zone (
                    tripduration, 
                    starttime, 
                    stoptime, 
                    start_station_id, 
                    start_station_name, 
                    start_station_latitude, 
                    start_station_longitude, 
                    end_station_id, 
                    end_station_name, 
                    end_station_latitude, 
                    end_station_longitude, 
                    bikeid, 
                    usertype, 
                    birth_year, 
                    gender
                )
                VALUES ( 
                    {item['tripduration']},
                    {item['starttime'][:-1]},
                    {item['stoptime'][:-1]},
                    {item['start station id']},
                    {item['start station name']},
                    {item['start station latitude']},
                    {item['start station longitude']},
                    {item['end station id']},
                    {item['end station name']},
                    {item['end station latitude']},
                    {item['end station longitude']},
                    {item['bikeid']},
                    {item['usertype']},
                    {item['birth year']},
                    {item['gender']} 
                 )
            """
            c.execute(query)
        else:
            break
        i = i + 1

def store_by_day(c):
    gen = read_file_gen('citibike-tripdata.csv')
    i = 0

    c.execute("""
        CREATE TABLE IF NOT EXISTS danousna_citibike_station.day (
            day_date text,
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

            PRIMARY KEY (day_date)
        )
    """)

    # We remove last char of time data because cassandra doesn't like precision 4 on seconds.
    for item in gen:
        if i < 10:
            dateparser = re.compile(
                "(?P<year>\d+)-(?P<month>\d+)-(?P<day>\d+) (?P<hour>\d+):(?P<minute>\d+):(?P<seconds>\d+\.?\d*)"
            )
            match_start = dateparser.match(item["starttime"])
            if not match_start:
                continue
            start = match_start.groupdict()
            item["day_date"] = start["year"] + '-' + start["month"] + '-' + start["day"]

            query = "INSERT INTO danousna_citibike_station.day (day_date, tripduration, starttime, stoptime, start_station_id, start_station_name, start_station_latitude, start_station_longitude, end_station_id, end_station_name, end_station_latitude, end_station_longitude, bikeid, usertype, birth_year, gender) VALUES ('{}', {}, {}, {}, {}, '}', '{}', '{}', {}, '{}', '{}', '{}', {}, '{}', {}, {} )".format(
                item['day_date'], 
                item['tripduration'],
                item['starttime'][:-1], 
                item['stoptime'][:-1], 
                item['start station id'], 
                item['start station name'], 
                item['start station latitude'], 
                item['start station longitude'], 
                item['end station id'], 
                item['end station name'], 
                item['end station latitude'], 
                item['end station longitude'], 
                item['bikeid'], 
                item['usertype'], 
                item['birth year'], 
                item['gender']
            )
            print(query)
            # c.execute(query)
        else:
            break
        i = i + 1

def tripduration_distribution(c):
    # Get min and max
    result =  c.execute("select min(tripduration) as min, max(tripduration) as max from chembise_tmp.day_bike where day = '2019-04-01';")
    
    spacing = (result.max - result.max) / 10
    hist = []
    for i in range(10):
        hist[i] = {
            'min': result.min + i * spacing
            'max': result.min + (i + 1) * spacing
            'n': 0
        }
        print(hist[i])

    rows = c.execute("select * from chembise_tmp.day_bike where day = '2019-04-01';")
    

c = cassandra.cluster.Cluster(['localhost'])
c = c.connect('danousna_citibike_station')

# store_by_zone(c)
# store_by_day(c)

tripduration_distribution(c)

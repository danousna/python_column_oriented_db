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
        create table danousna_citibike_station.day (
            day_date text,
            tripduration int, 
            starttime timestamp, 
            stoptime timestamp, 
            start_station_id int, 
            start_station_name int, 
            start_station_latitude text, 
            start_station_longitude text, 
            end_station_id int, 
            end_station_name text, 
            end_station_latitude text, 
            end_station_longitude text, 
            bikeid int, 
            usertype text, 
            birth_year int, 
            gender boolean
        )
    """)

    # We remove last char of time data because cassandra doesn't like precision 4 on seconds.
    for item in gen:
        if i < 10:
            query = """
            """
            # c.execute(query)
        else:
            break
        i = i + 1

c = cassandra.cluster.Cluster(['localhost'])
c = c.connect('danousna_citibike_station')

# store_by_zone(c)
store_by_day(c)

results = c.execute('select * from danousna_citibike_station.day;')

for r in results:
    print(r)

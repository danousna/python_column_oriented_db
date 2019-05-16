from csv import excel, DictReader
import lmdb

dial = excel
dial.delimiter = ','

def read_file_gen(file_name):
    with open(file_name) as f:
        reader = DictReader(f, dialect=dial)
        for r in reader:
            yield dict(r)

def print_lines():
    gen = read_file_gen('citibike-tripdata.csv')
    i = 0

    for item in gen:
        if i < 10:
            print(str(i) + '\n')
            print(item['tripduration'] + '\n')
        i = i + 1

    print(str(i))

print_lines()

# env = lmdb.open('db')

# with env.begin(write=True) as txn:

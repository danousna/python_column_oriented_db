from csv import excel, DictReader
import lmdb
import json

dial = excel
dial.delimiter = ','

def read_file_gen(file_name):
    with open(file_name) as f:
        reader = DictReader(f, dialect=dial)
        for r in reader:
            yield dict(r)

def store_by_zone():
    gen = read_file_gen('citibike-tripdata.csv')
    db = lmdb.open('db_zone')
    
    with db.begin(write=True) as txn:
        i = 0

        for item in gen:
            if i < 10:
                start_key = str(item['start station id']).encode()
                end_key = str(item['end station id']).encode()

                start_val = txn.get(start_key)
                if start_val is None:
                    txn.put(start_key, json.dumps({'start': [item], 'end': []}).encode())
                else:
                    start_val = json.loads(start_val)
                    start_val['start'].append(item)
                    txn.put(start_key, json.dumps(start_val).encode())

                end_val = txn.get(end_key)
                if end_val is None:
                    txn.put(end_key, json.dumps({'start': [], 'end': [item]}).encode())
                else:
                    end_val = json.loads(end_val)
                    end_val['end'].append(item)
                    txn.put(end_key, json.dumps(end_val).encode())
            else:
                break
            i = i + 1

store_by_zone()

# Verify
db = lmdb.open('db_zone')
with db.begin(write=True) as txn:
    data = txn.get(b'254')
    data = json.loads(data)
    print(data['start'])

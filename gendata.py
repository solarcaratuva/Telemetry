import json
import time
import random
import psycopg2
from config import POSTGRES
from datetime import datetime

run_params = {'create_run': False}

should_create_run = input("Create a new run? Type yes to create a new run: ")
if should_create_run.lower() == 'yes':
    run_params['create_run'] = True
    run_params['title'] = input("Run title: ")
    run_params['driver'] = input("Run driver: ")
    run_params['location'] = input("Run location: ")
    run_params['description'] = input("Run description: ")


def get_random_val(typ):
    if typ == 'bool':
        if random.random() < 0.5:
            return True
        return False
    elif typ == 'int':
        return random.randint(10, 20)
    elif typ == 'float':
        return random.randint(1000, 2000) / 100
    print("ERROR UNKNOWN TYPE:", typ)
    assert(False)

def create_run(cur, run_params):
    column_string = 'run_id,title,driver,location,description,timestamp'
    run_id = get_latest_run_id(cur) + 1
    arr_string = '{},{},{},{},{},{}'.format(run_id, run_params['title'], run_params['driver'], run_params['location'], run_params['description'], str(datetime.now()))
    sql = 'INSERT INTO "Runs"({}) VALUES({}) RETURNING id;'.format(column_string, arr_string)
    cur.execute(sql)
    row_id = cur.fetchone()
    print("Created run: ", row_id)


def get_latest_run_id(cur):
    cur.execute('SELECT run_id FROM "Runs" t1 WHERE NOT EXISTS (SELECT * FROM "Runs" t2 WHERE t2.timestamp > t1.timestamp);')
    latest_run_id = cur.fetchone()[0]
    return int(latest_run_id)


conn = psycopg2.connect('dbname={} user={} password={}'.format(POSTGRES['db'], POSTGRES['user'], POSTGRES['pw']))
cur = conn.cursor()

# cur.execute('SELECT * FROM "TestData";')
# for i in range(100):
#     print(cur.fetchone())
# print(1/0)

# Create a run if asked to
if run_params['create_run']:
    create_run(run_params)

# Get the latest run_id (by timestamp) using relational query
latest_run_id = get_latest_run_id(cur)

json_format = json.load(open("app/data.json"))
json_format['timestamp'] = 'float' # Add timestamp
json_format['run_id'] = 'int' # Add run id

columns = [i for i in json_format]
column_string = ','.join(columns)

data = []
for i in range(100):
    arr = []
    for key in columns:
        if key == 'timestamp':
            arr.append(time.time())
        elif key == 'run_id':
            arr.append(latest_run_id)
        else:
            arr.append(get_random_val(json_format[key]))

    arr_string = ','.join([str(i) for i in arr])
    sql = 'INSERT INTO "TestData"({}) VALUES({}) RETURNING id;'.format(column_string, arr_string)
    cur.execute(sql)
    row_id = cur.fetchone()
    print(row_id)
    conn.commit()
    time.sleep(3)

conn.commit()
cur.close()

import json
import time
import random
import psycopg2
import sqlite3

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


# conn = psycopg2.connect('dbname=telemetry user=postgres password=postgres')
conn = sqlite3.connect('app.db')

cur = conn.cursor()

# cur.execute('SELECT * FROM "TestData";')
# for i in range(100):
#     print(cur.fetchone())
# print(1/0)

json_format = json.load(open("app/data.json"))
json_format['timestamp'] = 'float' # Add timestamp
json_format['run_id'] = 'int' # Add run id
columns = [i for i in json_format]
column_string = ','.join(columns)
# print(columns)
# print(1/0)
data = []
for i in range(100):
    arr = []
    for key in columns:
        if key == 'timestamp':
            arr.append(time.time())
        elif key == 'run_id':
            arr.append(5)
        else:
            arr.append(get_random_val(json_format[key]))
    # json_string = json.dumps({columns[i]: arr[i] for i in range(len(columns))})

    arr_string = ','.join([str(i) for i in arr])
    sql = 'INSERT INTO "TestData"({}) VALUES({}) RETURNING id;'.format(column_string, arr_string)
    print(sql)
    cur.execute(sql)
    row_id = cur.fetchone()
    print(row_id)
    conn.commit()
    time.sleep(3)

conn.commit()
cur.close()

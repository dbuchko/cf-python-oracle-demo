from flask import Flask
import os
import json
import cx_Oracle

app = Flask(__name__)

# Get host & port from environment variable or choose 9099 as local default
hostIp = os.getenv('CF_INSTANCE_INTERNAL_IP', '0.0.0.0')
port = int(os.getenv("PORT", 9099))

# Get DB credentials
if 'VCAP_SERVICES' in os.environ:
    services = json.loads(os.getenv('VCAP_SERVICES'))

    # Assume OracleDB is first user-provided service.  Ideally should search for it by name.
    db_env = services['user-provided'][0]['credentials']
else:
    db_env = dict(dsn='localhost/xepdb1', username='system', password='')

# Connect to database
connection = cx_Oracle.connect(
    user=db_env['username'],
    password=db_env['password'],
    dsn=db_env['dsn'])

print("Successfully connected to Oracle Database")

cursor = connection.cursor()

# Create a table
cursor.execute("""
    begin
        execute immediate 'drop table keyvalue';
        exception when others then if sqlcode <> -942 then raise; end if;
    end;""")

cursor.execute("""
    create table keyvalue (
        id number generated always as identity,
        mykey varchar2(4000),
        creation_ts timestamp with time zone default current_timestamp,
        myvalue varchar2(4000),
        primary key (id))""")

@app.route('/')
def keys():
    if connection:
        # Query the rows back
        rows=''
        for row in cursor.execute('select mykey, myvalue from keyvalue'):
            cur_row = 'mykey=' + row[0] + ', myvalue=' + row[1] + '\n'
            rows+=cur_row
        return rows
    else:
        return 'No DB connection available!'

@app.route('/<key>/<s>')
def add_value(key, s):
    if connection:
        # Insert some data
        rows = [ (key, s)]
        cursor.executemany("insert into keyvalue (mykey, myvalue) values(:1, :2)", rows)
        print(cursor.rowcount, "Rows Inserted")
        connection.commit()
        return 'Added {}, {}.'.format(key, s)

    else:
        abort(503)

if __name__ == '__main__':
    # Run the app, listening on the instance IP with our chosen port number
    app.run(host=hostIp, port=port)

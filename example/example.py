from flask import Flask
import os
import json
import cx_Oracle

app = Flask(__name__)

# Get port from environment variable or choose 9099 as local default
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
        key varchar2(4000),
        creation_ts timestamp with time zone default current_timestamp,
        value varchar2(4000),
        primary key (id))""")

@app.route('/')
def keys():
    if connection:
        # Query the rows back
        for row in cursor.execute('select key, value from todoitem'):
            rows+='key=' + row[0] + ', value=' + row[1] + '\n'
        return rows
    else:
        return 'No DB connection available!'

@app.route('/<key>/<s>')
def add_value(key, s):
    if connection:
        # Insert some data
        rows = [ (key, value )]
        cursor.executemany("insert into todoitem (description, done) values(:1, :2)", rows)
        print(cursor.rowcount, "Rows Inserted")
        connection.commit()
        return 'Added {} to {}.'.format(s, key)

    else:
        abort(503)

if __name__ == '__main__':
    # Run the app, listening on all IPs with our chosen port number
    app.run(host='0.0.0.0', port=port)

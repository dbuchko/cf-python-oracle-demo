#from flask import Flask
import os
import json
import cx_Oracle

#app = Flask(__name__)

# Get port from environment variable or choose 9099 as local default
#port = int(os.getenv("PORT", 9099))

# Get Redis credentials
if 'VCAP_SERVICES' in os.environ:
    services = json.loads(os.getenv('VCAP_SERVICES'))
    db_env = services['oracledb'][0]['credentials']
else:
    db_env = dict(dsn='localhost', username='system', password='')
db_env['host'] = db_env['dsn']
del db_env['dsn']
db_env['username'] = int(db_env['username'])

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
        execute immediate 'drop table todoitem';
        exception when others then if sqlcode <> -942 then raise; end if;
    end;""")

cursor.execute("""
    create table todoitem (
        id number generated always as identity,
        description varchar2(4000),
        creation_ts timestamp with time zone default current_timestamp,
        done number(1,0),
        primary key (id))""")

# Insert some data

rows = [ ("Task 1", 0 ),
         ("Task 2", 0 ),
         ("Task 3", 1 ),
         ("Task 4", 0 ),
         ("Task 5", 1 ) ]

cursor.executemany("insert into todoitem (description, done) values(:1, :2)", rows)
print(cursor.rowcount, "Rows Inserted")

connection.commit()

# Now query the rows back
for row in cursor.execute('select description, done from todoitem'):
    if (row[1]):
        print(row[0], "is done")
    else:
        print(row[0], "is NOT done")

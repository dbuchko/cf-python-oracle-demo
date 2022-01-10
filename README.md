# Cloud Foundry Sample Python Application Connecting to Oracle
Simple Python demo app that connects to an Oracle DB.  The app is based on the example provided [here](https://www.oracle.com/database/technologies/appdev/python/quickstartpythononprem.html#linux-tab).

## Instructions
1. After you have cloned the repository to your local machine, you download the Oracle client from https://download.oracle.com/otn_software/linux/instantclient/214000/instantclient-basic-linux.x64-21.4.0.0.0dbru.zip and extract it into the `example` subdirectory.  You should now have an `example/instantclient_21_4` subdirectory created.
2. Create an `oracledb.json` file with the `user`, `password`, and `dsn` in the following format to point to your Oracle instance:
```
{
  "username": "system",
  "password": "xxxxx",
  "dsn": "localhost/xepdb1"
}
```

3. Create a user-provided service that connects to your external Oracle instance:
`cf cups oracledb -p oracledb.json`

4. Push the app to Cloud Foundry from the root project directory, using `cf push`.

5. The app has 2 endpoints:  the root `/` endpoint will query the table of all keys and values; and the `/<key>/value` endpoint will add a key/value pair to the table.

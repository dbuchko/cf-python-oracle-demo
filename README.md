# Cloud Foundry Sample Python Application that connects to Oracle
Simple Python demo app that connects to an Oracle DB.  The app is based on the example provided [here](https://www.oracle.com/database/technologies/appdev/python/quickstartpythononprem.html#linux-tab).

## Instructions
1. After you have cloned the repository to your local machine, you download the Oracle client from https://download.oracle.com/otn_software/linux/instantclient/214000/instantclient-basic-linux.x64-21.4.0.0.0dbru.zip and extract it into the `example` subdirectory.  You should now have an `example/instantclient_21_4` subdirectory created.
2. Update the `user`, `password`, and `dsn` in the `example.py` source file to point to your Oracle instance.

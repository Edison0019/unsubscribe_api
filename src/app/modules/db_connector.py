import mysql.connector
import os
import json
with open(os.path.join(os.path.dirname(os.getcwd()),'app','files','auth.json')) as f:
    auth = json.load(f)

def connection():
    mdb = mysql.connector.connect(
        db = auth['db'],
        password = auth['pass'],
        host = auth['host'],
        user = auth['user']
    )

    return mdb
from datetime import datetime, timedelta
from sqlalchemy import create_engine
import pymysql
import os
import pandas as pd
import sys

USER = os.environ.get('MySQLuser')
PASS = os.environ.get('MySQLpass')
if USER is None or PASS is None:
    print('No username and password found')
    sys.exit()
def dateformat(date):
    year = str((date - timedelta(days=1)).year)
    if len(str((date - timedelta(days=1)).month)) == 1:
        month = '0' + str((date - timedelta(days=1)).month)
    else:
        month = str((date - timedelta(days=1)).month)
    if len(str((date - timedelta(days=1)).day)) == 1:
        day = '0' + str((date - timedelta(days=1)).day)
    else:
        day = str((date - timedelta(days=1)).day)
    return year+month+day

def toSQL(data, date):
    engine = create_engine("mysql+pymysql://{}:{}@{}/{}".format(USER, PASS, '127.0.0.1:3306', 'stock'))

    if engine is None:
        print('Invalid username or password.')
        sys.exit()
    try:
        df = pd.DataFrame(data)
        print(type(df))
        df.to_sql(date,con=engine)
        print('Successfully Wrote {} in Mysql database.'.format(date))
    except Exception as e:
        print('Error: ',e)
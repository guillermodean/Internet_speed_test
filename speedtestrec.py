import pandas as pd
import speedtest as st
from datetime import datetime
from sqlalchemy import create_engine

engine= create_engine('sqlite:///internet_speed.sqlite',echo=False)

#TODO change connection to mysql

"""def get_connection():
    try:
        db = mysql.connect(
            host="localhost",
            user="root",
            password="Guillermo11",
            db="internet_speed"
        )
    except ValueError:
        print('error de conexión')

    return db"""

def get_new_speeds():
    speed_test=st.Speedtest()
    speed_test.get_best_server()

    #get ping
    ping=speed_test.results.ping

    #perform downloada and upload speed tests (bits per s)
    download=speed_test.download()
    upload=speed_test.upload()

    #convert download an upload speeds to megabits persecond
    download_mbs=round(download/(10**6),2)
    upload_mbs = round(upload / (10 ** 6), 2)

    return (ping,download_mbs,upload_mbs)

def update_sql(internetspeeds,db):
    date_today=datetime.today().strftime("%d%m%Y")
    results_df=pd.DataFrame([[internet_speeds[0],internet_speeds[1],internet_speeds[2]]],columns=["ping(ms)","Download (Mbs)","upload (Mbs)"],index=[date_today])
    try:
        sqlimport=pd.read_sql(sql='Select * FROM speedtests',con=engine)
        print(sqlimport)
        results_df.to_sql(name='speedtests', con=engine, if_exists='append')
        resultadosql = engine.execute("SELECT * FROM speedtests").fetchall()

    except:
        results_df.to_sql(name='speedtests', con=engine)
        resultadosql = engine.execute("SELECT * FROM speedtests").fetchall()


    return resultadosql

internet_speeds=get_new_speeds()
#db=get_connection()
update_sql(internet_speeds,engine)


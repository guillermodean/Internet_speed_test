import pandas as pd
import speedtest as st
from datetime import datetime
from sqlalchemy import create_engine
import pymysql

engine= create_engine('mysql+pymysql://root:Guillermo11@127.0.0.1/internet_speed', pool_recycle=3600)
dbConnection=engine.connect()

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
    date_today=datetime.today().strftime("%Y-%m-%d")
    results_df=pd.DataFrame([[internet_speeds[0],internet_speeds[1],internet_speeds[2],date_today]],columns=["ping(ms)","Download (Mbs)","upload (Mbs)","DATE"])
    #subir la tabla omitiendo el indice que es autonumerico de mysql y añadiendo registros nuevos.
    results_df.to_sql(name='speedtests', con=engine, if_exists='append',index=False)
    return results_df

internet_speeds=get_new_speeds()
update_sql(internet_speeds,engine)

frame=pd.read_sql("SELECT * from internet_speed.speedtests", dbConnection);
print(frame.head())

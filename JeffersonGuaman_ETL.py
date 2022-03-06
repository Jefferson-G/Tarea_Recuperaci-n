import pandas as pd
from datetime import datetime
from sqlalchemy import create_engine
import psycopg2


def log(logfile, message):
    timestamp_format = '%H:%M:%S-%h-%d-%Y'
    #Hour-Minute-Second-MonthName-Day-Year
    now = datetime.now() # get current timestamp
    timestamp = now.strftime(timestamp_format)
    with open(logfile,"a") as f: 
        f.write('[' + timestamp + ']: ' + message + '\n')
        print(message)

def transform():
    df = pd.read_csv('Building_Permits.csv')
    df=df.fillna("N/A")
    df=df.drop_duplicates()
    df['Permit Type Definition'] = df['Permit Type Definition'].str.upper()
    df['Description'] = df['Description'].str.upper()
    df['Current Status'] = df['Current Status'].str.upper()
    df['Street Name'] = df['Current Status'].str.upper()
    df['Street Suffix'] = df['Current Status'].str.upper()
    df['Existing Use'] = df['Existing Use'].str.upper()
    df['Proposed Use'] = df['Existing Use'].str.upper()
    df['Existing Construction Type Description'] = df['Existing Construction Type Description'].str.upper()
    df['Proposed Construction Type Description'] = df['Proposed Construction Type Description'].str.upper()
    df['Neighborhoods - Analysis Boundaries'] = df['Neighborhoods - Analysis Boundaries'].str.upper()
    df.to_csv("Building_Permits_Limpio.csv")
   
def load():
    df_clean = pd.read_csv('Building_Permits_Limpio.csv')
    """ Connect to the PostgreSQL database server """
    conn_string = 'postgresql://postgres:12345@localhost:5433/Permits'
    conn = psycopg2.connect(conn_string)
    db = create_engine(conn_string)
    try:
        log(logfile, "-------------------------------------------------------------")
        log(logfile, "Inicia Fase De Carga")
        df_clean.to_sql('buildingpermits', db)
        conn.autocommit = True
        log(logfile, "Finaliza Fase De Carga")
        log(logfile, "-------------------------------------------------------------")
    except (Exception, psycopg2.DatabaseError) as error:
        print(error)
    finally: 
        if conn is not None:
            conn.close()
            print('Database connection closed.') 


if __name__ == '__main__':
    
    logfile = "ProcesoETL_logfile.txt"
    log(logfile, "ETL Trabajo iniciado.")
    transform()
    load()
    log(logfile, "ETL Trabajo finalizado.")

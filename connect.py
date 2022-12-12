import psycopg2
from config import config_reader
import sqlalchemy
import pandas as pd

#create table sql
c_sql = """CREATE TABLE IF NOT EXISTS GENRE_DATA ( 
             danceability NUMERIC (10,10),
             energy	NUMERIC (10,10),
             key	NUMERIC (10,10),
             loudness	NUMERIC (10,10),
             mode	NUMERIC (10,10),
             speechiness NUMERIC (10,10),	
             acousticness	NUMERIC (10,10),
             instrumentalness NUMERIC (10,10),	
             liveness NUMERIC (10,10),	
             valence NUMERIC (10,10),	
             tempo	NUMERIC (10,10),
             id	VARCHAR(150), 
             duration_ms NUMERIC (10,10),	
             time_signature	NUMERIC (10,10),
             popularity	INTEGER,
             genre	VARCHAR(50),
             sub_genre VARCHAR(50)
            )"""



def init_db():
    
    conn = None
    try:
        #read db configs
        params = config_reader()
        conn_str="postgresql://{}/{}?user={}&password={}".format(params['host'], params['database'], params['user'], params['password'])
        print(params)
        print(conn_str)

        #connect
        print('Connecting to DB ...')
        conn = psycopg2.connect(**params)
        print(conn)
    except (Exception, psycopg2.DatabaseError) as error:
        print(error)


    return conn, conn_str

def create_table():

    conn,_ = init_db()
    
    #cursor
    cur = conn.cursor() 

    # execute create table statement
    try : 
        cur.execute(c_sql)
        print("Table Created!")
        conn.commit()
        cur.close()

    except :
        print("Cannot create table!")        

    finally:
        if conn is not None:
            conn.close()
            print('DB connection closed..')


def write_to_db(df):

        _, conn_str = init_db()
    
        #cursor
        #cur = conn.cursor()

        #engine
        engine = sqlalchemy.create_engine(conn_str)
        print(engine)
        # execute create table statement
        try : 

            with engine.connect().execution_options(autocommit=True) as conn:
                df.to_sql('GENRE_DATA', con=conn, if_exists='append', index=False)
            #cur.close()
            print("Data inserted!")

        except :
            print("Cannot insert data!")

        if conn is not None:
            conn.close()
            print('DB connection closed..')
    

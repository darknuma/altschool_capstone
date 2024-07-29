import psycopg2
from io import StringIO
import os
import csv
import pandas as pd

def csv_to_pgsql(csv_file, table_name, db_params):
    df = pd.read_csv(csv_file)
    df.to_sql(table_name, doc)
    pass

def insert_to_table():
    db_params ={
        'host': 'postgres',
        'database': 'postgres',
        'user': 'postgres',
        'password':'postgres',
        'port': 5432
    }
    try:
        conn = psycopg2.connect(**db_params)
        cursor = conn.cursor()
        conn.commit()
        insert_query = f"COPY {table_name} FROM STDIN WITH (format 'csv', header 'true')"
        inserts = conn.copy_from()

        conn.execute(insert_query)
    except:
        pass
    finally:
        pass



    
def create_table():

    with open () as f:
        f = csv.

        

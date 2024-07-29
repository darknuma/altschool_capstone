import pandas as pd
import psycopg2
import os
from io import StringIO
from typing import Dict, List, Tuple
from dotenv import load_dotenv

load_dotenv(dotenv_path='.env')




def get_database_connection(db_params: Dict[str, str]) -> Tuple[psycopg2.extensions.connection, psycopg2.extensions.cursor]:
    """Establish a database connection and return the connection and cursor objects."""
    try:
        print("Attempting to connect to the database with parameters:", db_params)
        conn = psycopg2.connect(**db_params)
        cur = conn.cursor()
        print("Connection successful")
        return conn, cur
    except Exception as e:
        print(f"Error connecting to database: {e}")
        return None


def close_database_connection(conn: psycopg2.extensions.connection, cur: psycopg2.extensions.cursor) -> None:
    """Close the database cursor and connection."""
    cur.close()
    conn.close()

def csv_to_postgresql(csv_file: str, table_name: str, conn: psycopg2.extensions.connection, 
                      cur: psycopg2.extensions.cursor, schema: str = 'olist') -> None:
    """Load data from a CSV file into a PostgreSQL table."""
    df = pd.read_csv(os.path.join('data', csv_file))
    
    buffer = StringIO()
    df.to_csv(buffer, index=False, header=False)
    buffer.seek(0)
    
    try:
        cur.copy_from(buffer, f"{schema}.{table_name}", sep=',')
        conn.commit()
    except (Exception, psycopg2.DatabaseError) as error:
        print(f"Error: {error}")
        conn.rollback()

def process_csv_files(csv_files: List[Tuple[str, str]], db_params: Dict[str, str]) -> None:
    """Process a list of CSV files and load them into their respective database tables."""
    conn, cur = get_database_connection(db_params)

    for csv_file, table_name in csv_files:
        print(f"Ingesting {csv_file} into {table_name}")
        try:
            csv_to_postgresql(csv_file, table_name, conn, cur)
            print(f"Completed ingestion of {csv_file}")
        except Exception as e:
            print(f"Error ingesting {csv_file}: {str(e)}")

    close_database_connection(conn, cur)

def run_etl(db_params: Dict[str, str], csv_files: List[Tuple[str, str]]) -> None:
    """Main ETL function to orchestrate the data loading process."""
    result =  get_database_connection(db_params)
    if result is None:
        print("Failed to connect to the database")
        return
    process_csv_files(csv_files, db_params)

# Example usage:
db_params = {
    'host': 'localhost',
    'database': 'ecommerce',
    'user': os.getenv('POSTGRES_USER'),
    'password': os.getenv('POSTGRES_PASSWORD'),
    'port': 5434
}

csv_files = [
    ('olist_customers_dataset.csv', 'customers'),
    ('olist_geolocation_dataset.csv', 'geolocation_data'),
    ('olist_order_items_dataset.csv', 'order_items'),
    ('olist_order_payments_dataset.csv', 'order_payments'),
    ('olist_order_reviews_dataset.csv', 'order_reviews'),
    ('olist_orders_dataset.csv', 'orders'),
    ('olist_products_dataset.csv', 'products'),
    ('product_category_name_translation.csv', 'product_category_translation')
]

run_etl(db_params, csv_files)  # Uncomment this line to run the ETL process
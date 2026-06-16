import sqlite3
import pandas as pd
import os

DB_PATH = "healthcare_saas.db"
SCHEMA_PATH = "sql/schema.sql"
RAW_DATA_DIR = "data/raw"

def init_db():
    print("Initializing database...")
    # Read schema.sql
    with open(SCHEMA_PATH, 'r') as f:
        schema_sql = f.read()
    
    # Connect and execute schema
    conn = sqlite3.connect(DB_PATH)
    cursor = conn.cursor()
    cursor.executescript(schema_sql)
    conn.commit()
    return conn

def load_data(conn):
    tables = [
        ("services.csv", "services"),
        ("incidents.csv", "incidents"),
        ("availability.csv", "availability"),
        ("capacity.csv", "capacity"),
        ("sla_tracking.csv", "sla_tracking")
    ]
    
    for file_name, table_name in tables:
        file_path = os.path.join(RAW_DATA_DIR, file_name)
        if os.path.exists(file_path):
            print(f"Loading {file_name} into table '{table_name}'...")
            df = pd.read_csv(file_path)
            # Write to sqlite
            df.to_sql(table_name, conn, if_exists='replace', index=False)
            
            # Re-apply indexes since to_sql with replace drops the table and re-creates it
            # To preserve schema safely without replace, we can use append
            # But wait, we just initialized schema. Let's use if_exists='append' to keep the schema constraints.
        else:
            print(f"File {file_path} not found.")

def load_data_safe(conn):
    # Using append instead of replace to keep primary keys and constraints from schema.sql
    tables = [
        ("services.csv", "services"),
        ("incidents.csv", "incidents"),
        ("availability.csv", "availability"),
        ("capacity.csv", "capacity"),
        ("sla_tracking.csv", "sla_tracking")
    ]
    
    for file_name, table_name in tables:
        file_path = os.path.join(RAW_DATA_DIR, file_name)
        if os.path.exists(file_path):
            print(f"Loading {file_name} into table '{table_name}'...")
            df = pd.read_csv(file_path)
            # Clear existing data just in case
            conn.execute(f"DELETE FROM {table_name};")
            # Write to sqlite
            df.to_sql(table_name, conn, if_exists='append', index=False)
            
            # Print row counts
            cursor = conn.cursor()
            cursor.execute(f"SELECT COUNT(*) FROM {table_name}")
            count = cursor.fetchone()[0]
            print(f"-> Successfully loaded {count} rows into '{table_name}'.")
        else:
            print(f"File {file_path} not found.")

if __name__ == "__main__":
    connection = init_db()
    load_data_safe(connection)
    connection.close()
    print("Database load complete!")

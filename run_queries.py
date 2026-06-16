import sqlite3
import pandas as pd
import os
import re

DB_PATH = "healthcare_saas.db"
QUERIES_PATH = "sql/kpi_queries.sql"
OUTPUT_DIR = "data/processed"

def run_queries():
    print("Running KPI queries...")
    os.makedirs(OUTPUT_DIR, exist_ok=True)
    
    with open(QUERIES_PATH, 'r') as f:
        sql_content = f.read()
        
    # Split queries by semicolon, being careful to keep them clean
    queries = []
    current_query = []
    
    for line in sql_content.split('\n'):
        if line.strip() == '' or line.strip().startswith('--'):
            # It's a comment or empty line, can keep or ignore
            # Let's keep comments if we want to print them
            pass
        current_query.append(line)
        if line.strip().endswith(';'):
            queries.append('\n'.join(current_query))
            current_query = []

    conn = sqlite3.connect(DB_PATH)
    
    query_num = 1
    for query in queries:
        if not query.strip():
            continue
            
        print(f"Running Query {query_num}...")
        try:
            df = pd.read_sql_query(query, conn)
            output_file = os.path.join(OUTPUT_DIR, f"query_{query_num:02d}_result.csv")
            df.to_csv(output_file, index=False)
            print(f"-> Saved to {output_file} ({len(df)} rows)")
        except Exception as e:
            print(f"Error running Query {query_num}: {e}")
            
        query_num += 1

    conn.close()
    print("All queries completed successfully!")

if __name__ == "__main__":
    run_queries()

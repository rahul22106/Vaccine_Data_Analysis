import pandas as pd
from sqlalchemy import create_engine, text
from urllib.parse import quote_plus
import os

# MySQL Configuration
host = 'localhost'
database = 'vaccine_db'
user = 'root'
password = 'Rahulkr@10'
port = 3306

# URL encode the password to handle special characters
encoded_password = quote_plus(password)

# Create connection string
connection_string = f"mysql+mysqlconnector://{user}:{encoded_password}@{host}:{port}/"

# Create engine and database
engine = create_engine(connection_string)
with engine.connect() as conn:
    conn.execute(text(f"CREATE DATABASE IF NOT EXISTS {database}"))
    conn.commit()
    print(f"✅ Database '{database}' created/verified")

# Connect to the database
connection_string_with_db = f"mysql+mysqlconnector://{user}:{encoded_password}@{host}:{port}/{database}"
engine = create_engine(connection_string_with_db)

# Load all Excel files from processed folder
processed_folder = 'processed'
excel_files = [f for f in os.listdir(processed_folder) if f.endswith(('.xlsx', '.xls'))]

print(f"\nFound {len(excel_files)} Excel files\n")

for file in excel_files:
    file_path = os.path.join(processed_folder, file)
    table_name = file.replace('.xlsx', '').replace('.xls', '').replace('-', '_').replace(' ', '_').lower()
    
    print(f"Loading {file} -> {table_name}")
    
    # Read Excel and load to MySQL
    df = pd.read_excel(file_path)
    df.to_sql(table_name, con=engine, if_exists='replace', index=False, chunksize=1000)
    
    print(f"✅ Loaded {len(df)} rows\n")

print("✅ All files loaded successfully!")
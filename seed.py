import psycopg2
import os
from dotenv import load_dotenv
import argparse

load_dotenv()

# Database connection parameters
db_config = {
    "dbname": os.getenv("DB_NAME"),
    "user": os.getenv("DB_USER"),
    "password": os.getenv("DB_PASSWORD"),
    "host": os.getenv("DB_HOST"),
    "port": os.getenv("DB_PORT"),
}

org_data = {
    "name": "example_org",
    "api_key": "asdasfasd",
}

parser = argparse.ArgumentParser()
parser.add_argument("--name", required=True, help="Name of the org")
# TODO: we can later generate this ourselves also
parser.add_argument("--apikey", required=True,
                    help="api key of the org")
args = parser.parse_args()

# SQL statement to check for existing data
check_existing_data_sql = f"""
SELECT id FROM orgs
WHERE name = '{args.name}' OR api_key = '{args.apikey}';
"""

# SQL statement to insert data into the table
insert_sql = f"""
INSERT INTO orgs (name, api_key)
VALUES ('{args.name}', '{args.apikey}');
"""

try:
    # Establish a connection to the PostgreSQL database
    conn = psycopg2.connect(**db_config)

    # Create a cursor object
    cursor = conn.cursor()

    # Execute the query to check for existing data
    cursor.execute(check_existing_data_sql)
    existing_record = cursor.fetchone()

    if existing_record:
        print("Org with the same name or api_key already exists. Skipping insertion.")
    else:
        # Execute the SQL statement to insert data
        cursor.execute(insert_sql)

        # Commit the changes
        conn.commit()

        print("Data inserted successfully.")

    cursor.close()
    conn.close()

except (Exception, psycopg2.DatabaseError) as error:
    print("Error: ", error)

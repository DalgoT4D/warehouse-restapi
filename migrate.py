import psycopg2
import os
from dotenv import load_dotenv

load_dotenv()

# Database connection parameters
db_config = {
    "dbname": os.getenv("DB_NAME"),
    "user": os.getenv("DB_USER"),
    "password": os.getenv("DB_PASSWORD"),
    "host": os.getenv("DB_HOST"),
    "port": os.getenv("DB_PORT"),
}

# Define SQL statements to create tables
create_table_sql = """
CREATE TABLE IF NOT EXISTS orgs (
    id serial PRIMARY KEY,
    name varchar(255),
    api_key varchar(255)
);
"""

# Connect to the database and create tables
try:
    # Establish a connection to the PostgreSQL database
    conn = psycopg2.connect(**db_config)

    # Create a cursor object
    cursor = conn.cursor()

    # Execute the SQL statement to create tables
    cursor.execute(create_table_sql)

    # Commit the changes
    conn.commit()

    print("Tables created successfully.")

    cursor.close()
    conn.close()

except (Exception, psycopg2.DatabaseError) as error:
    print("Error: ", error)

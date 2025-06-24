from api_req import mock_data_fetch, fetch_weather_data
from pprint import pprint
import psycopg2

# pprint(mock_data_fetch())


def connect_to_db():
    print("connecting to Postgres database")
    try:
        # Establish a connection using with block
        #uncomment the following while working locally
        # with psycopg2.connect(
        #     dbname="test_db",
        #     user="safal",
        #     password="safal",
        #     host="localhost",
        #     port="5000"
        # ) as conn:
      
      
      # this is changed to work with docker   (host= service name and port as it is)
         with psycopg2.connect(
            dbname="test_db",
            user="safal",
            password="safal",
            host="postgres",
            port="5432"
        ) as conn:
            print("Successfully connected to database")
            
            # Example: Execute a simple query
            with conn.cursor() as cursor:
                cursor.execute("SELECT version();")
                db_version = cursor.fetchall()
                print("PostgreSQL database version:", db_version)
            
            return conn
            
    except psycopg2.OperationalError as e:
        print(f"Error connecting to PostgreSQL database: {e}")
        return None
    except Exception as e:
        print(f"An unexpected error occurred: {e}")
        return None
    


def create_table(conn):
    pprint("creating table if not exists")
    try:
        cursor = conn.cursor()
        cursor.execute("""
                       CREATE SCHEMA if NOT EXISTS dev;
                       CREATE TABLE IF NOT EXISTS dev.bronze_weatherstack_raw (
                           
                           id SERIAL PRIMARY KEY,
                           city TEXT,
                           temperature FLOAT,
                           weather_description TEXT,
                           wind_speed FLOAT,
                           time TIMESTAMP,
                           inserted_at TIMESTAMP DEFAULT NOW(),
                           utc_offset TEXT
                       )
                       """)
        
        conn.commit()
        print("table creation successful")
        
    except psycopg2.Error as e:
        print(f"table creation failed {e}")
        raise


def insert_records(conn,data):
    print("inserting records into the weather database")
    location = data["location"]
    weather = data["current"]
    try:
        cursor = conn.cursor()
        cursor.execute(
                        """
                        INSERT INTO dev.bronze_weatherstack_raw(
                           city,
                           temperature,
                           weather_description,
                           wind_speed,
                           time,
                           inserted_at,
                           utc_offset
                        )
                        VALUES (%s, %s, %s, %s, %s, NOW(), %s)
                        """,
                        (
                            location["name"] + ", " + location["country"],
                            weather["temperature"],
                            weather["weather_descriptions"][0],
                            weather["wind_speed"],
                            location["localtime"],
                            location["utc_offset"]
                        )
                      )
        conn.commit()
        print("record inserted into database")
        
    except psycopg2.Error as e:
        print(f"There was an error. {e}") 
        raise 

def main():
    try:
        print("from main: making connection")
        conn = connect_to_db()
        # data = mock_data_fetch()
        data = fetch_weather_data("d1963a071c7dd60c53c598395df4112a", "New York")
        print("from main: creating table if not present")
        create_table(conn)
        print("from main: inserting")
        insert_records(conn,data)
        print("from main: inserted")
        
    except Exception as e:
        print(f"an error occured in the execution {e}")
    
    finally:
        
        if "conn" in locals():
            conn.close()
            print("Connection to DB closed")


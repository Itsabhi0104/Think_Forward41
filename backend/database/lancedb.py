from lancedb import connect

DATABASE_URL = "db"

def get_connection():
    try:
        connection = connect(DATABASE_URL)
        return connection
    except Exception as e:
        print(f"Error connecting to LanceDB: {e}")
        return None

def close_connection(connection):
    if connection:
        connection.close()
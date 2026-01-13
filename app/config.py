import os

def get_db_path():
    db_path = os.getenv("SERVICE_DB_PATH")
    if not db_path:
        raise RuntimeError("SERVICE_DB_PATH environment variable is not set")
    return db_path

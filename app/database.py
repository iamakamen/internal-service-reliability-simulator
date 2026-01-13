import sqlite3
from app.config import get_db_path

def get_connection():
    db_path = get_db_path()
    return sqlite3.connect(db_path)

def get_shipment_counts():
    conn = get_connection()
    cursor = conn.cursor()

    cursor.execute("""
        SELECT status, COUNT(*)
        FROM shipments
        GROUP BY status
    """)

    results = cursor.fetchall()
    conn.close()

    return {status: count for status, count in results}

import sqlite3
import json
import os

# Database path from environment or default
db_path = os.environ.get('DATA_STORE_PATH') or os.path.join(os.getcwd(), 'data.db')

def get_db_connection():
    """Get a database connection"""
    conn = sqlite3.connect(db_path)
    conn.execute('''
        CREATE TABLE IF NOT EXISTS sync_data (
            user_id TEXT PRIMARY KEY,
            data TEXT NOT NULL
        )
    ''')
    conn.commit()
    return conn

def write(data, user_id):
    """Write data for a user"""
    try:
        json_body = json.dumps(data or {})
        conn = get_db_connection()
        conn.execute('''
            INSERT OR REPLACE INTO sync_data (user_id, data)
            VALUES (?, ?)
        ''', (user_id, json_body))
        conn.commit()
        conn.close()
        return "ok", 200
    except Exception as e:
        return f"Error writing data: {str(e)}", 500

def read(user_id):
    """Read data for a user"""
    try:
        conn = get_db_connection()
        cursor = conn.cursor()
        cursor.execute('SELECT data FROM sync_data WHERE user_id = ?', (user_id,))
        row = cursor.fetchone()
        conn.close()
        if row:
            data = json.loads(row[0])
            return data, 200
        else:
            return "User not found", 404
    except Exception as e:
        return f"Error reading data: {str(e)}", 500
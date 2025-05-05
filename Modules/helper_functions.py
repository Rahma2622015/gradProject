import sqlite3
import os
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker

uploaded_db_path = r"D:\gradProject\university_information.db"

def get_uploaded_session():
    global uploaded_db_path
    if not uploaded_db_path or not os.path.exists(uploaded_db_path):
        raise Exception("No database uploaded or file not found")

    engine = create_engine(f"sqlite:///{uploaded_db_path}")
    Session = sessionmaker(bind=engine)
    return Session()

def allowed_file(filename):
    return '.' in filename and filename.rsplit('.', 1)[1].lower() in {'db', 'sqlite'}

def get_connection(db_name):
    conn = sqlite3.connect(f"./{db_name}.db")
    conn.row_factory = sqlite3.Row
    return conn, conn.cursor()

def close_connection(conn):
    conn.commit()
    conn.close()
"""
- searching for database files
- storing and retrieving data from db
"""

import sqlite3
from pathlib import Path

class DataBase:
    
    @staticmethod
    def search_files(file_name):
        """Search for a file in the current directory and its subdirectories."""
        path = Path(__file__).resolve().parent
        for file in path.rglob(file_name):
            return True
        return False

    @staticmethod
    def connect_to_db(db_name=f'{Path(__file__).resolve().parent}/Project_SHIELD.db'):
        """Connect to the SQLite database."""
        db = sqlite3.connect(db_name)
        cr = db.cursor()
        return cr, db

    @staticmethod
    def create_db_tables(cr, db):
        """Create tables in the database if they do not exist."""
        cr.execute("CREATE TABLE IF NOT EXISTS KEY (key TEXT,iv TEXT , UNIQUE (key , iv))")
        db.commit()

    @staticmethod
    def insert_data(cr, db, data):
        """Insert data into the KEY table."""
        cr.execute(f"INSERT INTO KEY (key,iv) VALUES (?,?)",(data))
        db.commit()

    @staticmethod
    def get_data(cr):
        """Retrieve data from the KEY table."""
        cr.execute("SELECT * FROM KEY")
        result = cr.fetchall()
        return result

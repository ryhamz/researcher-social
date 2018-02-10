"""
This module contains example code for basic SQLite usage.
Feel free to modify this file in any way.
"""
import sqlite3

# on import create or connect to an existing db
# and turn on foreign key constraints
conn = sqlite3.connect("globus_challenge.db")
c = conn.cursor()
c.execute("PRAGMA foreign_keys = ON;")
conn.commit()


def initialize_db():
    """
    Creates tables in the database if they do not already exist.
    Make sure to clean up old .db files on schema changes.
    """
    try:
        c.execute("""
            CREATE TABLE projects (
                project_id TEXT PRIMARY KEY
            );
            """)
        conn.commit()
    except sqlite3.OperationalError:
        pass


def get_num_projects():
    """
    Example of a simple SQL query using SQLite
    """
    c.execute("SELECT COUNT(project_id) FROM projects")
    return c.fetchone()[0]

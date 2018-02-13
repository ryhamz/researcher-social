"""
This module contains example code for basic SQLite usage.
Feel free to modify this file in any way.
"""
import sqlite3

# on import create or connect to an existing db
# and turn on foreign key constraints
conn = sqlite3.connect("globus_challenge.db" , check_same_thread=False)
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
                project_id TEXT PRIMARY KEY,
                owner_id TEXT
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

def add_project(project_id, owner_id):
    """
    Inserts a new project entry
    """
    c.execute(''' INSERT INTO projects(project_id, owner_id)
        VALUES(?, ?) ''', (project_id, owner_id))
    conn.commit()
def delete_project(project_id):
    """
    Deletes the given project entry
    """
    c.execute(''' DELETE FROM projects
        WHERE project_id = ? ''', (project_id,))
    conn.commit()

def delete_all_projects():
    """
    Testing function, used to clean db
    """
    c.execute('DELETE FROM projects')
    conn.commit()

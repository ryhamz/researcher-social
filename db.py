"""
This module contains example code for basic SQLite usage.
Feel free to modify this file in any way.
"""
import sqlite3

# on import create or connect to an existing db
# and turn on foreign key constraints
conn = sqlite3.connect("globus_challenge.db" , check_same_thread=False)
conn.row_factory = sqlite3.Row
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
                project_name TEXT,
                owner_username TEXT,
                owner_id TEXT
            );
            """)

        conn.commit()
    except sqlite3.OperationalError:
        print "initialization error"
    c.execute("""
            CREATE TABLE comments (
                comment_id TEXT PRIMARY KEY,
                commenter_id TEXT,
                commenter_username TEXT,
                message TEXT,
                p_id TEXT,
                FOREIGN KEY(p_id) REFERENCES projects(project_id)
            );
            """)
    conn.commit()


def get_num_projects():
    """
    Example of a simple SQL query using SQLite
    """
    c.execute("SELECT COUNT(project_id) FROM projects")
    return c.fetchone()[0]


def get_comments_for_project(project_id):
    """
    Returns all comments for the given project_id
    """
    c.execute('''SELECT comment_id, commenter_id,
                 commenter_username, message FROM comments
                 WHERE p_id = ?''', (project_id,))
    return c.fetchall()

def delete_comments_for_project(project_id):
    """
    Deletes all comments for the given project_id
    """
    c.execute('''DELETE FROM comments
                 WHERE p_id = ?''', (project_id,))
    conn.commit()


def add_comment(comment_id, commenter_id, commenter_username, message, project_id):
    """
    Inserts a new comment
    """
    c.execute(''' INSERT INTO comments(comment_id, commenter_id, commenter_username, message, p_id)
        VALUES(?, ?, ?, ?, ?) ''', (comment_id, commenter_id, commenter_username, message, project_id))
    conn.commit()


def get_project_by_id(project_id):
    """
    Returns project with given id
    """
    c.execute('''SELECT * FROM projects
        WHERE project_id = ?''', (project_id,))
    return c.fetchone()


def add_project(project_id, project_name, owner_username, owner_id):
    """
    Inserts a new project entry
    """
    c.execute(''' INSERT INTO projects(project_id, project_name, owner_username, owner_id)
        VALUES(?, ?, ?, ?) ''', (project_id, project_name, owner_username, owner_id))
    conn.commit()


def delete_project(project_id):
    """
    Deletes the given project entry
    """
    c.execute(''' DELETE FROM projects
        WHERE project_id = ? ''', (project_id,))
    conn.commit()

def delete_owners_project(project_id, owner_id):
    """
    Deletes the given project entry, but check that the owner
    id matches.
    """
    c.execute(''' DELETE FROM projects
        WHERE project_id = ? and owner_id = ?''', (project_id, owner_id))
    result = c.rowcount
    conn.commit()
    if rowcount == 0:
        return False
    return True


def delete_all_projects():
    """
    Testing function, used to clean db
    """
    c.execute('DELETE FROM projects')
    conn.commit()



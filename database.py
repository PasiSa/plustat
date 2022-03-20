import sqlite3
import importlib
import sys
from sqlite3 import Error

def create_connection(db_file: str) -> sqlite3.Connection:
    """ create a database connection to a SQLite database """
    conn = None
    try:
        conn = sqlite3.connect(db_file)
    except Error as e:
        print(e)

    return conn


def execute_query(connection: sqlite3.Connection, query: str) -> None:
    cursor = connection.cursor()
    try:
        cursor.execute(query)
        connection.commit()
        print("Query executed successfully")
    except Error as e:
        print(f"The error '{e}' occurred")


def execute_read_query(connection: sqlite3.Connection, query: str):
    cursor = connection.cursor()
    result = None
    try:
        cursor.execute(query)
        result = cursor.fetchall()
        return result
    except Error as e:
        print(f"The error '{e}' occurred")


def create_monthly_table(db: sqlite3.Connection) -> None:
    query = """
    CREATE TABLE IF NOT EXISTS monthly(
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        year INTEGER NOT NULL,
        month INTEGER NOT NULL,
        submission_count INTEGER,
        submitters INTEGER
    );
    """
    execute_query(db, query)


def insert_monthly_entry(
    db: sqlite3.Connection,
    year: int,
    month: int,
    submission_count: int,
    submitters: int,
) -> None:
    query = f"""
    INSERT INTO
        monthly (year, month, submission_count, submitters)
    VALUES
        ({year}, {month}, {submission_count}, {submitters});
    """
    execute_query(db, query)


def build_monthly_dict(db: sqlite3.Connection) -> dict:
    query = """
    SELECT * from monthly order by year,month;
    """
    entries = execute_read_query(db, query)
    data = {}
    for entry in entries:
        key = f"{entry[1]}-{entry[2]}"
        data[key] = list(entry)

    return data

def month_exists(db: sqlite3.Connection, year: int, month: int) -> bool:
    query = f"""
    SELECT * from monthly where year = {year} and month = {month};
    """
    entries = execute_read_query(db, query)
    if entries:
        return True
    else:
        return False

if __name__ == '__main__':
    if len(sys.argv) < 2:
        print("You need to specify config gile as an argument.")
        exit(-1)

    settings = importlib.import_module(sys.argv[1])
    db = create_connection(settings.DB_FILE)
    #create_monthly_table(db)

    # Just testing
    monthly = build_monthly_dict(db)
    print(monthly)


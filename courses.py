import datetime

from database import Database
from collector import api_request

def create_course_table(db: Database) -> None:
    query = """
    CREATE TABLE IF NOT EXISTS course(
        id INTEGER PRIMARY KEY,
        code CHAR(20),
        name VARCHAR,
        instance CHAR(20),
        start_time DATETIME,
        end_time DATETIME
    );
    """
    db.write_query(query)


def course_exists(db: Database, id: int) -> bool:
    query = f"""
    SELECT * from course where id = {id};
    """
    entries = db.read_query(query)
    if entries:
        return True
    else:
        return False


def insert_course(db: Database, course: dict) -> None:
    name = course['name'].replace("'", "''")
    instance = course['instance_name'].replace("'", "''")
    query = f"""
    INSERT INTO
        course (id, code, name, instance, start_time, end_time)
    VALUES
        ({course['id']}, '{course['code']}', '{name}', '{instance}', '{course['starting_time']}', '{course['ending_time']}');
    """
    db.write_query(query)


def get_courses(db: Database) -> None:
    from main import settings
    
    url = f"{settings.BASE_URL}/api/v2/courses/"
    repeat = True
    while repeat:
        json = api_request(url)
        url = json['next']
    
        for result in json['results']:
            if not course_exists(db, result['id']):
                courseurl = f"{settings.BASE_URL}/api/v2/courses/{result['id']}"
                course = api_request(courseurl)
                insert_course(db, course)
                print(f"Inserted course: {course['id']}, {course['code']}, {course['instance_name']}")
        if not url: repeat = False


def get_courses_between(db: Database, start: datetime.date, end: datetime.date) -> list:
    query = f"""
    SELECT id from course where not (start_time > '{end}' or end_time < '{start}');
    """
    print(f"query: {query}")
    entries = db.read_query(query)
    return entries


def get_coursecode_by_id(db: Database, id: int) -> str:
    query = f"""
    SELECT code from course where id = {id};
    """
    entries = db.read_query(query)
    return entries[0][0]

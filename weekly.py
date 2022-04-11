import datetime
from dateutil.relativedelta import relativedelta

from database import Database
from courses import get_courses_between
from collector import stats_course_api_request

def create_weekly_courses_table(db: Database) -> None:
    query = """
    CREATE TABLE IF NOT EXISTS weekly_courses(
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        course INTEGER NOT NULL,
        year INTEGER NOT NULL,
        week INTEGER NOT NULL,
        submission_count INTEGER,
        submitters INTEGER,
        FOREIGN KEY (course) REFERENCES course(id)
    );
    """
    db.write_query(query)


def week_exists(db: Database, date: datetime.date, course: int) -> bool:
    query = f"""
    SELECT * from weekly_courses where year = {date.isocalendar()[0]} and week = {date.isocalendar()[1]} and course = {course};
    """
    entries = db.read_query(query)
    if entries:
        return True
    else:
        return False


def build_weekly_dict(db: Database, start: datetime.date, end: datetime.date) -> dict:
    query = f"""
    SELECT * from weekly_courses where
        year >= {start.isocalendar()[0]} and
        week >= {start.isocalendar()[1]} and
        year <= {end.isocalendar()[0]} and
        week <= {end.isocalendar()[1]}
        order by year,week;
    """
    entries = db.read_query(query)
    courses = dict()
    for entry in entries:
        key = f"{entry[2]}-{entry[3]}"
        if key not in courses:
            courses[key] = dict()

        courses[key][entry[1]] = (entry[4], entry[5])

    return courses


def insert_weekly_entry(
        db: Database,
        course: int,
        date: datetime.date,
        submission_count: int,
        submitters: int,
        ) -> None:
    query = f"""
    INSERT INTO
        weekly_courses (course, year, week, submission_count, submitters)
    VALUES
        ({course}, {date.isocalendar()[0]}, {date.isocalendar()[1]}, {submission_count}, {submitters});
    """
    db.write_query(query)


def get_week(db: Database, start: datetime.date, course: int) -> None:
    if week_exists(db, start, course):
        return

    enddate = start + relativedelta(days=7)
    json = stats_course_api_request(course, start, enddate)
    insert_weekly_entry(db, course, start, json['submission_count'], json['submitters'])
    print(f"Week {start}, course {course} inserted")


def collect_weekly(db: Database, date: datetime.date, enddate: datetime.date) -> None:
    from main import settings

    while date <= enddate:
        end = date + relativedelta(days=7)
        courses = get_courses_between(db, date, end)
        for course in courses:
            get_week(db, date, course[0])

        date = end

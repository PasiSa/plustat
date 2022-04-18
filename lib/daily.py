import datetime
from dateutil.relativedelta import relativedelta

from lib.database import Database
from lib.collector import stats_api_request, stats_course_api_request
from lib.settings import settings


# FIXME: should use datetime instead of three separate integers for date
def create_daily_table(db: Database) -> None:
    query = """
    CREATE TABLE IF NOT EXISTS daily(
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        year INTEGER NOT NULL,
        month INTEGER NOT NULL,
        day INTEGER NOT NULL,
        submission_count INTEGER,
        submitters INTEGER
    );
    """
    db.write_query(query)


def create_daily_courses_table(db: Database) -> None:
    query = """
    CREATE TABLE IF NOT EXISTS daily_courses(
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        course INTEGER NOT NULL,
        date DATE,
        submission_count INTEGER,
        submitters INTEGER,
        FOREIGN KEY (course) REFERENCES course(id)
    );
    """
    db.write_query(query)


def insert_daily_entry(
    db: Database,
    date: datetime.date,
    submission_count: int,
    submitters: int,
) -> None:
    query = f"""
    INSERT INTO
        daily (year, month, day, submission_count, submitters)
    VALUES
        ({date.year}, {date.month}, {date.day}, {submission_count}, {submitters});
    """
    db.write_query(query)


def insert_daily_course_entry(
    db: Database,
    course: int,
    date: datetime.date,
    submission_count: int,
    submitters: int,
) -> None:
    query = f"""
    INSERT INTO
        daily_courses (course, date, submission_count, submitters)
    VALUES
        ({course}, '{date}', {submission_count}, {submitters});
    """
    db.write_query(query)


def build_daily_dict(db: Database, date: datetime.date) -> dict:
    query = f"""
    SELECT * from daily where year={date.year} and month={date.month} order by year,month,day;
    """
    entries = db.read_query(query)
    data = {}
    for entry in entries:
        key = f"{entry[1]}-{entry[2]-entry[3]}"
        data[key] = list(entry)

    return data


def build_daily_courses_dict(db: Database, start: datetime.date, end: datetime.date) -> dict:
    query = f"""
    SELECT * from daily_courses where date>='{start}' and date<='{end}' order by date;
    """
    entries = db.read_query(query)
    courses = dict()
    for entry in entries:
        key = f"{entry[2]}"
        if key not in courses:
            courses[key] = dict()

        courses[key][entry[1]] = (entry[3], entry[4])

    return courses


def day_exists(db: Database, date: datetime.date) -> bool:
    query = f"""
    SELECT * from daily where year = {date.year} and month = {date.month} and day = {date.day};
    """
    entries = db.read_query(query)
    if entries:
        return True
    else:
        return False


def day_course_exists(db: Database, date: datetime.date, course: int) -> bool:
    query = f"""
    SELECT * from daily_courses where date='{date}' and course={course};
    """
    entries = db.read_query(query)
    if entries:
        return True
    else:
        return False


def get_day(db: Database, date: datetime.date) -> None:
    if day_exists(db, date):
        return

    enddate = date + relativedelta(days=1)
    json = stats_api_request(date, enddate)
    insert_daily_entry(db, date, json['submission_count'], json['submitters'])
    print(f"Day {date} inserted")


def get_day_courses(db: Database, date: datetime.date, course: int) -> None:
    if day_course_exists(db, date, course):
        return

    enddate = date + relativedelta(days=1)
    json = stats_course_api_request(course, date, enddate)
    insert_daily_course_entry(db, course, date, json['submission_count'], json['submitters'])
    print(f"Day {date}, course {course} inserted")


def collect_daily(db: Database) -> None:
    date = datetime.date(settings.DAILY_START[0], settings.DAILY_START[1], 1)
    enddate = datetime.date(settings.DAILY_END[0], settings.DAILY_END[1], 1)
    while date <= enddate:
        get_day(db, date)
        date = date + relativedelta(days=1)

from lib.database import Database
import datetime
from dateutil.relativedelta import relativedelta

from lib.collector import stats_course_api_request_hourly
from lib.courses import count_totals, make_datalist, draw_courses
from lib.settings import settings


def create_hourly_courses_table(db: Database) -> None:
    query = """
    CREATE TABLE IF NOT EXISTS hourly_courses(
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        course INTEGER NOT NULL,
        time DATETIME,
        submission_count INTEGER,
        submitters INTEGER,
        FOREIGN KEY (course) REFERENCES course(id)
    );
    """
    db.write_query(query)


def insert_hourly_course_entry(
    db: Database,
    course: int,
    time: datetime.datetime,
    submission_count: int,
    submitters: int,
) -> None:
    query = f"""
    INSERT INTO
        hourly_courses (course, time, submission_count, submitters)
    VALUES
        ({course}, '{time}', {submission_count}, {submitters});
    """
    db.write_query(query)


def hourly_course_exists(db: Database, time: datetime.datetime, course: int) -> bool:
    query = f"""
    SELECT * from hourly_courses where time='{time}' and course={course};
    """
    entries = db.read_query(query)
    if entries:
        return True
    else:
        return False


def get_hourly_courses(db: Database, time: datetime.datetime, course: int) -> None:
    if hourly_course_exists(db, time, course):
        return

    enddate = time + relativedelta(hours=1)
    json = stats_course_api_request_hourly(course, time, enddate)
    insert_hourly_course_entry(db, course, time, json['submission_count'], json['submitters'])
    print(f"Time {time}, course {course} inserted")


# TODO: this is redundant with daily variant. Consider common implementation
def build_hourly_courses_dict(db: Database, start: datetime.datetime, end: datetime.datetime) -> dict:
    query = f"""
    SELECT * from hourly_courses where time>='{start}' and time<='{end}' order by time;
    """
    entries = db.read_query(query)
    courses = dict()
    for entry in entries:
        key = f"{entry[2]}"
        if key not in courses:
            courses[key] = dict()

        courses[key][entry[1]] = (entry[3], entry[4])

    return courses


def draw_hourly_courses(
        db: Database,
        processed: dict,
        startdate: datetime.datetime,
        enddate: datetime.datetime,
        ylabel: str,
        filename: str,
        ) -> None:

    ticks = range(6 - (startdate.hour % 6), len(processed['other']), 6)
    xlabels = list()
    for hour in ticks:
        d = startdate + relativedelta(hours=hour)
        if d.hour == 0:
            xlabels.append(f"{d.day:02d}/{d.month:02d}")
        else:
            xlabels.append(f"{d.hour:02d}")
    draw_courses(db, processed, startdate, enddate, ylabel, ticks, xlabels, filename)


def produce_hourly_courses(db: Database, start: datetime.datetime, end: datetime.datetime) -> None:
    data = build_hourly_courses_dict(db, start, end)

    (totals, alltotal) = count_totals(data)

    sorted_total = sorted(totals.items(), key=lambda k: k[1][0], reverse=True )

    dataset = make_datalist(data, sorted_total, alltotal, 0)
    draw_hourly_courses(
        db,
        dataset,
        start,
        end,
        "submissions / hour",
        f"{settings.OUTPUT_DIR}/submissions-courses-hourly-latest.png",
    )

    dataset = make_datalist(data, sorted_total, alltotal, 1)
    draw_hourly_courses(
        db,
        dataset,
        start,
        end,
        "submitters / hour",
        f"{settings.OUTPUT_DIR}/submitters-courses-hourly-latest.png",
    )

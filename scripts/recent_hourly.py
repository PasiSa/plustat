import sys
import datetime
from dateutil.relativedelta import relativedelta

from lib.database import Database
from lib.courses import get_courses_between
from lib.hourly import get_hourly_courses, produce_hourly_courses
from lib.settings import settings


def collect_recent_hourly(db: Database, date: datetime.datetime, end: datetime.datetime) -> None:
    courses = get_courses_between(db, date, end)

    while date < end:
        for course in courses:
            get_hourly_courses(db, date, course[0])
        date = date + relativedelta(hours=1)


if __name__ == '__main__':
    print(f"--- Starting plustat/recent_hourly.py at {datetime.datetime.now()} ---")
    if len(sys.argv) < 2:
        print("You need to specify config file as an argument.")
        exit(-1)

    db = Database()
    end = datetime.datetime.today()
    end = end.replace(microsecond=0, second=0, minute=0)
    start = end - relativedelta(hours=settings.RECENT_HOURS)
    collect_recent_hourly(db, start, end)
    produce_hourly_courses(db, start, end)
    print(f"--- Ending plustat/recent_hourly.py at {datetime.datetime.now()} ---")

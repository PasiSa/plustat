import importlib
import sys
import datetime
from dateutil.relativedelta import relativedelta

from database import Database
from courses import get_courses, get_courses_between
from daily import get_day_courses
from graph_daily import produce_daily_courses

settings = importlib.import_module(sys.argv[1])


def collect_recent(db: Database, date: datetime.date, end: datetime.date) -> None:
    get_courses(db)
    courses = get_courses_between(db, date, end)

    while date < end:
        for course in courses:
            get_day_courses(db, date, course[0])
        date = date + relativedelta(days=1)


if __name__ == '__main__':
    print(f"--- Starting plustat/periodic.py at {datetime.datetime.now()} ---")
    if len(sys.argv) < 2:
        print("You need to specify config gile as an argument.")
        exit(-1)

    db = Database()
    end = datetime.date.today()
    start = end - relativedelta(days=settings.RECENT_DAYS)
    collect_recent(db, start, end)
    produce_daily_courses(db, start, end)
    print(f"--- Ending plustat/periodic.py at {datetime.datetime.now()} ---")

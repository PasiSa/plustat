import sys
import datetime
from dateutil.relativedelta import relativedelta

from lib.database import Database
from lib.courses import get_courses_between
from lib.daily import get_day_courses
from lib.graph_daily import produce_daily_courses
from lib.settings import settings


def collect_recent(db: Database, date: datetime.date, end: datetime.date) -> None:
    courses = get_courses_between(db, date, end)

    while date < end:
        for course in courses:
            get_day_courses(db, date, course[0])
        date = date + relativedelta(days=1)


if __name__ == '__main__':
    print(f"--- Starting plustat/recent_daily.py at {datetime.datetime.now()} ---")
    if len(sys.argv) < 2:
        print("You need to specify config gile as an argument.")
        exit(-1)

    db = Database()
    end = datetime.date.today()
    start = end - relativedelta(days=settings.RECENT_DAYS)
    collect_recent(db, start, end)
    produce_daily_courses(db, start, end)
    print(f"--- Ending plustat/recent_daily.py at {datetime.datetime.now()} ---")

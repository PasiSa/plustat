import importlib
import sys
import datetime

from lib.database import Database
from lib.monthly import collect_monthly
from lib.graph_monthly import build_monthly_dict, monthly_submissions, monthly_submitters

settings = importlib.import_module(sys.argv[1])


if __name__ == '__main__':
    print(f"--- Starting plustat/monthly.py at {datetime.datetime.now()} ---")
    if len(sys.argv) < 2:
        print("You need to specify config gile as an argument.")
        exit(-1)

    db = Database()
    today = datetime.date.today()
    if today.month == 1:
        end = datetime.date(today.year-1, 12, 1)
    else:
        end = datetime.date(today.year, today.month-1, 1)
    start = datetime.date(settings.MONTHLY_START[0], settings.MONTHLY_START[1], 1)

    collect_monthly(db, start, end)
    data = build_monthly_dict(db)
    monthly_submissions(data)
    monthly_submitters(data)

import importlib
import sys
import datetime
from dateutil.relativedelta import relativedelta

from lib.database import Database
from lib.graph_weekly import produce_weekly
from lib.weekly import collect_weekly

settings = importlib.import_module(sys.argv[1])


if __name__ == '__main__':
    print(f"--- Starting plustat/recent_weekly.py at {datetime.datetime.now()} ---")
    if len(sys.argv) < 2:
        print("You need to specify config gile as an argument.")
        exit(-1)

    # This works for now, until the end of spring 2022. Then needs updating after that :-)
    db = Database()
    current_year = datetime.date.today().isocalendar()[0]
    current_week = datetime.date.today().isocalendar()[1]
    if current_week > 22: current_week = 22  # Assume we are collecting spring term
    end = datetime.date.fromisocalendar(current_year, current_week-1, 1)
    start = datetime.date.fromisocalendar(current_year, 1, 1)
    collect_weekly(db, start, end)
    produce_weekly(db, start, end)
    print(f"--- Ending plustat/recent_weekly.py at {datetime.datetime.now()} ---")

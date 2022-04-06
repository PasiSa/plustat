import importlib
import sys

from database import Database
from daily import create_daily_table, collect_daily
from weekly import collect_weekly, create_weekly_courses_table
from graph_daily import draw_daily
from courses import create_course_table, get_courses


settings = importlib.import_module(sys.argv[1])


if __name__ == '__main__':
    if len(sys.argv) < 2:
        print("You need to specify config gile as an argument.")
        exit(-1)

    settings = importlib.import_module(sys.argv[1])
    db = Database()
    #create_daily_table(db)
    #create_course_table(db)
    #create_weekly_courses_table(db)

    if (settings.UPDATE_COURSES):
        get_courses(db)

    if (settings.DO_DAILY):
        collect_daily(db)
        draw_daily(db)

    if (settings.DO_WEEKLY):
        collect_weekly(db)

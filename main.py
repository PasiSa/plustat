import importlib
import sys
import datetime

from database import Database
from daily import create_daily_courses_table, create_daily_table, collect_daily
from weekly import collect_weekly, create_weekly_courses_table
from graph_daily import draw_daily
from graph_weekly import produce_weekly
from courses import create_course_table, get_courses


settings = importlib.import_module(sys.argv[1])


if __name__ == '__main__':
    if len(sys.argv) < 2:
        print("You need to specify config gile as an argument.")
        exit(-1)

    db = Database()
    #create_daily_table(db)
    #create_course_table(db)
    #create_weekly_courses_table(db)
    #create_daily_courses_table(db)

    if (settings.UPDATE_COURSES):
        get_courses(db)

    if (settings.DO_DAILY):
        collect_daily(db)
        draw_daily(db)

    if (settings.DO_WEEKLY):
        collect_weekly(db)
        produce_weekly(
            db,
            datetime.date.fromisocalendar(2021,1,1),
            datetime.date.fromisocalendar(2021,21,1)
        )
        produce_weekly(
            db,
            datetime.date.fromisocalendar(2021,34,1),
            datetime.date.fromisocalendar(2021,52,1)
        )
        produce_weekly(
            db,
            datetime.date.fromisocalendar(2022,1,1),
            datetime.date.fromisocalendar(2022,13,1)
        )

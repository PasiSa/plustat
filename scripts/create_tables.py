import sys

from lib.database import Database
from lib.daily import create_daily_courses_table, create_daily_table
from lib.weekly import create_weekly_courses_table
from lib.courses import create_course_table
from lib.hourly import create_hourly_courses_table


if __name__ == '__main__':
    if len(sys.argv) < 2:
        print("You need to specify config gile as an argument.")
        exit(-1)

    db = Database()

    create_daily_table(db)
    create_course_table(db)
    create_weekly_courses_table(db)
    create_daily_courses_table(db)
    create_hourly_courses_table(db)

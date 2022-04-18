import sys
import datetime

from lib.database import Database
from lib.courses import get_courses


if __name__ == '__main__':
    print(f"--- Starting plustat/update_courses.py at {datetime.datetime.now()} ---")
    if len(sys.argv) < 2:
        print("You need to specify config gile as an argument.")
        exit(-1)

    db = Database()
    get_courses(db)
    print(f"--- Ending plustat/update_courses.py at {datetime.datetime.now()} ---")

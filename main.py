import importlib
import sys

from database import Database
from daily import create_daily_table, collect_daily
from graph_daily import draw_daily


settings = importlib.import_module(sys.argv[1])


if __name__ == '__main__':
    if len(sys.argv) < 2:
        print("You need to specify config gile as an argument.")
        exit(-1)

    settings = importlib.import_module(sys.argv[1])
    db = Database()
    #create_daily_table(db)

    if (settings.DO_DAILY):
        #collect_daily(db)
        draw_daily(db)

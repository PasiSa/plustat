import requests
import datetime
import sqlite3
import importlib
import sys
from dateutil.relativedelta import relativedelta

from database import create_connection, insert_monthly_entry, month_exists

settings = None

def get_month(db: sqlite3.Connection, year: int, month: int) -> None:
    if month_exists(db, year, month):
        print(f"Month {year}/{month} already exists")
        return

    date = datetime.date(year, month, 1)
    enddate = date + relativedelta(months=1)

    url = f"{settings.BASE_URL}/api/v2/statistics/?starttime={year}-{month:02d}-01T00:00&endtime={enddate.year}-{enddate.month:02d}-01T00:00"
    print(f"Requested: {url}")
    headers = {"Authorization":f"Token {settings.AUTH_TOKEN}"}
    querystart = datetime.datetime.now()
    response = requests.get(url, headers=headers)
    queryend = datetime.datetime.now()
    response.raise_for_status()
    json = response.json()
    print(f"response ({queryend - querystart}): {json}")

    insert_monthly_entry(db, year, month, json['submission_count'], json['submitters'])
    print(f"Month {year}/{month} inserted")


def do_monthly(db: sqlite3.Connection):
    date = datetime.date(settings.MONTHLY_START[0], settings.MONTHLY_START[1], 1)
    enddate = datetime.date(settings.MONTHLY_END[0], settings.MONTHLY_END[1], 1)
    while date <= enddate:
        get_month(db, date.year, date.month)
        date = date + relativedelta(months=1)

if __name__ == '__main__':
    if len(sys.argv) < 2:
        print("You need to specify config gile as an argument.")
        exit(-1)

    settings = importlib.import_module(sys.argv[1])
    db = create_connection(settings.DB_FILE)
    #get_month(db, 2022, 1)
    do_monthly(db)

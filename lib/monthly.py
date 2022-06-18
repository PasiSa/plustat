import importlib
import sys
import datetime
from dateutil.relativedelta import relativedelta

from lib.database import Database
from lib.collector import stats_api_request


def create_monthly_table(db: Database) -> None:
    query = """
    CREATE TABLE IF NOT EXISTS monthly(
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        year INTEGER NOT NULL,
        month INTEGER NOT NULL,
        submission_count INTEGER,
        submitters INTEGER
    );
    """
    db.write_query(query)


def insert_monthly_entry(
    db: Database,
    year: int,
    month: int,
    submission_count: int,
    submitters: int,
) -> None:
    query = f"""
    INSERT INTO
        monthly (year, month, submission_count, submitters)
    VALUES
        ({year}, {month}, {submission_count}, {submitters});
    """
    db.write_query(query)


def build_monthly_dict(db: Database) -> dict:
    query = """
    SELECT * from monthly order by year,month;
    """
    entries = db.read_query(query)
    data = {}
    for entry in entries:
        key = f"{entry[1]}-{entry[2]}"
        data[key] = list(entry)

    return data


def month_exists(db: Database, year: int, month: int) -> bool:
    query = f"""
    SELECT * from monthly where year = {year} and month = {month};
    """
    entries = db.read_query(query)
    if entries:
        return True
    else:
        return False


def get_month(db: Database, year: int, month: int) -> None:
    if month_exists(db, year, month):
        #print(f"Month {year}/{month} already exists")
        return

    startdate = datetime.date(year, month, 1)
    enddate = startdate + relativedelta(months=1)

    json = stats_api_request(startdate, enddate)

    insert_monthly_entry(db, year, month, json['submission_count'], json['submitters'])
    print(f"Month {year}/{month} inserted")


def collect_monthly(db: Database, date: datetime.date, enddate: datetime.date) -> None:
    while date <= enddate:
        get_month(db, date.year, date.month)
        date = date + relativedelta(months=1)


if __name__ == '__main__':
    if len(sys.argv) < 2:
        print("You need to specify config gile as an argument.")
        exit(-1)

    settings = importlib.import_module(sys.argv[1])
    db = Database()
    #create_monthly_table(db)

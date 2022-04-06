import datetime
from dateutil.relativedelta import relativedelta

from database import Database
from collector import stats_api_request

def create_daily_table(db: Database) -> None:
    query = """
    CREATE TABLE IF NOT EXISTS daily(
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        year INTEGER NOT NULL,
        month INTEGER NOT NULL,
        day INTEGER NOT NULL,
        submission_count INTEGER,
        submitters INTEGER
    );
    """
    db.write_query(query)


def insert_daily_entry(
    db: Database,
    date: datetime.date,
    submission_count: int,
    submitters: int,
) -> None:
    query = f"""
    INSERT INTO
        daily (year, month, day, submission_count, submitters)
    VALUES
        ({date.year}, {date.month}, {date.day}, {submission_count}, {submitters});
    """
    db.write_query(query)


def build_daily_dict(db: Database, date: datetime.date) -> dict:
    query = f"""
    SELECT * from daily where year={date.year} and month={date.month} order by year,month,day;
    """
    entries = db.read_query(query)
    data = {}
    for entry in entries:
        key = f"{entry[1]}-{entry[2]-entry[3]}"
        data[key] = list(entry)

    return data


def day_exists(db: Database, date: datetime.date) -> bool:
    query = f"""
    SELECT * from daily where year = {date.year} and month = {date.month} and day = {date.day};
    """
    entries = db.read_query(query)
    if entries:
        return True
    else:
        return False


def get_day(db: Database, date: datetime.date) -> None:
    if day_exists(db, date):
        #print(f"Day {date} already exists")
        return

    enddate = date + relativedelta(days=1)
    json = stats_api_request(date, enddate)
    insert_daily_entry(db, date, json['submission_count'], json['submitters'])
    print(f"Day {date} inserted")


def collect_daily(db: Database) -> None:
    from main import settings

    date = datetime.date(settings.DAILY_START[0], settings.DAILY_START[1], 1)
    enddate = datetime.date(settings.DAILY_END[0], settings.DAILY_END[1], 1)
    while date <= enddate:
        get_day(db, date)
        date = date + relativedelta(days=1)

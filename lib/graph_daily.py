import datetime
from dateutil.relativedelta import relativedelta

import matplotlib.pyplot as plt
import numpy as np

from lib.database import Database
from lib.daily import build_daily_dict, build_daily_courses_dict
from lib.courses import count_totals, draw_courses, make_datalist
from lib.settings import settings


def daily_common(
        ydata: list,
        startdate: datetime.date,
        tickinterval: int,
        ylabel: str,
        filename: str
        ):
    x = 0.5 + np.arange(len(ydata))
    mondays = range((7 - startdate.weekday()), len(ydata), 7)
    yticks = range(0, max(ydata), tickinterval)
    fig, ax = plt.subplots(figsize=(12,6))
    ax.bar(x, ydata, width=1, edgecolor="white", linewidth=0.7)
    ax.set(
        xlim=(0, len(ydata)), xticks=mondays,
        ylim=(0, max(ydata)), yticks=yticks,
    )
    xlabels = list(map(lambda a: str(a+1), mondays))
    ax.set_xticklabels(xlabels)

    for a in mondays:
        ax.axvline(x=a, color='lightgray', linestyle='--')

    for a in range(tickinterval, max(ydata), tickinterval):
        ax.axhline(y=a, color='lightgray', linestyle=':')

    ax.set_ylabel(ylabel)
    plt.savefig(filename)


def daily_submissions(data: dict, startdate: datetime.date):
    #from main import settings
    y = []
    for key in data:
        y.append(data[key][4])

    daily_common(
        y,
        startdate,
        1000,
        'submissions / day',
        f"{settings.OUTPUT_DIR}/submissions-{startdate.year}-{startdate.month:02d}.png",
    )


def daily_submitters(data: dict, startdate: datetime.date):
    #from main import settings
    y = []
    for key in data:
        y.append(data[key][5])
    
    daily_common(
        y,
        startdate,
        200,
        'submitters / day',
        f"{settings.OUTPUT_DIR}/submitters-{startdate.year}-{startdate.month:02d}.png",
    )


def draw_daily(db: Database):
    date = datetime.date(settings.DAILY_START[0], settings.DAILY_START[1], 1)
    enddate = datetime.date(settings.DAILY_END[0], settings.DAILY_END[1], 1)
    while (date <= enddate):
        data = build_daily_dict(db, date)
        daily_submissions(data, date)
        daily_submitters(data, date)
        #daily_submissions_submitters(data)
        date = date + relativedelta(months=1)


def draw_daily_courses(
        db: Database,
        processed: dict,
        startdate: datetime.date,
        enddate: datetime.date,
        ylabel: str,
        filename: str,
        ) -> None:

    mondays = range((7 - startdate.weekday()), len(processed['other']), 7)
    xlabels = list()
    for day in mondays:
        d = startdate + relativedelta(days=day)
        xlabels.append(f"{d.day:02d}/{d.month:02d}")
    draw_courses(db, processed, startdate, enddate, ylabel, mondays, xlabels, filename)


def produce_daily_courses(db: Database, start: datetime.date, end: datetime.date) -> None:
    data = build_daily_courses_dict(db, start, end)

    (totals, alltotal) = count_totals(data)

    sorted_total = sorted(totals.items(), key=lambda k: k[1][0], reverse=True )

    dataset = make_datalist(data, sorted_total, alltotal, 0)
    draw_daily_courses(
        db,
        dataset,
        start,
        end,
        "submissions / day",
        f"{settings.OUTPUT_DIR}/submissions-courses-daily-latest.png",
    )

    dataset = make_datalist(data, sorted_total, alltotal, 1)
    draw_daily_courses(
        db,
        dataset,
        start,
        end,
        "submitters / day",
        f"{settings.OUTPUT_DIR}/submitters-courses-daily-latest.png",
    )
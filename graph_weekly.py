import datetime
from dateutil.relativedelta import relativedelta

import matplotlib.pyplot as plt
import numpy as np

from database import Database
from weekly import build_weekly_dict
from courses import get_coursecode_by_id


def draw_weekly(
        db: Database,
        processed: dict,
        startdate: datetime.date,
        enddate: datetime.date,
        ylabel: str,
        filename: str,
        ) -> None:

    x = 0.5 + np.arange(len(processed['other']))
    startweek = startdate.isocalendar()[1]
    xticks = range(0, len(processed['other']), 2)
    fig, ax = plt.subplots(figsize=(12,6))
    bars = [0] * len(processed['other'])
    for i in processed:
        if i != 'other':
            code = get_coursecode_by_id(db, i)
        else:
            code = 'other'
        ax.bar(x, processed[i], width=1, bottom=bars, label=code, edgecolor="white", linewidth=0.7)
        bars = np.add(bars, processed[i]).tolist()
    ax.set(
        xlim=(0, len(processed['other'])), xticks=xticks,
    )
    
    d = startdate
    labels = list()
    while d <= enddate:
        labels.append(f"{d.day:02d}/{d.month:02d}")
        d = d + relativedelta(days=14)
    ax.set_xticklabels(labels)
    ax.legend()
    ax.set_ylabel(ylabel)
    plt.savefig(filename)


def make_datalist(data: dict, sorted_total: dict, alltotal: dict, idx: int) -> dict:
    processed = dict()
    for key in data:
        sa = alltotal[key][idx]
        for i in range(0,5):
            if sorted_total[i][0] not in processed:
                processed[sorted_total[i][0]] = list()

            if sorted_total[i][0] in data[key]:
                processed[sorted_total[i][0]].append(data[key][sorted_total[i][0]][idx])
                sa -= data[key][sorted_total[i][0]][idx]
            else:
                processed[sorted_total[i][0]].append(0)

        if 'other' not in processed:
            processed['other'] = list()
        processed['other'].append(sa)
    return processed


def produce_weekly(db: Database, start: datetime.date, end: datetime.date) -> None:
    from main import settings

    data = build_weekly_dict(db, start, end)

    totals = dict()
    alltotal = dict()
    for key in data:  # key = week id
        week = data[key]
        alltotal[key] = (0,0)
        for i in week:  # i = course id
            if i in totals:
                a = totals[i][0] + week[i][0]  # submissions
                b = totals[i][1] + week[i][1]  # submitters
            else:
                a = week[i][0]
                b = week[i][1]
            totals[i] = (a,b)
            ta = alltotal[key][0] + week[i][0]
            tb = alltotal[key][1] + week[i][1]
            alltotal[key] = (ta, tb)

    sorted_total = sorted(totals.items(), key=lambda k: k[1][0], reverse=True )

    dataset = make_datalist(data, sorted_total, alltotal, 0)
    draw_weekly(
        db,
        dataset,
        start,
        end,
        "submissions / week",
        f"{settings.OUTPUT_DIR}/submissions-courses-weekly-{start.year}-{start.month:02d}.png",
    )

    dataset = make_datalist(data, sorted_total, alltotal, 1)
    draw_weekly(
        db,
        dataset,
        start,
        end,
        "submitters / week",
        f"{settings.OUTPUT_DIR}/submitters-courses-weekly-{start.year}-{start.month:02d}.png",
    )

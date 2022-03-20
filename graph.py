import importlib
import sys

import matplotlib.pyplot as plt
import numpy as np

from database import create_connection, build_monthly_dict


def monthly_common(ydata, tickinterval, hlines, ylabel, filename):
    x = 0.5 + np.arange(len(ydata))
    xticks = range(0, len(ydata), 12)
    yticks = range(0, max(ydata), tickinterval)
    fig, ax = plt.subplots(figsize=(12,6))
    ax.bar(x, ydata, width=1, edgecolor="white", linewidth=0.7)
    ax.set(
        xlim=(0, len(ydata)+1), xticks=xticks,
        ylim=(0, max(ydata)), yticks=yticks,
    )
    xx = list(range(2013, 2013 + len(xticks)))
    xlabels = list(map(lambda a: str(a), xx))
    ax.set_xticklabels(xlabels)
    for a in xticks:
        ax.axvline(x=a, color='lightgray', linestyle='--')

    #yy = list(range(100000, 300000, 100000))
    for a in hlines:
        ax.axhline(y=a, color='lightgray', linestyle=':')

    ax.set_ylabel(ylabel)
    plt.savefig(filename)


def monthly_submissions(data):
    y = []
    for key in data:
        y.append(data[key][3])

    monthly_common(
        y,
        20000,
        list(range(100000, 300000, 100000)),
        'submissions / month',
        'submissons.png',
    )


def monthly_submitters(data):
    y = []
    for key in data:
        y.append(data[key][4])
    
    monthly_common(
        y,
        200,
        list(range(1000, 4000, 1000)),
        'submitters / month',
        'submitters.png',
    )


def monthly_submissions_submitters(data):
    y = []
    for key in data:
        y.append(int(data[key][3]/data[key][4]))
    
    monthly_common(
        y,
        20,
        list(range(40, 160, 40)),
        'submissions / submitter',
        'submissions-submitters.png',
    )


if __name__ == '__main__':
    if len(sys.argv) < 2:
        print("You need to specify config gile as an argument.")
        exit(-1)

    settings = importlib.import_module(sys.argv[1])
    db = create_connection(settings.DB_FILE)
    data = build_monthly_dict(db)
    monthly_submissions(data)
    monthly_submitters(data)
    monthly_submissions_submitters(data)

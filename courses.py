import datetime

import matplotlib.pyplot as plt
import numpy as np

from database import Database
from collector import api_request

def create_course_table(db: Database) -> None:
    query = """
    CREATE TABLE IF NOT EXISTS course(
        id INTEGER PRIMARY KEY,
        code CHAR(20),
        name VARCHAR,
        instance CHAR(20),
        start_time DATETIME,
        end_time DATETIME
    );
    """
    db.write_query(query)


def course_exists(db: Database, id: int) -> bool:
    query = f"""
    SELECT * from course where id = {id};
    """
    entries = db.read_query(query)
    if entries:
        return True
    else:
        return False


def insert_course(db: Database, course: dict) -> None:
    name = course['name'].replace("'", "''")
    instance = course['instance_name'].replace("'", "''")
    query = f"""
    INSERT INTO
        course (id, code, name, instance, start_time, end_time)
    VALUES
        ({course['id']}, '{course['code']}', '{name}', '{instance}', '{course['starting_time']}', '{course['ending_time']}');
    """
    db.write_query(query)


def get_courses(db: Database) -> None:
    from main import settings
    
    url = f"{settings.BASE_URL}/api/v2/courses/"
    repeat = True
    while repeat:
        json = api_request(url)
        url = json['next']
    
        for result in json['results']:
            if not course_exists(db, result['id']):
                courseurl = f"{settings.BASE_URL}/api/v2/courses/{result['id']}"
                course = api_request(courseurl)
                insert_course(db, course)
                print(f"Inserted course: {course['id']}, {course['code']}, {course['instance_name']}")
        if not url: repeat = False


def get_courses_between(db: Database, start: datetime.date, end: datetime.date) -> list:
    query = f"""
    SELECT id from course where not (start_time > '{end}' or end_time < '{start}');
    """
    entries = db.read_query(query)
    return entries


def get_coursecode_by_id(db: Database, id: int) -> str:
    query = f"""
    SELECT code from course where id = {id};
    """
    entries = db.read_query(query)
    return entries[0][0]


def count_totals(data: dict):
    totals = dict()
    alltotal = dict()
    for key in data:  # key = date id
        date = data[key]
        alltotal[key] = (0,0)
        for i in date:  # i = course id
            if i in totals:
                a = totals[i][0] + date[i][0]  # submissions
                b = totals[i][1] + date[i][1]  # submitters
            else:
                a = date[i][0]
                b = date[i][1]
            totals[i] = (a,b)
            ta = alltotal[key][0] + date[i][0]
            tb = alltotal[key][1] + date[i][1]
            alltotal[key] = (ta, tb)

    return (totals, alltotal)


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


def draw_courses(
        db: Database,
        processed: dict,
        startdate: datetime.date,
        enddate: datetime.date,
        ylabel: str,
        xticks: list,
        xticklabels: list,
        filename: str,
        ) -> None:

    x = 0.5 + np.arange(len(processed['other']))
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
    
    ax.set_xticklabels(xticklabels)
    ax.legend()
    ax.set_ylabel(ylabel)
    plt.savefig(filename)
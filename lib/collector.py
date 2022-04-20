import requests
import datetime

from lib.settings import settings


def api_request(url: str) -> dict:
    print(f"Requested: {url}")
    headers = {"Authorization":f"Token {settings.AUTH_TOKEN}"}
    querystart = datetime.datetime.now()
    response = requests.get(url, headers=headers)
    queryend = datetime.datetime.now()
    response.raise_for_status()
    json = response.json()
    print(f"response in ({queryend - querystart})")
    return json


def stats_api_request(startdate: datetime.date, enddate: datetime.date) -> dict:
    url = f"{settings.BASE_URL}/api/v2/statistics/?starttime={startdate.year}-{startdate.month:02d}-{startdate.day:02d}T00:00&endtime={enddate.year}-{enddate.month:02d}-{enddate.day:02d}T00:00"
    return api_request(url)


def stats_course_api_request(
        course: int,
        startdate: datetime.date,
        enddate: datetime.date
        ) -> dict:

    url = f"{settings.BASE_URL}/api/v2/courses/{course}/statistics/?starttime={startdate.year}-{startdate.month:02d}-{startdate.day:02d}T00:00&endtime={enddate.year}-{enddate.month:02d}-{enddate.day:02d}T00:00"
    return api_request(url)


# FIXME: this and above should be combined
def stats_course_api_request_hourly(
        course: int,
        startdate: datetime.datetime,
        enddate: datetime.datetime
        ) -> dict:

    url = f"{settings.BASE_URL}/api/v2/courses/{course}/statistics/?starttime={startdate.year}-{startdate.month:02d}-{startdate.day:02d}T{startdate.hour:02d}:00&endtime={enddate.year}-{enddate.month:02d}-{enddate.day:02d}T{enddate.hour:02d}:00"
    return api_request(url)

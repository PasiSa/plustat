import requests
import datetime


def api_request(url: str) -> dict:
    from main import settings
    
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
    from main import settings
    
    url = f"{settings.BASE_URL}/api/v2/statistics/?starttime={startdate.year}-{startdate.month:02d}-{startdate.day:02d}T00:00&endtime={enddate.year}-{enddate.month:02d}-{enddate.day:02d}T00:00"
    return api_request(url)


def stats_course_api_request(
        course: int,
        startdate: datetime.date,
        enddate: datetime.date
        ) -> dict:

    from main import settings
    
    url = f"{settings.BASE_URL}/api/v2/courses/{course}/statistics/?starttime={startdate.year}-{startdate.month:02d}-{startdate.day:02d}T00:00&endtime={enddate.year}-{enddate.month:02d}-{enddate.day:02d}T00:00"
    return api_request(url)

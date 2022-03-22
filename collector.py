import requests
import datetime


def api_request(startdate: datetime.date, enddate: datetime.date) -> dict:
    from main import settings
    
    url = f"{settings.BASE_URL}/api/v2/statistics/?starttime={startdate.year}-{startdate.month:02d}-{startdate.day:02d}T00:00&endtime={enddate.year}-{enddate.month:02d}-{enddate.day:02d}T00:00"
    print(f"Requested: {url}")
    headers = {"Authorization":f"Token {settings.AUTH_TOKEN}"}
    querystart = datetime.datetime.now()
    response = requests.get(url, headers=headers)
    queryend = datetime.datetime.now()
    response.raise_for_status()
    json = response.json()
    print(f"response ({queryend - querystart}): {json}")
    return json

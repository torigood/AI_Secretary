import requests
import os
from dotenv import load_dotenv

load_dotenv()

username = os.getenv("USERNAME")


def geonames_lookup(city_name, username=username):
    url = "http://api.geonames.org/searchJSON"
    params = {
        "q": city_name,
        "maxRows": 1,
        "lang": "ko",
        "username": username
    }
    response = requests.get(url, params=params)
    
    try:
        data = response.json()
    except Exception as e:
        print("응답 JSON 파싱 실패:", e)
        return None

    if "geonames" in data and data["geonames"]:
        return data["geonames"][0]["name"]
    else:
        print("GeoNames 응답 문제:", data)
        return None

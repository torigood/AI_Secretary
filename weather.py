import os
from dotenv import load_dotenv

load_dotenv()

import requests
from translator import translate_to_korean
from city_list import city_list, en_city_list
import datetime


#   한글 도시명 추출을 위한 리스트 기반
def extract_city_with_list(command):
    for city in city_list:
        if city in command:
            return city
    return None
#    한글 도시명 추출을 위한 키워드 제거
def extract_city_from_command(command):
    command = command.strip()
    keywords = ["날씨", "알려줘", "어디", "의", "는", "좀", "보여줘", "어때", "기온", "정보"]
    for word in keywords:
        command = command.replace(word, "")
    return command.strip()


def extract_city(command):
    # 1단계: 한글 도시 추출 시도 (정확도 높은 리스트 기반)
    city_ko = extract_city_with_list(command)
    if not city_ko:
        # 2단계: 키워드 제거 방식으로 한글 도시 추출 시도
        city_ko = extract_city_from_command(command)

    # 3단계: 한글 도시명을 영어로 매핑
    if city_ko in city_list:
        return city_list[city_ko]
    
    # 4단계:
    # city_en = geonames_lookup(city_ko)
    # if city_en:
    #     return city_en
    
    
    # 5단계: 못 찾으면 None
    return None


def get_weather(city):
    api_key = os.getenv("WEATHER_API_KEY")
    url = f"http://api.weatherapi.com/v1/current.json?key={api_key}&q={city}&aqi=yes&lang=en"
    response = requests.get(url)

    if response.status_code != 200:
        return "날씨 정보를 가져오는 데 실패했습니다."

    try:
        data = response.json()
    except Exception as e:
        return f"JSON 파싱 오류: {e}"

    location = data['location']['name']
    location_korean = translate_to_korean(location)

    country = data['location']['country']
    country_korean = translate_to_korean(country)

    temp_c = data['current']['temp_c']
    condition = data['current']['condition']['text']
    condition_korean = translate_to_korean(condition)
    humidity = data['current']['humidity']
    wind_kph = data['current']['wind_kph']

    return (f"{country_korean}, {location_korean}의 온도는 {temp_c}°C입니다.\n"
            f"날씨는 {condition_korean}이며, 습도는 {humidity}%이며 바람은 {wind_kph}km/h입니다.")
    


def get_forecast(city):
    api_key = os.getenv("WEATHER_API_KEY")
    url = f"http://api.weatherapi.com/v1/forecast.json?key={api_key}&q={city}&days=7&aqi=no&alerts=no&lang=en"
    response = requests.get(url)

    if response.status_code != 200:
        return "날씨 정보를 가져오는 데 실패했습니다."

    try:
        data = response.json()
        forecast_days = data['forecast']['forecastday']
    except Exception as e:
        return f"JSON 파싱 오류: {e}"

    results = []

    for day in forecast_days:
        date = day['date']
        condition = day['day']['condition']['text']
        condition_kor = translate_condition_to_korean(condition)
        emoji = get_weather_emoji(condition)
        weekday = get_weekday_korean(date)
        max_temp = day['day']['maxtemp_c']
        min_temp = day['day']['mintemp_c']
        results.append(f"{date} ({weekday}) | {emoji} {condition_kor} | 최고: {max_temp}°C / 최저: {min_temp}°C")

    return results


def generate_weather_notice(forecast: list[str]) -> list[str]:
    rain_days = 0
    hot_days = 0
    cold_days = 0
    clear_days = 0

    for line in forecast:
        parts = line.split(" | ")
        if len(parts) < 3:
            continue

        condition = parts[1]  # ex) "🌧️ 비"
        temp_info = parts[2]  # ex) "최고: 26.0°C / 최저: 15.8°C"

        if any(word in condition for word in ["비", "이슬비", "천둥", "🌧️", "⛈️"]):
            rain_days += 1
        if "맑음" in condition:
            clear_days += 1

        try:
            max_temp = float(temp_info.split("최고:")[1].split("°")[0].strip())
            min_temp = float(temp_info.split("최저:")[1].split("°")[0].strip())
        except:
            continue

        if max_temp >= 30:
            hot_days += 1
        if min_temp <= 0:
            cold_days += 1

    notices = []

    if rain_days >= 1:
        notices.append("☔ 이번 주 중 비가 오는 날이 있습니다. 우산을 챙기세요!")
    if hot_days >= 1:
        notices.append("🔥 폭염 주의! 시원한 옷차림과 수분 섭취를 챙기세요.")
    if cold_days >= 1:
        notices.append("🧥 강추위가 예상됩니다. 따뜻하게 입으세요.")
    if clear_days == len(forecast):
        notices.append("😎 이번 주는 맑은 날씨가 계속될 예정입니다!")

    return notices


def get_weekday_korean(date_str):
    # 'YYYY-MM-DD' → 요일 반환 (예: '2025-05-22' → '목')
    date_obj = datetime.datetime.strptime(date_str, "%Y-%m-%d")
    weekdays = ['월', '화', '수', '목', '금', '토', '일']
    return weekdays[date_obj.weekday()]

def get_weather_emoji(condition):
    mapping = {
        "sunny": "☀️",
        "clear": "🌙",
        "partly cloudy": "⛅",
        "cloudy": "☁️",
        "overcast": "🌥️",
        "mist": "🌫️",
        "rain": "🌧️",
        "light rain": "🌦️",
        "heavy rain": "🌧️",
        "thunder": "⛈️",
        "snow": "❄️",
        "fog": "🌁",
        "drizzle": "🌦️"
    }
    condition_lower = condition.lower()
    for key, icon in mapping.items():
        if key in condition_lower:
            return icon
    return ""  # 매칭 안 되면 빈 이모지 반환
    
def translate_condition_to_korean(condition):
    simplified = condition.lower()

    if "light rain" in simplified: return "약한 비"
    if "heavy rain" in simplified: return "강한 비"
    if "rain" in simplified: return "비"
    if "light snow" in simplified: return "약한 눈"
    if "snow" in simplified: return "눈"
    if "drizzle" in simplified: return "이슬비"
    if "partly cloudy" in simplified: return "부분 흐림"
    if "cloudy" in simplified: return "흐림"
    if "overcast" in simplified: return "흐림"
    if "clear" in simplified: return "맑음"
    if "sunny" in simplified: return "맑음"
    if "fog" in simplified or "mist" in simplified: return "안개"
    if "thunder" in simplified: return "천둥"

    return condition

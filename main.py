import streamlit as st
import streamlit.components.v1 as components
from datetime import datetime
from google_search import google_search
from weather import get_weather, extract_city, get_forecast
from show_forecast_cards import show_forecast_cards
from weather import generate_weather_notice

# 페이지 설정
st.set_page_config(page_title="AI 비서", page_icon="🤖")

# 제목
st.title("🤖 AI 비서")
st.write("명령어를 입력해보세요! 예: **서울 날씨 알려줘**, **구글 검색 인공지능**, **시간 알려줘**")

# 사용자 입력창
command = st.text_input("명령어 입력", "")

# 명령 실행 버튼
if st.button("실행"):
    if "시간" in command:
        now = datetime.now()
        st.success(f"🕒 현재 시간은 {now.strftime('%Y-%m-%d %H:%M')}입니다.")

    elif "구글 검색" in command or "검색" in command:
        keyword = command.replace("구글 검색", "").replace("검색", "").strip()
        if keyword:
            result = google_search(keyword)
            st.success(result)
        else:
            st.warning("검색할 키워드를 입력해 주세요.")

    elif "날씨" in command and not any(word in command for word in ["예보", "날씨 예보" "일기 예보", "이번주", "일주일",  "forecast"]):
        city = extract_city(command)
        if city:
            weather_info = get_weather(city)
            st.success(weather_info)
        else:
            st.error("도시 이름을 찾을 수 없습니다. 예: '서울 날씨 알려줘'")

    elif any(word in command for word in ["예보", "일기 예보", "날씨 예보", "이번주", "일주일", "forecast"]):
        city = extract_city(command)
        if city:
            forecast = get_forecast(city)
            
            if isinstance(forecast, list):
                st.markdown("### 📅 이번 주 날씨 예보")
                show_forecast_cards(forecast)
                
                notices = generate_weather_notice(forecast)
                if notices:
                    st.markdown("### 📢 날씨에 따른 안내")
                    for msg in notices:
                        st.info(msg)
            else:
                st.error(forecast)
                
        else:
            st.error("도시 이름을 인식하지 못했습니다.")

    elif "종료" in command:
        st.info("앱은 수동으로 종료해야 합니다. 😊")

    else:
        st.warning("알 수 없는 명령입니다. 예: '시간 알려줘', '구글 검색 고양이', '서울 날씨 알려줘'")

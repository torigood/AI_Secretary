import streamlit.components.v1 as components

def show_forecast_cards(forecast):
    """
    Displays the weather forecast in a card format.
    Args:
        forecast (list): A list of strings containing weather forecast data.
    """
    if len(forecast) > 0:
        # 🔹 외부 CSS 불러오기 (필요시)
        try:
            with open("style.css", "r") as f:
                css = f.read()
                components.html(
                    f"<style>{css}</style>",
                    height=0,
                )
        except:
            pass  # style.css가 없어도 무시

        # ✅ 항상 forecast 반복
        forecast_html = ""
        for line in forecast:
            parts = line.split(" | ")
            if len(parts) < 3:
                continue
            date_info = parts[0]
            emoji_weather = parts[1].strip()
            temp_info = parts[2]

            weekday = date_info.split("(")[-1].replace(")", "")
            date = date_info.split(" ")[0]

            forecast_html += f"""
                <div class='card'>
                    <h4>{weekday}요일</h4>
                    <div class='icon'>{emoji_weather}</div>
                    <div class='date'>{date}</div>
                    <div class='temp'>{temp_info}</div>
                </div>
            """

        # 🔹 HTML 카드 표시
        components.html(
            f"""
            <style>
                .scroll-container {{
                    display: flex;
                    overflow-x: auto;
                    padding-bottom: 10px;
                }}
                .card {{
                    flex: 0 0 160px;
                    margin-right: 10px;
                    background-color: #f0f2f6;
                    padding: 16px;
                    border-radius: 12px;
                    text-align: center;
                    box-shadow: 0 2px 6px rgba(0,0,0,0.1);
                    font-family: sans-serif;
                }}
                .card h4 {{
                    margin: 5px 0;
                }}
                .icon {{
                    font-size: 27px;
                    margin: 6px 0;
                }}
                .date {{
                    font-size: 13px;
                    color: #555;
                }}
                .temp {{
                    font-size: 13px;
                    margin-top: 4px;
                }}
            </style>

            <div class="scroll-container">
                {forecast_html}
            </div>
            """,
            height=250,
            scrolling=True
        )

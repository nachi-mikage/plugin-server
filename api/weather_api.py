from flask import Blueprint, request, Response
import json
import requests

weather_bp = Blueprint('weather_api', __name__)

@weather_bp.route('/api/weather', methods=['GET'])
def get_weather():
    # クエリで都道府県名（例: tokyo）を取得
    pref = request.args.get('pref', 'tokyo').lower()

    if pref == 'tokyo':
        weather_data = fetch_tokyo_weather()
        return Response(
            json.dumps(weather_data, ensure_ascii=False),
            content_type='application/json; charset=utf-8'
        )

def fetch_tokyo_weather():
    url = "https://www.jma.go.jp/bosai/forecast/data/forecast/130000.json"
    data = requests.get(url).json()

# 今日・明日・明後日の天気文言
    time_series = data[0]["timeSeries"][0]
    weathers = time_series["areas"][0]["weathers"]  # 天気説明
    temps_series = data[0]["timeSeries"][1]  # ← [1] に気温がある
    temps_area = temps_series["areas"][0]
    temps = temps_area.get("temps", [])
    try:
        temp_min = int(temps[0])  # 今日の最低気温
    except:
        temp_min = None
    try:
        temp_max = int(temps[1])  # 今日の最高気温
    except:
        temp_max = None
    area = time_series["areas"][0]["area"]["name"]
    weather = weathers[0]


# 条件（雑に体感表現）
    if temp_max and temp_max >= 30:
        condition = "暑い"
    elif temp_max and temp_max >= 25:
        condition = "やや蒸し暑い"
    else:
        condition = "穏やか"


    return {
        "location": area,
        "weather": weather,
        "temperature": {
            "min": temp_min if temp_min is not None else "取得できず",
            "max": temp_max if temp_max is not None else "取得できず"
        },
        "condition": condition
}
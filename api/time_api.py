from flask import Blueprint, Response
from datetime import datetime
import pytz
import json

time_bp = Blueprint('time_api', __name__)

@time_bp.route('/api/time', methods=['GET'])
def get_time():
    jst = pytz.timezone('Asia/Tokyo')
    now = datetime.now(jst)

    hour = now.hour
    if 5 <= hour < 12:
        part_of_day = "朝"
    elif 12 <= hour < 19:
        part_of_day = "昼"
    else:
        part_of_day = "夜"

    # 曜日を日本語で表示する辞書マップ
    weekday_jp = {
        "Monday": "月曜日",
        "Tuesday": "火曜日",
        "Wednesday": "水曜日",
        "Thursday": "木曜日",
        "Friday": "金曜日",
        "Saturday": "土曜日",
        "Sunday": "日曜日"
    }

    # strftimeで英語表記を取得し、日本語に変換
    weekday_en = now.strftime("%A")
    weekday = weekday_jp[weekday_en]

    return Response(
    json.dumps({
        "datetime": now.isoformat(),
        "weekday": weekday,
        "time_zone": "JST",
        "part_of_day": part_of_day
    }, ensure_ascii=False),
    content_type='application/json; charset=utf-8'
)

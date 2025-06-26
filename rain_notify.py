import os
import requests
from datetime import datetime, timedelta

API_KEY = os.getenv("OWM_API_KEY")
CHANNEL_TOKEN = os.getenv("LINE_CHANNEL_TOKEN")
USER_ID = os.getenv("LINE_USER_ID")

def get_forecast():
    lat, lon = 35.6595, 139.7005  # 渋谷
    url = f"https://api.openweathermap.org/data/2.5/forecast?lat={lat}&lon={lon}&appid={API_KEY}&units=metric"
    res = requests.get(url)
    return res.json()

def send_line_message(message):
    headers = {
        "Authorization": f"Bearer {CHANNEL_TOKEN}",
        "Content-Type": "application/json"
    }
    data = {
        "to": USER_ID,
        "messages": [{"type": "text", "text": message}]
    }
    requests.post("https://api.line.me/v2/bot/message/push", headers=headers, json=data)

forecast = get_forecast()

# 明日の日付を取得（JST）
tomorrow = (datetime.utcnow() + timedelta(hours=9) + timedelta(days=1)).date()

alerts = []
for entry in forecast["list"]:
    dt = datetime.utcfromtimestamp(entry["dt"]) + timedelta(hours=9)  # JSTに変換
    if dt.date() == tomorrow:
        rain = entry.get("rain", {}).get("3h", 0)  # 3時間あたりの降水量（mm）
        rain_per_hour = rain / 3  # 1時間あたりに換算
        if rain_per_hour > 1:
            time_str = dt.strftime("%Y-%m-%d %H:%M")
            alerts.append(f"{time_str} に強い雨の予報（{rain_per_hour:.1f}mm/h）")

if alerts:
    message = "【明日の雨予報（渋谷）】\n" + "\n".join(alerts)
    send_line_message(message)

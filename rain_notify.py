import os
import requests

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
rain_info = forecast["list"][0]["weather"][0]["description"]
send_line_message(f"渋谷の天気予報: {rain_info}")


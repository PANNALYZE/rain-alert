import os
import requests
from datetime import datetime, timedelta

# 環境変数からAPIキー・トークン取得
API_KEY = os.getenv("OWM_API_KEY")
CHANNEL_TOKEN = os.getenv("LINE_CHANNEL_TOKEN")  # 個人ID不要

# 天気予報を取得（渋谷）
def get_forecast():
    lat, lon = 35.6595, 139.7005
    url = f"https://api.openweathermap.org/data/2.5/forecast?lat={lat}&lon={lon}&appid={API_KEY}&units=metric"
    res = requests.get(url)
    return res.json()

# ブロードキャスト（全員送信）
def send_broadcast_message(message):
    headers = {
        "Authorization": f"Bearer {CHANNEL_TOKEN}",
        "Content-Type": "application/json"
    }
    data = {
        "messages": [{"type": "text", "text": message}]
    }
    response = requests.post(
        "https://api.line.me/v2/bot/message/broadcast",
        headers=headers,
        json=data
    )
    print("Broadcast response:", response.status_code, response.text)

# メイン処理
forecast = get_forecast()

# JST明日の日付
tomorrow = (datetime.utcnow() + timedelta(hours=9) + timedelta(days=1)).date()

alerts = []
for entry in forecast["list"]:
    dt = datetime.utcfromtimestamp(entry["dt"]) + timedelta(hours=9)
    if dt.date() == tomorrow:
        rain = entry.get("rain", {}).get("3h", 0)
        rain_per_hour = rain / 3
        if rain_per_hour > 5:
            time_str = dt.strftime("%Y-%m-%d %H:%M")
            alerts.append(f"{time_str} に強い雨の予報（{rain_per_hour:.1f}mm/h）")

if alerts:
    message = "【明日の雨予報（渋谷）】\n" + "\n".join(alerts)
    send_broadcast_message(message)

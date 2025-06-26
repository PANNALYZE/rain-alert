import os
import requests
from datetime import datetime, timedelta

# 環境変数からAPIキー等を取得
API_KEY = os.getenv("OWM_API_KEY")
CHANNEL_TOKEN = os.getenv("LINE_CHANNEL_TOKEN")

# 天気予報取得関数（渋谷）
def get_forecast():
    lat, lon = 35.6595, 139.7005  # 渋谷
    url = f"https://api.openweathermap.org/data/2.5/forecast?lat={lat}&lon={lon}&appid={API_KEY}&units=metric"
    res = requests.get(url)
    return res.json()

# LINEにブロードキャスト送信（全友だちへ一斉送信）
def send_broadcast_message(message):
    headers = {
        "Authorization": f"Bearer {CHANNEL_TOKEN}",
        "Content-Type": "application/json"
    }
    data = {
        "messages": [{"type": "text", "text": message}]
    }
    response = requests.post("https://api.line.me/v2/bot/message/broadcast", headers=headers, json=data)
    print(response.status_code, response.text)  # デバッグ用出力

# 明日の日付（JST）を取得
forecast = get_forecast()
tomorrow = (datetime.utcnow() + timedelta(hours=9) + timedelta(days=1)).date()

# 降水量チェック
alerts = []
for entry in forecast["list"]:
    dt = datetime.utcfromtimestamp(entry["dt"]) + timedelta(hours=9)  # JST変換
    if dt.date() == tomorrow:
        rain = entry.get("rain", {}).get("3h", 0)  # 3時間あたりの降水量
        rain_per_hour = rain / 3  # 1時間換算
        if rain_per_hour > 3:
            time_str = dt.strftime("%Y-%m-%d %H:%M")
            alerts.append(f"{time_str} に強い雨の予報（{rain_per_hour:.1f}mm/h）")

# 通知送信
if alerts:
    message = "【明日の雨予報（渋谷）】\n" + "\n".join(alerts)
    send_broadcast_message(message)
else:
    print("強い雨の予報はありませんでした。")

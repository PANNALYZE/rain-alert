import requests
import os

CHANNEL_TOKEN = os.getenv("LINE_CHANNEL_TOKEN")

headers = {
    "Authorization": f"Bearer {CHANNEL_TOKEN}",
    "Content-Type": "application/json"
}

data = {
    "messages": [{
        "type": "text",
        "text": "📢 テストメッセージです（Broadcast API確認）"
    }]
}

response = requests.post(
    "https://api.line.me/v2/bot/message/broadcast",
    headers=headers,
    json=data
)

print("Status Code:", response.status_code)
print("Response:", response.text)

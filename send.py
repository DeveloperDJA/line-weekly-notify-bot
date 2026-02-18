import os
import requests
from typing import Dict, Any

LINE_PUSH_API_URL = "https://api.line.me/v2/bot/message/push"


def send_push_message(
    channel_access_token: str,
    group_id: str,
    text: str,
) -> Dict[str, Any]:

    headers = {
        "Authorization": f"Bearer {channel_access_token}",
        "Content-Type": "application/json",
    }

    payload = {
        "to": group_id,
        "messages": [
            {
                "type": "text",
                "text": text,
            }
        ],
    }

    response = requests.post(
        LINE_PUSH_API_URL,
        headers=headers,
        json=payload,
        timeout=15,
    )

    if response.status_code >= 400:
        raise requests.HTTPError(
            f"LINE push failed: status={response.status_code}, body={response.text}",
            response=response,
        )

    if not response.text.strip():
        return {"status": response.status_code, "body": None}

    return {"status": response.status_code, "body": response.json()}


def main():

    print("[INFO] Starting LINE weekly notification job")

    channel_access_token = os.environ["LINE_CHANNEL_ACCESS_TOKEN"].strip()
    group_id = os.environ["LINE_GROUP_ID"].strip()

    if not channel_access_token:
        raise ValueError("LINE_CHANNEL_ACCESS_TOKEN is empty")

    if not group_id:
        raise ValueError("LINE_GROUP_ID is empty")

    print("[INFO] Environment variables validated")

    message_text = """【定例MTGのお知らせ】

📅 毎週木曜 21:00〜  
📍 Teams

本日もよろしくお願いします！
"""

    result = send_push_message(
        channel_access_token=channel_access_token,
        group_id=group_id,
        text=message_text,
    )

    print("[INFO] LINE notification sent successfully")
    print(result)


if __name__ == "__main__":
    main()

import os
import re
import sys
import requests
from typing import Dict, Any

LINE_PUSH_API_URL = "https://api.line.me/v2/bot/message/push"
LINE_ID_PATTERN = re.compile(r"^[CUR][0-9a-fA-F]{32}$")


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
    try:
        print("[INFO] Starting LINE weekly notification job")

        channel_access_token = os.environ["LINE_CHANNEL_ACCESS_TOKEN"].strip()
        group_id = os.environ["LINE_GROUP_ID"].strip().strip('"').strip("'")

        if not channel_access_token:
            raise ValueError("LINE_CHANNEL_ACCESS_TOKEN is empty")

        if not group_id:
            raise ValueError("LINE_GROUP_ID is empty")

        if not LINE_ID_PATTERN.fullmatch(group_id):
            raise ValueError(
                "LINE_GROUP_ID format is invalid. "
                "Use source.groupId from webhook event (starts with 'C' and 33 chars total). "
                f"Current value prefix='{group_id[:10]}' length={len(group_id)}"
            )

        print("[INFO] Environment variables validated")

        message_text = """【📅 定例MTGのお知らせ】

■ 日時：毎週木曜 21:00〜
■ Teams URL：
https://teams.microsoft.com/meet/43131765033851?p=GJHg166GJsiwNDg9Fy

■ 会議ID：
431 317 650 338 51

■ パスコード：
uq6eH2uP

＝＝＝＝＝＝＝＝＝＝＝
参加できる方のみ
「👍」リアクションをお願いします
（不参加の方はリアクション不要です）
＝＝＝＝＝＝＝＝＝＝＝
"""

        result = send_push_message(
            channel_access_token=channel_access_token,
            group_id=group_id,
            text=message_text,
        )

        print("[INFO] LINE notification sent successfully")
        print(result)
        return 0
    except KeyError as exc:
        print(f"[ERROR] Missing environment variable: {exc}")
        return 1
    except Exception as exc:
        print(f"[ERROR] {exc}")
        return 1


if __name__ == "__main__":
    sys.exit(main())

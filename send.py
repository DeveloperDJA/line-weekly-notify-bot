import logging
import os
import sys
from typing import Any, Dict

import requests


LINE_PUSH_API_URL = "https://api.line.me/v2/bot/message/push"


def get_required_env(name: str) -> str:
    value = os.getenv(name)
    if not value:
        raise ValueError(f"Missing required environment variable: {name}")
    return value


def build_message_text() -> str:
    return (
        "【📅 定例MTGのお知らせ（毎週木曜 21:00〜）】\n\n"
        "■ Teams URL：\n"
        "https://teams.microsoft.com/meet/43131765033851?p=GJHg166GJsiwNDg9Fy\n\n"
        "■ 会議ID：\n"
        "431 317 650 338 51\n\n"
        "■ パスコード：\n"
        "uq6eH2uP\n\n"
        "＝＝＝＝＝＝＝＝＝＝＝\n"
        "参加できる方のみ「👍」リアクションお願いします\n"
        "（不参加の方はリアクション不要です）\n"
        "＝＝＝＝＝＝＝＝＝＝＝"
    )


def send_push_message(channel_access_token: str, group_id: str, text: str) -> Dict[str, Any]:
    headers = {
        "Authorization": f"Bearer {channel_access_token}",
        "Content-Type": "application/json",
    }
    payload = {
        "to": group_id,
        "messages": [{"type": "text", "text": text}],
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


def main() -> int:
    logging.basicConfig(
        level=logging.INFO,
        format="%(asctime)s [%(levelname)s] %(message)s",
    )

    try:
        logging.info("Starting LINE weekly notification job")

        channel_access_token = get_required_env("LINE_CHANNEL_ACCESS_TOKEN")
        group_id = get_required_env("LINE_GROUP_ID")

        logging.info("Environment variables validated")

        result = send_push_message(
            channel_access_token=channel_access_token,
            group_id=group_id,
            text=build_message_text(),
        )

        logging.info("Push message sent successfully: %s", result)
        return 0

    except Exception as exc:
        logging.exception("Job failed: %s", exc)
        return 1


if __name__ == "__main__":
    sys.exit(main())

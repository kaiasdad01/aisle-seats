from __future__ import annotations

import json
import logging
import subprocess
from typing import Sequence

import requests

from aisle_seats.seats import Seat

log = logging.getLogger(__name__)


def format_alert(seats: Sequence[Seat]) -> str:
    codes = ", ".join(s.code for s in seats)
    return f"Aisle seats available: {codes}"


def notify_console(message: str) -> None:
    print(message, flush=True)


def notify_macos(message: str) -> None:
    script = f'display notification "{message}" with title "Aisle Seats"'
    try:
        subprocess.run(["osascript", "-e", script], check=False, capture_output=True)
    except FileNotFoundError:
        log.debug("osascript not available; skipping macOS notification")


def notify_webhook(webhook_url: str, message: str, seats: Sequence[Seat]) -> None:
    payload = {
        "text": message,
        "seats": [s.code for s in seats],
    }
    response = requests.post(
        webhook_url,
        data=json.dumps(payload),
        headers={"Content-Type": "application/json"},
        timeout=15,
    )
    response.raise_for_status()


def send_alerts(
    seats: Sequence[Seat],
    *,
    webhook_url: str | None = None,
    macos: bool = True,
) -> None:
    if not seats:
        return
    message = format_alert(seats)
    notify_console(message)
    if macos:
        notify_macos(message)
    if webhook_url:
        notify_webhook(webhook_url, message, seats)

from __future__ import annotations

import os
from dataclasses import dataclass

from dotenv import load_dotenv


@dataclass(frozen=True)
class Config:
    api_base_url: str
    api_token: str
    booking_reference: str
    flight_number: str
    departure_date: str
    poll_interval_seconds: int
    webhook_url: str | None
    notify_macos: bool

    @classmethod
    def from_env(cls) -> Config:
        load_dotenv()

        api_base_url = os.getenv("API_BASE_URL", "").rstrip("/")
        if not api_base_url:
            raise ValueError("API_BASE_URL is required")

        return cls(
            api_base_url=api_base_url,
            api_token=os.getenv("API_TOKEN", ""),
            booking_reference=os.getenv("BOOKING_REFERENCE", ""),
            flight_number=os.getenv("FLIGHT_NUMBER", ""),
            departure_date=os.getenv("DEPARTURE_DATE", ""),
            poll_interval_seconds=int(os.getenv("POLL_INTERVAL_SECONDS", "300")),
            webhook_url=os.getenv("WEBHOOK_URL") or None,
            notify_macos=os.getenv("NOTIFY_MACOS", "true").lower()
            in {"1", "true", "yes"},
        )

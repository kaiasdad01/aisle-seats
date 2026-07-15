from __future__ import annotations

import requests

from aisle_seats.config import Config
from aisle_seats.seats import Seat, parse_seat_map


class SeatMapClient:
    """Thin HTTP client for whichever seat-map API you plug in."""

    def __init__(self, config: Config, session: requests.Session | None = None) -> None:
        self.config = config
        self.session = session or requests.Session()

    def fetch_seat_map(self) -> list[Seat]:
        """
        GET the current seat map for the configured booking/flight.

        Replace the path and query params below to match your API docs.
        """
        url = f"{self.config.api_base_url}/v1/seatmaps"
        headers = {"Accept": "application/json"}
        if self.config.api_token:
            headers["Authorization"] = f"Bearer {self.config.api_token}"

        params = {
            "bookingReference": self.config.booking_reference,
            "flightNumber": self.config.flight_number,
            "departureDate": self.config.departure_date,
        }
        # Drop empty params so partial configs still work during setup
        params = {k: v for k, v in params.items() if v}

        response = self.session.get(url, headers=headers, params=params, timeout=30)
        response.raise_for_status()
        return parse_seat_map(response.json())

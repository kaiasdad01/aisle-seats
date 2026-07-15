from __future__ import annotations

import json
import logging
from pathlib import Path

from aisle_seats.client import SeatMapClient
from aisle_seats.config import Config
from aisle_seats.notify import send_alerts
from aisle_seats.seats import available_aisle_seats

log = logging.getLogger(__name__)

DEFAULT_STATE_PATH = Path("state.json")


def load_seen(path: Path = DEFAULT_STATE_PATH) -> set[str]:
    if not path.exists():
        return set()
    try:
        data = json.loads(path.read_text())
        return set(data.get("seen_aisle_seats", []))
    except (json.JSONDecodeError, OSError) as exc:
        log.warning("Could not read state file %s: %s", path, exc)
        return set()


def save_seen(seen: set[str], path: Path = DEFAULT_STATE_PATH) -> None:
    path.write_text(json.dumps({"seen_aisle_seats": sorted(seen)}, indent=2) + "\n")


def check_once(config: Config, *, state_path: Path = DEFAULT_STATE_PATH) -> list[str]:
    """
    Fetch the seat map once. Alert only for aisle seats not already in state.

    Returns newly discovered aisle seat codes (empty if nothing new).
    """
    client = SeatMapClient(config)
    seats = client.fetch_seat_map()
    aisle = available_aisle_seats(seats)
    codes = {s.code for s in aisle}

    seen = load_seen(state_path)
    new_codes = sorted(codes - seen)

    if new_codes:
        new_seats = [s for s in aisle if s.code in new_codes]
        send_alerts(
            new_seats,
            webhook_url=config.webhook_url,
            macos=config.notify_macos,
        )
        save_seen(seen | codes, state_path)
        log.info("Alerted for new aisle seats: %s", ", ".join(new_codes))
    else:
        log.info(
            "No new aisle seats (%d available, %d already seen)",
            len(codes),
            len(seen & codes),
        )

    return new_codes

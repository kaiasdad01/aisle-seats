from __future__ import annotations

import argparse
import logging
import sys
import time

from aisle_seats.checker import check_once
from aisle_seats.config import Config


def main(argv: list[str] | None = None) -> int:
    parser = argparse.ArgumentParser(
        description="Poll a flight seat-map API and alert when aisle seats open."
    )
    parser.add_argument(
        "--once",
        action="store_true",
        help="Run a single check and exit (default: poll forever)",
    )
    parser.add_argument(
        "-v",
        "--verbose",
        action="store_true",
        help="Enable debug logging",
    )
    args = parser.parse_args(argv)

    logging.basicConfig(
        level=logging.DEBUG if args.verbose else logging.INFO,
        format="%(asctime)s %(levelname)s %(message)s",
        datefmt="%H:%M:%S",
    )

    try:
        config = Config.from_env()
    except ValueError as exc:
        logging.error("%s", exc)
        logging.error("Copy .env.example to .env and fill in your API details.")
        return 1

    if args.once:
        check_once(config)
        return 0

    logging.info(
        "Watching %s %s every %ss (Ctrl+C to stop)",
        config.flight_number or "(flight)",
        config.departure_date or "",
        config.poll_interval_seconds,
    )
    while True:
        try:
            check_once(config)
        except Exception:
            logging.exception("Check failed; will retry after interval")
        time.sleep(config.poll_interval_seconds)


if __name__ == "__main__":
    sys.exit(main())

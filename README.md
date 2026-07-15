# Aisle Seats

Poll a flight seat-map API and alert when aisle seats become available.

## Setup

```bash
python3 -m venv .venv
source .venv/bin/activate
pip install -r requirements.txt
cp .env.example .env
```

Edit `.env` with your API base URL, token, booking reference, flight number, and departure date.

## Run

Single check:

```bash
python -m aisle_seats --once
```

Poll forever (default interval: 5 minutes):

```bash
python -m aisle_seats
```

## Alerts

- Always prints to the console
- macOS Notification Center when `NOTIFY_MACOS=true`
- Optional JSON webhook via `WEBHOOK_URL` (Slack, ntfy, etc.)

Already-seen aisle seats are stored in `state.json` so you only get alerted on **new** openings.

## Wiring your API

`aisle_seats/client.py` calls `GET {API_BASE_URL}/v1/seatmaps` with booking/flight query params. Point that at your real endpoint (or change the path/params).

Seat payloads are normalized in `aisle_seats/seats.py`. The expected shape:

```json
{
  "seats": [
    {
      "row": 12,
      "column": "C",
      "available": true,
      "characteristics": ["AISLE"]
    }
  ]
}
```

If your API uses different field names, adjust `parse_seat_map` and/or `Seat.is_aisle`.

## Tests

```bash
python -m unittest discover -s tests -v
```

from __future__ import annotations

from dataclasses import dataclass


@dataclass(frozen=True, order=True)
class Seat:
    """A single seat on the map."""

    row: int
    letter: str
    available: bool
    characteristics: frozenset[str]

    @property
    def code(self) -> str:
        return f"{self.row}{self.letter}"

    @property
    def is_aisle(self) -> bool:
        chars = {c.lower() for c in self.characteristics}
        if chars & {"aisle", "a", "aisle_seat"}:
            return True
        # Common layout heuristic when the API only returns letters
        return self.letter.upper() in {"C", "D", "G", "H"}


def parse_seat_map(payload: dict) -> list[Seat]:
    """
    Normalize a seat-map API response into Seat objects.

    Expected shape (adapt in fetch_seat_map if your API differs):

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
    """
    seats: list[Seat] = []
    for raw in payload.get("seats", []):
        letter = str(raw.get("column") or raw.get("letter") or "").upper()
        row = int(raw.get("row"))
        chars = raw.get("characteristics") or raw.get("features") or []
        seats.append(
            Seat(
                row=row,
                letter=letter,
                available=bool(raw.get("available", False)),
                characteristics=frozenset(str(c) for c in chars),
            )
        )
    return seats


def available_aisle_seats(seats: list[Seat]) -> list[Seat]:
    return sorted(s for s in seats if s.available and s.is_aisle)

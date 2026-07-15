from aisle_seats.seats import Seat, available_aisle_seats, parse_seat_map


def test_parse_and_find_aisle_seats():
    payload = {
        "seats": [
            {
                "row": 12,
                "column": "A",
                "available": True,
                "characteristics": ["WINDOW"],
            },
            {
                "row": 12,
                "column": "C",
                "available": True,
                "characteristics": ["AISLE"],
            },
            {
                "row": 14,
                "column": "D",
                "available": False,
                "characteristics": ["AISLE"],
            },
            {"row": 15, "letter": "G", "available": True, "features": []},
        ]
    }
    seats = parse_seat_map(payload)
    aisle = available_aisle_seats(seats)
    assert [s.code for s in aisle] == ["12C", "15G"]


def test_explicit_aisle_characteristic():
    seat = Seat(
        row=10,
        letter="B",
        available=True,
        characteristics=frozenset({"aisle"}),
    )
    assert seat.is_aisle

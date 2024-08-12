from typing import TYPE_CHECKING

import pytest
import uuid

if TYPE_CHECKING:
    from django.test import Client


@pytest.mark.parametrize(
    "data",
    [
        # Interestingly enough, the test passes even when we pass a string or boolean instead of an integer.
        # I suspect it's being coerced by the Pydantic schema, but I haven't confirmed this.
        {
            "hours": "24",
            "minutes": False,
            "seconds": 45,
            "url": "https://someserver.com",
        },
        {"hours": 10, "minutes": 50, "seconds": 1, "url": "https://someserver.com"},
        {"hours": 5, "minutes": 10, "seconds": 20, "url": "https://someserver.com"},
    ],
)
def test_set_timer(data: dict[str, int | str], client: "Client") -> None:
    response = client.post("/timer", data=data, content_type="application/json")
    assert response.status_code == 200
    assert response.json()["timer_uuid"]
    assert response.json()["time_left"] > 0


@pytest.mark.parametrize(
    "data",
    [
        {
            "hours": (23, 76),
            "minutes": 30,
            "seconds": 45,
            "url": "https://google.com",
        },
        {"hours": 10, "minutes": [76], "seconds": 1, "url": "https://someserver.com"},
        {"hours": 0, "minutes": 0, "seconds": None, "url": "https://someserver.com"},
        {"hours": 0, "minutes": 0, "seconds": 0, "url": "hltps://someserver.com"},
        {"hours": -1, "minutes": 0, "seconds": None, "url": "https://someserver.com"},
    ],
)
def test_set_timer_wrong_input(data: dict[str, int | str], client: "Client") -> None:
    response = client.post("/timer", data=data, content_type="application/json")
    assert response.status_code == 422


@pytest.mark.parametrize(
    "data,expected",
    [
        (
            {"hours": 4, "minutes": 0, "seconds": 1, "url": "https://google.com"},
            4 * 3600 + 1,
        ),
        ({"hours": 0, "minutes": 0, "seconds": 10, "url": "https://google.com"}, 10),
        ({"hours": 0, "minutes": 1, "seconds": 0, "url": "https://google.com"}, 60),
        ({"hours": 0, "minutes": 0, "seconds": 5, "url": "https://google.com"}, 5),
    ],
)
def test_get_timer(data: dict[str, int | str], expected: int, client: "Client") -> None:
    response = client.post("/timer", data=data, content_type="application/json")
    timer_uuid = str(response.json()["timer_uuid"])
    response = client.get(f"/timer/{timer_uuid}", follow=True)
    assert response.status_code == 200
    # We can't guarantee the exact time left due to the time it takes to run the test.
    assert response.json()["time_left"] <= expected


def test_get_timer_does_not_exist(client: "Client") -> None:
    response = client.get(f"/timer/{uuid.uuid4()}", follow=True)
    assert response.status_code == 404

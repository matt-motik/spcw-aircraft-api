from unittest.mock import patch

import pytest

from src.aeroplane import Aeroplane
from src.aeroplanes_api import AeroplanesAPI
from src.json_storage import JsonStorage


@pytest.fixture
def plane_1():
    return Aeroplane(
        icao24="ABC123",
        callsign="AFL123",
        origin_country="Russia",
        longitude=37.5,
        latitude=55.7,
        altitude=10000.0,
        velocity=250.0,
        on_ground=False,
    )


@pytest.fixture
def plane_1_dict():
    return {
        "icao24": "ABC123",
        "callsign": "AFL123",
        "origin_country": "Russia",
        "longitude": 37.5,
        "latitude": 55.7,
        "altitude": 10000.0,
        "velocity": 250.0,
        "on_ground": False,
    }


@pytest.fixture
def plane_2():
    return Aeroplane(
        icao24="ABC000",
        callsign="AFL000",
        origin_country="Russia",
        longitude=-37.5,
        latitude=-55.7,
        altitude=11000.0,
        velocity=270.0,
        on_ground=False,
    )


@pytest.fixture
def open_sky():
    return [
        [
            "4b1812",
            "SWR438A ",
            "Switzerland",
            1766166618,
            1766166618,
            -0.0168,
            51.0888,
            4267.2,
            False,
            189.7,
            129.39,
            14.63,
            None,
            4282.44,
            "2061",
            False,
            0,
        ],
        [1, 2, 3, 4],
        12,
    ]


@pytest.fixture
def temp_storage(tmp_path, monkeypatch):
    # Подменяем get_data_dir на функцию, возвращающую tmp_path
    monkeypatch.setattr("src.json_storage.get_data_dir", lambda: tmp_path)
    return JsonStorage("test_aeroplanes.json")


@pytest.fixture
def api():
    """Создаёт экземпляр API."""
    return AeroplanesAPI()


@pytest.fixture
def mock_session():
    """Создаёт замоканную сессию requests."""
    with patch("src.aeroplanes_api.requests.Session") as mock:
        yield mock

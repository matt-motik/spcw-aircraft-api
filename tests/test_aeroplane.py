import pytest

from src.aeroplane import Aeroplane


def test_aeroplane_creation():
    plane = Aeroplane(
        icao24="ABC123",
        callsign="AFL123",
        origin_country="Russia",
        longitude=37.5,
        latitude=55.7,
        altitude=10000.0,
        velocity=250.0,
        on_ground=False,
    )
    assert plane.icao24 == "ABC123"
    assert plane.callsign == "AFL123"
    assert plane.origin_country == "Russia"
    assert plane.longitude == 37.5
    assert plane.latitude == 55.7
    assert plane.altitude == 10000.0
    assert plane.velocity == 250.0
    assert not plane.on_ground
    assert (
        str(plane)
        == "ICAO24 ABC123   | Рейс AFL123   | Страна: Russia                         "
        + "| Координаты : 55°42′0″N   / 37°30′0″E   | Высота: 10000 м | Скорость:  250 м/с | Статус: в воздухе"
    )


def test_icao24_type_error(plane_1):
    with pytest.raises(TypeError):
        plane_1.icao24 = 123456


def test_icao24_value_error(plane_1):
    with pytest.raises(ValueError):
        plane_1.icao24 = "007"

    with pytest.raises(ValueError):
        plane_1.icao24 = "не хэш"


def test_callsign_type_error(plane_1):
    with pytest.raises(TypeError):
        plane_1.callsign = 123456


def test_callsign_value_error(plane_1):
    with pytest.raises(ValueError):
        plane_1.callsign = "1234567890"


def test_origin_country_type_error(plane_1):
    with pytest.raises(TypeError):
        plane_1.origin_country = 123456


def test_longitude_none(plane_1):
    plane_1.longitude = None
    assert plane_1.longitude is None


def test_longitude_type_error(plane_1):
    with pytest.raises(TypeError):
        plane_1.longitude = "45"


def test_longitude_value_error(plane_1):
    with pytest.raises(ValueError):
        plane_1.longitude = 181

    with pytest.raises(ValueError):
        plane_1.longitude = -181


def test_latitude_none(plane_1):
    plane_1.latitude = None
    assert plane_1.latitude is None


def test_latitude_type_error(plane_1):
    with pytest.raises(TypeError):
        plane_1.latitude = "45"


def test_latitude_value_error(plane_1):
    with pytest.raises(ValueError):
        plane_1.latitude = 91

    with pytest.raises(ValueError):
        plane_1.latitude = -91


def test_altitude_type_error(plane_1):
    with pytest.raises(TypeError):
        plane_1.altitude = "45"


def test_velocity_type_error(plane_1):
    with pytest.raises(TypeError):
        plane_1.velocity = "45"


def test_velocity_value_error(plane_1):
    with pytest.raises(ValueError):
        plane_1.velocity = -250


def test_on_ground_type_error(plane_1):
    with pytest.raises(TypeError):
        plane_1.on_ground = "45"


def test_lt(plane_1, plane_2):
    assert plane_1 < plane_2


def test_gt(plane_1, plane_2):
    assert plane_2 > plane_1


def test_eq(plane_1, plane_2):
    plane_2.altitude = plane_1.altitude
    plane_2.velocity = plane_1.velocity
    assert plane_2 == plane_1


def test_le(plane_1, plane_2):
    plane_2.altitude = plane_1.altitude
    plane_2.velocity = plane_1.velocity
    assert plane_2 <= plane_1
    plane_2.velocity = plane_1.velocity - 1
    assert plane_2 <= plane_1


def test_ge(plane_1, plane_2):
    plane_2.altitude = plane_1.altitude
    plane_2.velocity = plane_1.velocity
    assert plane_2 >= plane_1
    plane_2.velocity = plane_1.velocity + 1
    assert plane_2 >= plane_1


def test_eq_type_error(plane_1):
    assert (plane_1.__eq__(1)) is NotImplemented


def test_lt_type_error(plane_1):
    assert (plane_1.__lt__(1)) is NotImplemented


def test__decimal_to_dms_none():
    assert Aeroplane._decimal_to_dms(None) == "N/A"


def test_cast_to_object_list(open_sky):
    aeroplanes = Aeroplane.cast_to_object_list(open_sky)
    assert isinstance(aeroplanes, list)
    assert isinstance(aeroplanes[0], Aeroplane)
    assert len(aeroplanes) == 1
    assert aeroplanes[0].icao24 == "4B1812"
    assert aeroplanes[0].altitude == 4267.2


def test_cast_to_object_type_error():
    with pytest.raises(TypeError):
        Aeroplane.cast_to_object_list(44)


def test_to_dict(plane_1, plane_1_dict):
    assert plane_1.to_dict() == plane_1_dict


def test_from_dict(plane_1, plane_1_dict):
    test = Aeroplane.from_dict(plane_1_dict)
    assert test.icao24 == plane_1.icao24
    assert test.longitude == plane_1.longitude
    assert test.latitude == plane_1.latitude
    assert test.altitude == plane_1.altitude
    assert test.velocity == plane_1.velocity
    assert test.on_ground == plane_1.on_ground
    assert test.callsign == plane_1.callsign
    assert test.origin_country == plane_1.origin_country

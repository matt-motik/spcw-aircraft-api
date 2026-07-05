import json
import os
import stat

import pytest

from src.aeroplane import Aeroplane
from src.json_storage import JsonStorage


def test_init_type_error():
    with pytest.raises(TypeError):
        _ = JsonStorage(123)


def test_init_empty(temp_storage):
    assert temp_storage.get_aeroplanes() == []


def test_add_and_get(temp_storage, plane_1):
    temp_storage.add_aeroplane(plane_1)
    assert len(temp_storage.get_aeroplanes()) == 1
    assert temp_storage.get_aeroplanes()[0].icao24 == "ABC123"


def test_add_type_error(temp_storage):
    result = temp_storage.get_aeroplanes()
    old_len = len(result)
    with pytest.raises(TypeError):
        temp_storage.add_aeroplane(123)

    planes = temp_storage.get_aeroplanes()
    assert len(planes) == old_len


def test_add_duplicate_updates(temp_storage, plane_1):
    temp_storage.add_aeroplane(plane_1)
    # Создаём обновлённый самолёт с тем же icao24
    updated = Aeroplane(
        icao24="ABC123",
        callsign="NEW",
        origin_country="USA",
        longitude=0,
        latitude=0,
        altitude=0,
        velocity=0,
        on_ground=True,
    )
    temp_storage.add_aeroplane(updated)
    result = temp_storage.get_aeroplanes()
    assert len(result) == 1
    assert result[0].altitude == 0  # число, а не строка!
    assert result[0].callsign == "NEW"


def test_add_multiple_aeroplanes(temp_storage, plane_1, plane_2):
    temp_storage.add_multiple_aeroplanes([plane_1, plane_2, plane_1])
    result = temp_storage.get_aeroplanes()
    assert len(result) == 2
    icaos = {p.icao24 for p in result}
    assert icaos == {"ABC123", "ABC000"}


def test_add_multiple_aeroplanes_type_error(temp_storage):
    result = temp_storage.get_aeroplanes()
    old_len = len(result)
    with pytest.raises(TypeError):
        temp_storage.add_multiple_aeroplanes(123)

    planes = temp_storage.get_aeroplanes()
    assert len(planes) == old_len


def test_add_multiple_aeroplanes_all_type_error(temp_storage):
    result = temp_storage.get_aeroplanes()
    old_len = len(result)
    with pytest.raises(TypeError):
        temp_storage.add_multiple_aeroplanes([123])

    planes = temp_storage.get_aeroplanes()
    assert len(planes) == old_len


def test_delete_existing(temp_storage, plane_1):
    temp_storage.add_aeroplane(plane_1)
    temp_storage.delete_aeroplane(plane_1)
    assert temp_storage.get_aeroplanes() == []


def test_delete_type_error(temp_storage, plane_1):
    with pytest.raises(TypeError):
        temp_storage.delete_aeroplane(1)


def test_delete_nonexistent(temp_storage, plane_1):
    with pytest.raises(ValueError):
        temp_storage.delete_aeroplane(plane_1)


def test_get_aeroplanes_filters(temp_storage, plane_1, plane_2):
    temp_storage.add_multiple_aeroplanes([plane_1, plane_2])

    # По стране
    result = temp_storage.get_aeroplanes(origin_country="Russia")
    assert len(result) == 2

    # По высоте
    result = temp_storage.get_aeroplanes(min_altitude=10500, max_altitude=12000)
    assert len(result) == 1
    assert result[0].icao24 == "ABC000"

    # По скорости
    result = temp_storage.get_aeroplanes(min_velocity=240, max_velocity=260)
    assert len(result) == 1
    assert result[0].icao24 == "ABC123"

    # По координатам
    result = temp_storage.get_aeroplanes(min_latitude=50, max_latitude=60, min_longitude=30, max_longitude=40)
    assert len(result) == 1
    assert result[0].icao24 == "ABC123"

    # На земле
    result = temp_storage.get_aeroplanes(on_ground=False)
    assert len(result) == 2

    # Неверный ключ
    with pytest.raises(ValueError):
        temp_storage.get_aeroplanes(invalid_key="test")


def test_init_json_not_list(tmp_path, monkeypatch):
    path = tmp_path / "test.json"
    path.write_text('{"key": "value"}')  # валидный JSON, но словарь

    monkeypatch.setattr("src.json_storage.get_data_dir", lambda: tmp_path)
    storage = JsonStorage("test.json")
    assert storage.get_aeroplanes() == []


def test_init_json_invalid_json(tmp_path, monkeypatch):
    path = tmp_path / "test.json"
    path.write_text("{ 1 : invalid json")  # не валидный JSON

    monkeypatch.setattr("src.json_storage.get_data_dir", lambda: tmp_path)
    storage = JsonStorage("test.json")
    assert storage.get_aeroplanes() == []


def test_init_json_with_valid_data(tmp_path, monkeypatch):
    path = tmp_path / "test.json"
    path.write_text(
        json.dumps(
            [
                {
                    "icao24": "ABC123",
                    "callsign": "AFL123",
                    "origin_country": "Russia",
                    "longitude": 37.5,
                    "latitude": 55.7,
                    "altitude": 10000.0,
                    "velocity": 250.0,
                    "on_ground": False,
                }
            ]
        )
    )

    monkeypatch.setattr("src.json_storage.get_data_dir", lambda: tmp_path)
    storage = JsonStorage("test.json")
    assert len(storage.get_aeroplanes()) == 1
    assert storage.get_aeroplanes()[0].icao24 == "ABC123"


def test_save_os_error(temp_storage, plane_1, monkeypatch):
    temp_storage.add_aeroplane(plane_1)
    path = temp_storage._storage_path
    # Делаем файл только для чтения
    os.chmod(path, stat.S_IREAD)
    try:
        temp_storage.add_aeroplane(plane_1)  # вызовет _save, который упадёт
    finally:
        os.chmod(path, stat.S_IWRITE)  # восстанавливаем права для очистки tmp_path

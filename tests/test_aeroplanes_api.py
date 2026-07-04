from unittest.mock import Mock
from unittest.mock import patch

import pytest

from src.aeroplanes_api import AeroplanesAPI


def test_init():
    api = AeroplanesAPI()
    assert api.nominatim_url == "https://nominatim.openstreetmap.org/search"
    assert api.opensky_url == "https://opensky-network.org/api/states/all"


def test_get_country_bbox_success(api):
    mock_response = Mock()
    mock_response.json.return_value = [{"boundingbox": ["10.5", "20.5", "30.5", "40.5"]}]
    mock_response.raise_for_status.return_value = None

    with patch.object(api.session, "get", return_value=mock_response):
        bbox = api.get_country_bbox("Testland")
        assert bbox == {"lamin": 10.5, "lamax": 20.5, "lomin": 30.5, "lomax": 40.5}


def test_get_country_bbox_not_found(api):
    mock_response = Mock()
    mock_response.json.return_value = None
    mock_response.raise_for_status.return_value = None

    with patch.object(api.session, "get", return_value=mock_response):
        with pytest.raises(RuntimeError):
            api.get_country_bbox("Testland")


def test_get_country_bbox_key_error(api):
    mock_response = Mock()
    mock_response.json.return_value = [{"bbox": ["10.5", "20.5", "30.5", "40.5"]}]
    mock_response.raise_for_status.return_value = None

    with patch.object(api.session, "get", return_value=mock_response):
        with pytest.raises(RuntimeError):
            api.get_country_bbox("Testland")


def test_get_country_bbox_http_error(api):
    mock_response = Mock()
    mock_response.raise_for_status.side_effect = __import__("requests").exceptions.HTTPError("500 Server Error")

    with patch.object(api.session, "get", return_value=mock_response):
        with pytest.raises(RuntimeError, match="Ошибка запроса"):
            api.get_country_bbox("Testland")


def test_get_aeroplanes_success(api):
    """Успешное получение списка самолётов."""
    mock_nominatim = Mock()
    mock_nominatim.json.return_value = [{"boundingbox": ["10", "20", "30", "40"]}]
    mock_nominatim.raise_for_status.return_value = None

    mock_opensky = Mock()
    mock_opensky.json.return_value = {
        "states": [["abc123", "AFL123", "Russia", None, None, 15.5, 35.7, 10000.0, False, 250.0]]
    }
    mock_opensky.raise_for_status.return_value = None

    with patch.object(api.session, "get", side_effect=[mock_nominatim, mock_opensky]):
        states = api.get_aeroplanes("Russia")
        assert len(states) == 1
        assert states[0][0] == "abc123"


def test_get_aeroplanes_no_states_key(api):
    """Ответ OpenSky без ключа 'states'."""
    mock_nominatim = Mock()
    mock_nominatim.json.return_value = [{"boundingbox": ["10", "20", "30", "40"]}]
    mock_nominatim.raise_for_status.return_value = None

    mock_opensky = Mock()
    mock_opensky.json.return_value = {"no_states": []}
    mock_opensky.raise_for_status.return_value = None

    with patch.object(api.session, "get", side_effect=[mock_nominatim, mock_opensky]):
        with pytest.raises(RuntimeError, match="отсутствует ключ 'states'"):
            api.get_aeroplanes("Russia")


def test_get_aeroplanes_opensky_error(api):
    """OpenSky возвращает HTTP-ошибку."""
    mock_nominatim = Mock()
    mock_nominatim.json.return_value = [{"boundingbox": ["10", "20", "30", "40"]}]
    mock_nominatim.raise_for_status.return_value = None

    mock_opensky = Mock()
    mock_opensky.raise_for_status.side_effect = __import__("requests").exceptions.HTTPError("500 Error")

    with patch.object(api.session, "get", side_effect=[mock_nominatim, mock_opensky]):
        with pytest.raises(RuntimeError, match="Не удалось получить данные о самолётах"):
            api.get_aeroplanes("Russia")


def test_make_request_json_decode_error(api):
    """Ответ с некорректным JSON."""
    mock_response = Mock()
    mock_response.json.side_effect = ValueError("Invalid JSON")
    mock_response.raise_for_status.return_value = None

    with patch.object(api.session, "get", return_value=mock_response):
        with pytest.raises(RuntimeError, match="Некорректный JSON"):
            api._make_request("http://test.com", {})


def test_make_request_network_error(api):
    """Ошибка сети."""
    with patch.object(api.session, "get", side_effect=__import__("requests").exceptions.ConnectionError("No network")):
        with pytest.raises(RuntimeError, match="Ошибка запроса"):
            api._make_request("http://test.com", {})

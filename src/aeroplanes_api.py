"""Модуль класса для работы с внешними API (Nominatim + OpenSky)."""

from typing import Any, Dict, List

import requests

from .base_api import BaseAPI


class AeroplanesAPI(BaseAPI):
    """
    Класс для работы с API nominatim.openstreetmap.org и opensky-network.org.

    Реализует получение bounding box страны и списка самолётов в её воздушном пространстве.
    """

    def __init__(self) -> None:
        """Инициализация клиента API."""
        self.session = requests.Session()
        self.session.headers.update({
            "User-Agent": "Skypro-Coursework-AircraftAPI/1.0 (educational project)"
        })

        # Базовые URL
        self.nominatim_url = "https://nominatim.openstreetmap.org/search"
        self.opensky_url = "https://opensky-network.org/api/states/all"

        self.aeroplanes = None

    def get_country_bbox(self, country_name: str) -> Dict[str, float]:
        """
        Получает bounding box страны через Nominatim API.

        Args:
            country_name: Название страны (например, "Spain", "Russia")

        Returns:
            Словарь с координатами: {'latmin': , 'lonmin': , 'latmax': , 'lonmax': }

        Raises:
            RuntimeError: Если страна не найдена или запрос неуспешен.
        """
        # Указываем параметры: в каком формате возвращать данные и максимальную длину списка стран в ответе.
        params = {
            'country': country_name,
            'format': 'json',
            'limit': 1,
        }

        data = self._make_request(self.nominatim_url, params)

        if not data:
            raise RuntimeError(f"Страна '{country_name}' не найдена.")

        try:
            bbox = data[0]['boundingbox']
            return {
                'lamin': float(bbox[0]),  # south (минимальная широта)
                'lamax': float(bbox[1]),  # north (максимальная широта)
                'lomin': float(bbox[2]),  # west (минимальная долгота)
                'lomax': float(bbox[3]),  # east (максимальная долгота)
            }
        except (KeyError, IndexError, TypeError, ValueError) as e:
            raise RuntimeError(f"Некорректный формат ответа от Nominatim для страны '{country_name}': {e}") from e

    def get_aeroplanes(self, country_name: str) -> List[Dict[str, Any]]:
        """
        Получает список самолётов в воздушном пространстве указанной страны.

        1. Получает bounding box страны.
        2. Делает запрос к OpenSky API.

        Args:
            country_name: Название страны.

        Returns:
            Список словарей с данными о самолётах.

        Raises:
            RuntimeError: При ошибках API или если страна не найдена.
        """

        bbox = self.get_country_bbox(country_name)

        try:
            data = self._make_request(self.opensky_url, bbox)
            if 'states' not in data:
                raise RuntimeError(f"Некорректный ответ OpenSky: отсутствует ключ 'states'")
            self.aeroplanes = data['states']  # сохраняем именно список
            return data['states']
        except RuntimeError as e:
            raise RuntimeError(f"Не удалось получить данные о самолётах для страны '{country_name}': {e}") from e

    def _make_request(self, url: str, params: Dict[str, Any]) -> Dict[str, Any]:
        """
        Вспомогательный метод для выполнения HTTP-запросов с обработкой ошибок.

        Используется внутри класса.
        """
        try:
            response = self.session.get(url=url, params=params, timeout=10)
            response.raise_for_status()  # автоматически поднимает исключение при 4xx/5xx
            return response.json()
        except requests.exceptions.RequestException as e:
            raise RuntimeError(f"Ошибка запроса к {url}: {e}") from e
        except ValueError as e:
            raise RuntimeError(f"Некорректный JSON в ответе от {url}: {e}") from e

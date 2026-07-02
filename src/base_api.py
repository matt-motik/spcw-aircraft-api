"""Модуль базового класса для работы с внешними API."""
from abc import ABC, abstractmethod


class BaseAPI(ABC):
    """Абстрактный класс для работы с внешними API."""

    @abstractmethod
    def get_country_bbox(self, country_name: str) -> dict:
        """Метод получения bounding box страны."""
        pass

    @abstractmethod
    def get_aeroplanes(self, country_name: str) -> list:
        """Метод получения списка самолётов."""
        pass

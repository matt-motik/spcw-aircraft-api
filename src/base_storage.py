"""Модуль базового класса для работы с хранилищем самолётов."""

from abc import ABC
from abc import abstractmethod
from typing import Any

from .aeroplane import Aeroplane


class BaseStorage(ABC):
    """
    Абстрактный базовый класс для хранилища данных о самолётах.

    Определяет интерфейс для добавления, получения и удаления записей.
    Конкретные реализации (JSON, CSV, БД) должны переопределить все методы.
    """

    @abstractmethod
    def add_aeroplane(self, aeroplane: Aeroplane) -> None:
        """
        Добавляет запись о самолёте в хранилище.

        Args:
            aeroplane: Экземпляр класса Aeroplane.

        Raises:
            TypeError: Если передан объект не типа Aeroplane.
            FileNotFoundError: Если файл хранилища не найден (при необходимости).
        """
        pass

    @abstractmethod
    def add_multiple_aeroplanes(self, aeroplanes: list[Aeroplane]) -> None:
        """
        Пакетное добавление/обновление списка самолётов с однократным сохранением.

        Args:
            aeroplanes: Список объектов Aeroplane.

        Raises:
            TypeError: Если передан объект не типа List[Aeroplane].
        """
        pass

    @abstractmethod
    def get_aeroplanes(self, **filters: dict[str, Any]) -> list[Aeroplane]:
        """
        Возвращает список самолётов, удовлетворяющих заданным фильтрам.

        Args:
            **filters: Именованные параметры для фильтрации.
                       Поддерживаемые ключи зависят от реализации.
                       Например: origin_country='Russia', min_altitude=10000.

        Returns:
            Список объектов Aeroplane, соответствующих критериям.

        Raises:
            ValueError: Если переданы некорректные ключи фильтрации.
        """
        pass

    @abstractmethod
    def delete_aeroplane(self, aeroplane: Aeroplane) -> None:
        """
        Удаляет запись о самолёте из хранилища.

        Сравнение производится по уникальному идентификатору icao24.

        Args:
            aeroplane: Экземпляр Aeroplane, который требуется удалить.

        Raises:
            ValueError: Если самолёт с таким icao24 не найден в хранилище.
        """
        pass

    @abstractmethod
    def add_country(self, country_name: str, bbox: dict[str, float]) -> int | None:
        """
        Добавляет страну в хранилище.

        Returns:
            id страны или None, если хранилище не поддерживает страны.
        """
        pass

    @abstractmethod
    def get_country(self, country_name: str) -> dict | None:
        """
        Получает данные о стране из хранилища.

        Returns:
            {
                'id': int,
                'lat_min': float,
                'lat_max': float,
                'lon_min': float,
                'lon_max': float
            }
            или None, если не найдена или не поддерживается.
        """
        pass

    @abstractmethod
    def initialize(self) -> None:
        """Подготовка хранилища (создание таблиц, файлов и т.д.)."""
        pass

    @abstractmethod
    def close(self) -> None:
        """Закрывает хранилище если поддерживает."""
        pass

    @abstractmethod
    def get_aeroplanes_with_keyword(self, keyword: str) -> list[Aeroplane]:
        """
        Получает самолёты, в позывном которых содержится keyword.

        Args:
            keyword: Подстрока для поиска (например, 'AFL').
        """
        pass

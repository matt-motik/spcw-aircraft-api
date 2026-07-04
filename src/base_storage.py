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

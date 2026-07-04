"""Модуль класса для работы с JSON-хранилищем самолётов."""

import json
import os
from typing import Any

from .aeroplane import Aeroplane
from .base_storage import BaseStorage
from .logger_creator import create_logger
from .path import get_data_dir

logger = create_logger(__name__)


class JsonStorage(BaseStorage):
    """
    Класс для хранилища данных о самолётах.

    Определяет Класс для добавления, получения и удаления записей.
    """

    def __init__(self, storage_path: str) -> None:
        """Инициализация хранилища."""
        self._storage: list[Aeroplane] = []
        datadir = get_data_dir()
        self._storage_path: str = os.path.join(datadir, storage_path)
        json_data = self._read_json_file()
        if isinstance(json_data, list):
            for data in json_data:
                self._storage.append(Aeroplane.from_dict(data))
        else:
            logger.warning("JSON-файл не содержит список, хранилище будет пустым")

        logger.info("Хранилище инициализировано, самолётов: %d", len(self._storage))

    def add_aeroplane(self, aeroplane: Aeroplane) -> None:
        """
        Добавляет запись о самолёте в хранилище.

        Args:
            aeroplane: Экземпляр класса Aeroplane.

        Raises:
            TypeError: Если передан объект не типа Aeroplane.
        """
        if not isinstance(aeroplane, Aeroplane):
            raise TypeError("aeroplane должен быть типа Aeroplane.")
        index = next((i for i, p in enumerate(self._storage) if p.icao24 == aeroplane.icao24), None)
        if index is not None:
            self._storage[index] = aeroplane  # обновление
        else:
            self._storage.append(aeroplane)  # добавление нового
        self._save()

    def add_multiple_aeroplanes(self, aeroplanes: list[Aeroplane]) -> None:
        """
        Пакетное добавление/обновление списка самолётов с однократным сохранением.

        Args:
            aeroplanes: Список объектов Aeroplane.

        Raises:
            TypeError: Если передан объект не типа List[Aeroplane].
        """
        if not isinstance(aeroplanes, list):
            raise TypeError("aeroplanes должен быть списком.")
        added = 0
        updated = 0
        for aeroplane in aeroplanes:
            if not isinstance(aeroplane, Aeroplane):
                raise TypeError("Все элементы списка должны быть типа Aeroplane.")
            index = next((i for i, p in enumerate(self._storage) if p.icao24 == aeroplane.icao24), None)
            if index is not None:
                updated += 1
                self._storage[index] = aeroplane
            else:
                added += 1
                self._storage.append(aeroplane)
        logger.info(f"В хранилище добавлено {added}, обновлено {updated} самолётов")
        self._save()

    def get_aeroplanes(self, **filters: Any) -> list[Aeroplane]:
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
        valid_keys = {
            "origin_country",
            "min_altitude",
            "max_altitude",
            "min_velocity",
            "max_velocity",
            "on_ground",
            "min_latitude",
            "max_latitude",
            "min_longitude",
            "max_longitude",
        }
        for key in filters:
            if key not in valid_keys:
                raise ValueError(f"Некорректный фильтр: {key}")

        result = self._storage
        if "origin_country" in filters:
            country = str(filters["origin_country"]).strip().upper()
            result = [p for p in result if p.origin_country.upper() == country]
        if "min_altitude" in filters:
            min_alt = float(filters["min_altitude"])
            result = [p for p in result if p.altitude >= min_alt]
        if "max_altitude" in filters:
            max_alt = float(filters["max_altitude"])
            result = [p for p in result if p.altitude <= max_alt]
        if "min_velocity" in filters:
            min_vel = float(filters["min_velocity"])
            result = [p for p in result if p.velocity >= min_vel]
        if "max_velocity" in filters:
            max_vel = float(filters["max_velocity"])
            result = [p for p in result if p.velocity <= max_vel]
        if "on_ground" in filters:
            on_gr = bool(filters["on_ground"])
            result = [p for p in result if p.on_ground == on_gr]
        if "min_latitude" in filters:
            min_lat = float(filters["min_latitude"])
            result = [p for p in result if p.latitude is not None and p.latitude >= min_lat]
        if "max_latitude" in filters:
            max_lat = float(filters["max_latitude"])
            result = [p for p in result if p.latitude is not None and p.latitude <= max_lat]
        if "min_longitude" in filters:
            min_lon = float(filters["min_longitude"])
            result = [p for p in result if p.longitude is not None and p.longitude >= min_lon]
        if "max_longitude" in filters:
            max_lon = float(filters["max_longitude"])
            result = [p for p in result if p.longitude is not None and p.longitude <= max_lon]

        return result

    def delete_aeroplane(self, aeroplane: Aeroplane) -> None:
        """
        Удаляет запись о самолёте из хранилища.

        Сравнение производится по уникальному идентификатору icao24.

        Args:
            aeroplane: Экземпляр Aeroplane, который требуется удалить.

        Raises:
            ValueError: Если самолёт с таким icao24 не найден в хранилище.
        """
        if not isinstance(aeroplane, Aeroplane):
            raise TypeError("aeroplane должен быть типа Aeroplane.")
        index = next((i for i, p in enumerate(self._storage) if p.icao24 == aeroplane.icao24), None)
        if index is not None:
            self._storage.pop(index)
            self._save()
        else:
            raise ValueError(f"Самолёт с icao24={aeroplane.icao24!r} не найден в хранилище.")

    def _read_json_file(self) -> Any | None:
        """Функция чтения JSON-файла.

        Returns:
            JSON объект или None в случае неудачи.

        Example:

            >>> result = self._read_json_file()
        """
        logger.debug(f"Проверка JSON-файла filename '{self._storage_path}' на существование")

        if os.path.exists(self._storage_path):
            logger.debug(f"JSON-файла '{self._storage_path}' существует")
            logger.debug(f"Открываем JSON-файл '{self._storage_path}' на чтение")
            with open(self._storage_path, "r", encoding="utf-8") as f:
                try:
                    logger.debug("Читаем JSON-файл'")
                    result = json.load(f)
                    return result
                except json.JSONDecodeError as err:
                    logger.warning(f"Данные не являются корректным JSON. Возвращаем None. {str(err)}", exc_info=True)
                    return None
        else:
            logger.warning(f"JSON-файл {self._storage_path!r} не существует. Возвращаем None. ")
            return None

    def _save(self) -> None:
        """Функция записи JSON-файла.

        Returns:
            None

        Example:

            >>> self._save()
        """
        logger.debug(f"Открываем JSON-файл '{self._storage_path}' на запись")
        try:
            with open(self._storage_path, "w", encoding="utf-8") as f:
                data = []
                for plane in self._storage:
                    data.append(plane.to_dict())
                logger.debug("Пишем JSON-файл'")
                json.dump(data, f, ensure_ascii=False, indent=4)
        except OSError as err:
            logger.error(f"JSON-файл не сохранён. {str(err)}", exc_info=True)
            return

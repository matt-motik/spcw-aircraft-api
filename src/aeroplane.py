"""Модуль класса, моделирующего данные самолёта."""

from functools import total_ordering
from typing import Any
from typing import Optional

from .logger_creator import create_logger

logger = create_logger(__name__)


@total_ordering
class Aeroplane:
    """
    Класс, представляющий данные о самолёте.

    Инкапсулирует атрибуты, полученные из API OpenSky Network, и предоставляет
        методы для валидации, сравнения и создания объектов из сырых данных.
    """

    # Ожидаемые индексы в массиве состояния от OpenSky API
    _STATE_ICAO24 = 0
    _STATE_CALLSIGN = 1
    _STATE_ORIGIN_COUNTRY = 2
    _STATE_LONGITUDE = 5
    _STATE_LATITUDE = 6
    _STATE_BARO_ALTITUDE = 7
    _STATE_ON_GROUND = 8
    _STATE_VELOCITY = 9

    def __init__(
        self,
        icao24: str,  # Уникальный идентификатор борта
        callsign: str,  # Позывной рейса
        origin_country: str,  # Страна регистрации воздушного судна.
        longitude: float | None,  # Долгота (°)
        latitude: float | None,  # Широта(°)
        altitude: float,  # Барометрическая высота в метрах.
        velocity: float,  # Скорость относительно земли в м/с (>=0).
        on_ground: bool,  # Флаг нахождения на земле.
    ) -> None:
        """
        Инициализация объекта самолёта с валидацией.

        Args:
            icao24: Уникальный 24-битный идентификатор борта (транспондера) (hex).
            callsign: Позывной рейса (может быть пустым).
            origin_country: Страна регистрации воздушного судна.
            longitude: Долгота (°)
            latitude: Широта(°)
            altitude: Барометрическая высота в метрах.
            velocity: Скорость относительно земли в м/с (>=0).
            on_ground: Флаг нахождения на земле.

        Raises:
            ValueError: Если параметры не проходят валидацию.
        """
        logger.debug("Создаем Самолёт.")
        self.icao24 = icao24
        self.callsign = callsign
        self.origin_country = origin_country
        self.longitude = longitude
        self.latitude = latitude
        self.altitude = altitude
        self.velocity = velocity
        self.on_ground = on_ground
        logger.debug(f"Самолёт cоздан успешно. {self.__repr__()}.")

    @property
    def icao24(self) -> str:
        """Геттер. Уникальный идентификатор борта (транспондера)."""
        return self._icao24

    @icao24.setter
    def icao24(self, value: str) -> None:
        """Сеттер. Уникальный идентификатор борта (транспондера)."""
        if not isinstance(value, str):
            raise TypeError(f"icao24 должен быть строкой. Получен {value}:{type(value).__name__}.")
        clean = str(value).strip().upper()
        if len(clean) != 6:
            raise ValueError(f"icao24 должен содержать ровно 6 символов. Получено {len(clean)}: '{clean}'")
        try:
            int(clean, 16)  # проверка на hex
        except ValueError:
            raise ValueError(f"icao24 должен быть шестнадцатеричной строкой (0-9, A-F). '{clean}'") from None
        self._icao24 = clean

    @property
    def callsign(self) -> str:
        """Позывной рейса."""
        return self._callsign

    @callsign.setter
    def callsign(self, value: str) -> None:
        """Сеттер. Позывной рейса."""
        if not isinstance(value, str):
            raise TypeError(f"callsign должен быть строкой. Получен {value}:{type(value).__name__}.")
        clean = value.strip().upper()
        if len(clean) > 8:
            raise ValueError(f"callsign должен содержать не более 8 символов. Получено {len(clean)}: '{clean}'")
        self._callsign = clean

    @property
    def origin_country(self) -> str:
        """Страна регистрации."""
        return self._origin_country

    @origin_country.setter
    def origin_country(self, value: str) -> None:
        """Сеттер. Страна регистрации."""
        if not isinstance(value, str):
            raise TypeError(f"origin_country должен быть строкой. Получен {value}:{type(value).__name__}.")
        self._origin_country = value.strip()

    @property
    def longitude(self) -> float | None:
        """Долгота (°)."""
        return self._longitude

    @longitude.setter
    def longitude(self, value: float | None) -> None:
        """Сеттер. Долгота (°)."""
        if value is None:
            self._longitude = None
            return
        if not isinstance(value, (float, int)):
            raise TypeError(f"longitude должен быть числом. Получен {value}:{type(value).__name__}.")
        if not (-180 <= value <= 180):
            raise ValueError(f"Значение longitude должно быть от -180 до 180. Получен {value}")
        self._longitude = value

    @property
    def latitude(self) -> float | None:
        """Широта (°)."""
        return self._latitude

    @latitude.setter
    def latitude(self, value: float | None) -> None:
        """Сеттер. Широта (°)."""
        if value is None:
            self._latitude = None
            return
        if not isinstance(value, (float, int)):
            raise TypeError(f"latitude должен быть числом. Получен {value}:{type(value).__name__}.")
        if not (-90 <= value <= 90):
            raise ValueError(f"Значение latitude должно быть от -90 до 90. Получен {value}")
        self._latitude = value

    @property
    def altitude(self) -> float:
        """Барометрическая высота, м."""
        return self._altitude

    @altitude.setter
    def altitude(self, value: float) -> None:
        """Сеттер. Барометрическая высота, м."""
        if not isinstance(value, (float, int)):
            raise TypeError(f"altitude должен быть числом. Получен {value}:{type(value).__name__}.")
        self._altitude = value

    @property
    def velocity(self) -> float:
        """Скорость относительно земли, м/с."""
        return self._velocity

    @velocity.setter
    def velocity(self, value: float) -> None:
        """Сеттер. Скорость относительно земли, м/с."""
        if not isinstance(value, (float, int)):
            raise TypeError(f"velocity должен быть числом. Получен {value}:{type(value).__name__}.")
        if value < 0:
            raise ValueError("velocity должен быть больше 0.")
        self._velocity = value

    @property
    def on_ground(self) -> bool:
        """Флаг нахождения на земле."""
        return self._on_ground

    @on_ground.setter
    def on_ground(self, value: bool) -> None:
        """Сеттер. Флаг нахождения на земле."""
        if not isinstance(value, bool):
            raise TypeError(f"on_ground должен быть булевым значением. Получен {value}:{type(value).__name__}.")
        self._on_ground = value

    # ---------- методы сравнения ----------
    def __eq__(self, other: object) -> bool:
        """Сравнение самолётов по (высота, скорость)."""
        if not isinstance(other, Aeroplane):
            return NotImplemented
        return (self.altitude, self.velocity) == (other.altitude, other.velocity)

    def __lt__(self, other: object) -> bool:
        """Меньше — значит ниже (или медленнее при равной высоте)."""
        if not isinstance(other, Aeroplane):
            return NotImplemented
        return (self.altitude, self.velocity) < (other.altitude, other.velocity)

    @staticmethod
    def _decimal_to_dms(decimal_degrees: float | None, is_latitude: bool = True) -> str:
        """Преобразует десятичные градусы в строку вида 55°45′6″N."""
        if decimal_degrees is None:
            return "N/A"

        if is_latitude:
            direction = "N" if decimal_degrees >= 0 else "S"
        else:
            direction = "E" if decimal_degrees >= 0 else "W"

        absolute = abs(decimal_degrees)
        degrees = int(absolute)
        minutes_full = (absolute - degrees) * 60
        minutes = int(minutes_full)
        seconds = (minutes_full - minutes) * 60

        return f"{degrees}°{minutes}′{seconds:.0f}″{direction}"

    def __repr__(self) -> str:
        """Репрезентация."""
        return (
            f"Aeroplane(icao24={self.icao24!r}, callsign={self.callsign!r}, "
            f"origin_country={self.origin_country!r}, longitude={self.longitude}, "
            f"latitude={self.latitude}, altitude={self.altitude}, "
            f"velocity={self.velocity}, on_ground={self.on_ground})"
        )

    def __str__(self) -> str:
        """Строковое представление."""
        status = "на земле" if self.on_ground else "в воздухе"
        lon_str = self._decimal_to_dms(self.longitude, is_latitude=False) if self.longitude is not None else "N/A"
        lat_str = self._decimal_to_dms(self.latitude, is_latitude=True) if self.latitude is not None else "N/A"

        return (
            f"ICAO24 {self.icao24 or 'N/A':<8} | "
            f"Рейс {self.callsign or 'N/A':<8} | "
            f"Страна: {self.origin_country:<30} | "
            f"Координаты : {lat_str:<11} / {lon_str:<11} | "
            f"Высота: {self.altitude:5.0f} м | "
            f"Скорость: {self.velocity:4.0f} м/с | "
            f"Статус: {status}"
        )

    @staticmethod
    def cast_to_object_list(data: list[list[Optional[Any]]]) -> list[Aeroplane]:
        """
        Преобразует сырой список состояний от OpenSky API в список объектов Aeroplane.

        Ожидается структура вложенных списков, где каждый внутренний список соответствует одному
        воздушному судну и содержит как минимум 10 элементов:
        [icao24, callsign, origin_country, time_position, last_contact, longitude, latitude,
         baro_altitude, on_ground, velocity, ...]

        Для отсутствующих числовых значений (None) используется 0.0, для строковых — пустая строка.

        Args:
            data: Список списков, полученный из API.

        Returns:
            Список экземпляров Aeroplane.
        """
        aeroplanes = []
        if not isinstance(data, list):
            raise TypeError("data должен быть списком.")
        for state in data:
            try:
                # Извлечение полей с безопасной заменой None
                icao = state[Aeroplane._STATE_ICAO24] or ""
                callsign = (state[Aeroplane._STATE_CALLSIGN] or "").strip()
                country = state[Aeroplane._STATE_ORIGIN_COUNTRY] or ""
                lon = state[Aeroplane._STATE_LONGITUDE]
                lat = state[Aeroplane._STATE_LATITUDE]
                alt_val = state[Aeroplane._STATE_BARO_ALTITUDE]
                alt = float(alt_val) if alt_val is not None else 0.0
                vel_val = state[Aeroplane._STATE_VELOCITY]
                vel = float(vel_val) if vel_val is not None else 0.0
                on_ground = bool(state[Aeroplane._STATE_ON_GROUND])

                aeroplanes.append(
                    Aeroplane(
                        icao24=icao,
                        callsign=callsign,
                        origin_country=country,
                        longitude=lon,
                        latitude=lat,
                        altitude=alt,
                        velocity=vel,
                        on_ground=on_ground,
                    )
                )
            except (IndexError, ValueError, AttributeError) as e:
                # Логирование и пропуск некорректной записи
                logger.warning(f"Пропущена некорректная запись самолёта: {state[:9]}... Ошибка: {e}")
                continue
            except TypeError as e:
                # Логирование и пропуск некорректной записи
                logger.warning(f"Пропущена некорректная запись самолёта: Ошибка: {e}")
                continue
        return aeroplanes

    def to_dict(self) -> dict:
        """Сериализация в словарь."""
        return {
            "icao24": self.icao24,
            "callsign": self.callsign,
            "origin_country": self.origin_country,
            "longitude": self.longitude,
            "latitude": self.latitude,
            "altitude": self.altitude,
            "velocity": self.velocity,
            "on_ground": self.on_ground,
        }

    @staticmethod
    def from_dict(data: dict) -> Aeroplane:
        """Десериализация из словаря."""
        return Aeroplane(
            icao24=data["icao24"],
            callsign=data.get("callsign", ""),
            origin_country=data.get("origin_country", ""),
            longitude=data.get("longitude"),
            latitude=data.get("latitude"),
            altitude=float(data.get("altitude", 0.0)),
            velocity=float(data.get("velocity", 0.0)),
            on_ground=bool(data.get("on_ground", False)),
        )

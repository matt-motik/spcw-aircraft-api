"""Модуль класса, моделирующего данные самолёта."""
from functools import total_ordering
from typing import Optional, Any


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
        self.icao24 = icao24
        self.callsign = callsign
        self.origin_country = origin_country
        self.longitude = longitude
        self.latitude = latitude
        self.altitude = altitude
        self.velocity = velocity
        self.on_ground = on_ground

    @property
    def icao24(self) -> str:
        """Геттер. Уникальный идентификатор борта (транспондера)."""
        return self._icao24

    @icao24.setter
    def icao24(self, value: str) -> None:
        """Сеттер. Уникальный идентификатор борта (транспондера)."""
        if not isinstance(value, str):
            raise TypeError("icao24 должен быть строкой.")
        clean = value.strip()
        if len(clean) != 6:
            raise ValueError("icao24 должен содержать ровно 6 символов.")
        try:
            int(clean, 16)  # проверка на hex
        except ValueError:
            raise ValueError("icao24 должен быть шестнадцатеричной строкой (0-9, a-f, A-F).")
        self._icao24 = clean.upper()

    @property
    def callsign(self) -> str :
        """Позывной рейса."""
        return self._callsign

    @callsign.setter
    def callsign(self, value: str) -> None:
        """Сеттер. Позывной рейса."""
        if not isinstance(value, str):
            raise TypeError("callsign должен быть строкой.")
        clean = value.strip()
        if len(clean) > 8:
            raise ValueError("callsign должен содержать не более 8 символов.")
        self._callsign = clean.upper()

    @property
    def origin_country(self) -> str:
        """Страна регистрации."""
        return self._origin_country

    @origin_country.setter
    def origin_country(self, value: str) -> None:
        """Сеттер. Страна регистрации."""
        if not isinstance(value, str):
            raise TypeError("origin_country должен быть строкой.")
        clean = value.strip()
        self._origin_country = clean.upper()

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
            raise TypeError("longitude должен быть числом.")
        if not (-180 <= value <= 180):
            raise ValueError("Значение longitude должно быть от -180 до 180")
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
            raise TypeError("latitude должен быть числом.")
        if not (-90 <= value <= 90):
            raise ValueError("Значение latitude должно быть от -90 до 90")
        self._latitude = value

    @property
    def altitude(self) -> float:
        """Барометрическая высота, м."""
        return self._altitude

    @altitude.setter
    def altitude(self, value: float) -> None:
        """Сеттер. Барометрическая высота, м."""
        if not isinstance(value, (float, int)):
            raise TypeError("altitude должен быть числом.")
        self._altitude = value

    @property
    def velocity(self) -> float:
        """Скорость относительно земли, м/с."""
        return self._velocity

    @velocity.setter
    def velocity(self, value: float) -> None:
        """Сеттер. Скорость относительно земли, м/с."""
        if not isinstance(value, (float, int)):
            raise TypeError("velocity должен быть числом.")
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
            raise TypeError("on_ground должен быть булевым значением.")
        self._on_ground = value

    # ---------- методы сравнения ----------
    def __eq__(self, other: object) -> bool:
        """
        Сравнение самолётов по (высота, скорость).

        Сравнивает по кортежу (altitude, velocity). Если other не Aeroplane, вызывает TypeError.
        """
        if not isinstance(other, Aeroplane):
            # raise TypeError("other должен быть типа Aeroplane.")
            return NotImplemented
        return (self.altitude, self.velocity) == (other.altitude, other.velocity)

    def __lt__(self, other: object) -> bool:
        """
        Меньше — значит ниже (или медленнее при равной высоте).
        """
        if not isinstance(other, Aeroplane):
            # raise TypeError("other должен быть типа Aeroplane.")
            return NotImplemented
        return (self.altitude, self.velocity) < (other.altitude, other.velocity)

    # ---------- строковое представление ----------
    def __repr__(self) -> str:
        return (
            f"Aeroplane(icao24={self.icao24!r}, callsign={self.callsign!r}, "
            f"origin_country={self.origin_country!r}, longitude={self.longitude}, "
            f"latitude={self.latitude}, altitude={self.altitude}, "
            f"velocity={self.velocity}, on_ground={self.on_ground})"
        )

    # ---------- фабричный метод ----------
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
            except (IndexError, ValueError) as e:
                # Логирование или пропуск некорректной записи
                # Можно добавить logger.warning(...)
                continue
        return aeroplanes

"""Модуль класса для работы с PostgreSQL."""

from typing import Any

import psycopg2
from psycopg2.extras import RealDictCursor

from .aeroplane import Aeroplane
from .base_storage import BaseStorage
from .config_reader import get_db_config
from .logger_creator import create_logger

logger = create_logger(__name__)


class DBManager(BaseStorage):
    """
    Класс для работы с данными в PostgreSQL.

    Подключается к БД, создаёт таблицы, выполняет запросы.
    Использует библиотеку psycopg2.
    """

    def __init__(self, config_file: str = "database.ini") -> None:
        """
        Инициализация менеджера БД.

        Args:
            config_file: Путь к конфигу с параметрами подключения.
        """
        self._config = get_db_config(config_file)
        self._connection = None

    @property
    def connection(self) -> psycopg2.extensions.connection:
        """Ленивое создание соединения."""
        if self._connection is None or self._connection.closed:
            self._connection = psycopg2.connect(**self._config)
            logger.debug("Соединение с БД установлено")
        return self._connection

    def initialize(self) -> None:
        """Подготовка хранилища — создание таблиц."""
        self.create_tables()

    def create_tables(self) -> None:
        """Создаёт таблицы countries и aeroplanes."""
        with self.connection.cursor() as cur:
            cur.execute("""
                        CREATE TABLE IF NOT EXISTS countries (
                            id SERIAL PRIMARY KEY,
                            name VARCHAR(100) NOT NULL UNIQUE,
                            lat_min FLOAT,
                            lat_max FLOAT,
                            lon_min FLOAT,
                            lon_max FLOAT
                        );
                    """)

        with self.connection.cursor() as cur:
            cur.execute("""
                        CREATE TABLE IF NOT EXISTS aeroplanes (
                            id SERIAL PRIMARY KEY,
                            icao24 VARCHAR(6) NOT NULL UNIQUE,
                            callsign VARCHAR(8),
                            origin_country VARCHAR(100),
                            longitude FLOAT,
                            latitude FLOAT,
                            altitude FLOAT,
                            velocity FLOAT,
                            on_ground BOOLEAN,
                            country_id INTEGER REFERENCES countries(id)
                        );
                    """)
        self.connection.commit()
        logger.info("Таблицы проверены и готовы")

    # === Методы для заполнения данных ===

    def insert_country(self, name: str, lat_min: float, lat_max: float, lon_min: float, lon_max: float) -> int:
        """
        Добавляет страну в таблицу.

        Returns:
            id созданной записи.
        """
        with self.connection.cursor() as cur:
            cur.execute(
                """
                INSERT INTO countries (name, lat_min, lat_max, lon_min, lon_max)
                VALUES (%s, %s, %s, %s, %s)
                ON CONFLICT (name) DO NOTHING
                RETURNING id;
            """,
                (name, lat_min, lat_max, lon_min, lon_max),
            )
            result = cur.fetchone()
            if result is None:
                cur.execute("SELECT id FROM countries WHERE name = %s", (name,))
                result = cur.fetchone()
            country_id = int(result[0])
            self.connection.commit()
            return country_id

    def add_country(self, country_name: str, bbox: dict[str, float]) -> int | None:
        """
        Добавляет страну в хранилище.

        Returns:
            id страны или None, если хранилище не поддерживает страны.
        """
        return self.insert_country(
            name=country_name,
            lat_min=bbox["lamin"],
            lat_max=bbox["lamax"],
            lon_min=bbox["lomin"],
            lon_max=bbox["lomax"],
        )

    def insert_aeroplane(
        self,
        icao24: str,
        callsign: str,
        origin_country: str,
        longitude: float | None,
        latitude: float | None,
        altitude: float,
        velocity: float,
        on_ground: bool,
        country_id: int | None = None,
    ) -> None:
        """Добавляет самолёт в таблицу."""
        with self.connection.cursor() as cur:
            cur.execute(
                """
                INSERT INTO aeroplanes (icao24, callsign, origin_country, longitude, latitude,
                                        altitude, velocity, on_ground, country_id)
                VALUES (%s, %s, %s, %s, %s, %s, %s, %s, %s)
                ON CONFLICT (icao24) DO UPDATE SET
                    callsign = EXCLUDED.callsign,
                    origin_country = EXCLUDED.origin_country,
                    longitude = EXCLUDED.longitude,
                    latitude = EXCLUDED.latitude,
                    altitude = EXCLUDED.altitude,
                    velocity = EXCLUDED.velocity,
                    on_ground = EXCLUDED.on_ground,
                    country_id = EXCLUDED.country_id
            """,
                (icao24, callsign, origin_country, longitude, latitude, altitude, velocity, on_ground, country_id),
            )

    def add_aeroplane(self, aeroplane: Aeroplane) -> None:
        """Добавляет один самолёт в БД."""
        self.insert_aeroplane(
            icao24=aeroplane.icao24,
            callsign=aeroplane.callsign,
            origin_country=aeroplane.origin_country,
            longitude=aeroplane.longitude,
            latitude=aeroplane.latitude,
            altitude=aeroplane.altitude,
            velocity=aeroplane.velocity,
            on_ground=aeroplane.on_ground,
            country_id=aeroplane.country_id,
        )
        self.connection.commit()

    def add_multiple_aeroplanes(self, aeroplanes: list[Aeroplane]) -> None:
        """
        Пакетное добавление/обновление списка самолётов с однократным сохранением.

        Args:
            aeroplanes: Список объектов Aeroplane.

        Raises:
            TypeError: Если передан объект не типа List[Aeroplane].
        """
        for aeroplane in aeroplanes:
            self.insert_aeroplane(
                icao24=aeroplane.icao24,
                callsign=aeroplane.callsign,
                origin_country=aeroplane.origin_country,
                longitude=aeroplane.longitude,
                latitude=aeroplane.latitude,
                altitude=aeroplane.altitude,
                velocity=aeroplane.velocity,
                on_ground=aeroplane.on_ground,
                country_id=aeroplane.country_id,
            )
        self.connection.commit()

    def delete_aeroplane(self, aeroplane: Aeroplane) -> None:
        """Удаляет самолёт из БД по icao24."""
        with self.connection.cursor() as cur:
            cur.execute("DELETE FROM aeroplanes WHERE icao24 = %s", (aeroplane.icao24,))
            self.connection.commit()

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
            "country_id",
            "callsign",
        }
        for key in filters:
            if key not in valid_keys:
                raise ValueError(f"Некорректный фильтр: {key}")

        conditions = []
        params = []

        if "origin_country" in filters:
            conditions.append("UPPER(origin_country) = UPPER(%s)")
            params.append(filters["origin_country"].strip().upper())

        if "min_altitude" in filters:
            conditions.append("altitude >= %s")
            params.append(float(filters["min_altitude"]))

        if "max_altitude" in filters:
            conditions.append("altitude <= %s")
            params.append(float(filters["max_altitude"]))

        if "min_velocity" in filters:
            conditions.append("velocity >= %s")
            params.append(float(filters["min_velocity"]))

        if "max_velocity" in filters:
            conditions.append("velocity <= %s")
            params.append(float(filters["max_velocity"]))

        if "on_ground" in filters:
            conditions.append("on_ground = %s")
            params.append(bool(filters["on_ground"]))

        if "min_latitude" in filters:
            conditions.append("latitude >= %s")
            params.append(float(filters["min_latitude"]))

        if "max_latitude" in filters:
            conditions.append("latitude <= %s")
            params.append(float(filters["max_latitude"]))

        if "min_longitude" in filters:
            conditions.append("longitude >= %s")
            params.append(float(filters["min_longitude"]))

        if "max_longitude" in filters:
            conditions.append("longitude <= %s")
            params.append(float(filters["max_longitude"]))

        if "country_id" in filters:
            conditions.append("country_id = %s")
            params.append(int(filters["country_id"]))

        if "callsign" in filters:
            conditions.append("UPPER(callsign) LIKE UPPER(%s)")
            params.append(f"%{filters['callsign']}%")

        # Собираем запрос
        sql = (
            "SELECT icao24, callsign, origin_country, longitude, latitude, altitude, "
            "velocity, on_ground, country_id FROM aeroplanes"
        )
        if conditions:
            sql += " WHERE " + " AND ".join(conditions)

        with self.connection.cursor(cursor_factory=RealDictCursor) as cur:
            cur.execute(sql, params)
            rows = cur.fetchall()

        # Преобразуем rows в list[Aeroplane]
        return [Aeroplane(**row) for row in rows]

    # === Методы задания ===

    def get_countries_and_aeroplanes_count(self) -> list[dict]:
        """Получает список всех стран и количество самолётов в их воздушных пространствах."""
        with self.connection.cursor(cursor_factory=RealDictCursor) as cur:
            cur.execute("""
                SELECT
                    c.name,
                    COUNT(a.id) as aeroplanes_count
                FROM countries c
                LEFT JOIN aeroplanes a ON c.id = a.country_id
                GROUP BY c.id, c.name
                ORDER BY aeroplanes_count DESC
            """)
            rows = cur.fetchall()

        return [dict(row) for row in rows]

    def get_all_aeroplanes(self) -> list[Aeroplane]:
        """Получает список всех воздушных судов."""
        with self.connection.cursor(cursor_factory=RealDictCursor) as cur:
            sql = (
                "SELECT icao24, callsign, origin_country, longitude, latitude, altitude, "
                "velocity, on_ground, country_id FROM aeroplanes"
            )
            cur.execute(sql)
            rows = cur.fetchall()

        return [Aeroplane(**row) for row in rows]

    def get_avg_speed(self) -> float:
        """Получает среднюю скорость по самолётам."""
        with self.connection.cursor() as cur:
            cur.execute("SELECT AVG(velocity) FROM aeroplanes")
            result = cur.fetchone()
            return float(result[0]) if result[0] is not None else 0.0

    def get_aeroplanes_with_higher_speed(self, limit: int = 5) -> list[Aeroplane]:
        """Получает топ-N самолётов со скоростью выше средней.

        Args:
            limit: Максимальное количество возвращаемых самолетов (по умолчанию 5).
                   Если limit <= 0, возвращает пустой список.

        Returns:
            Список самых быстрых самолетов, отсортированных по убыванию скорости.

        Example:
            >>> db = DBManager()
            >>> fast_planes = db.get_aeroplanes_with_higher_speed(10)
            >>> for plane in fast_planes:
            ...     print(f"{plane.callsign}: {plane.velocity:.1f} м/с")
        """
        if limit <= 0:
            return []

        with self.connection.cursor(cursor_factory=RealDictCursor) as cur:
            cur.execute(
                """
                SELECT icao24, callsign, origin_country, longitude, latitude,
                       altitude, velocity, on_ground, country_id
                FROM aeroplanes
                WHERE velocity > COALESCE((SELECT AVG(velocity) FROM aeroplanes), 0)
                ORDER BY velocity DESC
                LIMIT %s
            """,
                (limit,),
            )
            rows = cur.fetchall()
            return [Aeroplane(**row) for row in rows]

    def get_aeroplanes_with_keyword(self, keyword: str) -> list[Aeroplane]:
        """
        Получает самолёты, в позывном которых содержится keyword.

        Args:
            keyword: Подстрока для поиска (например, 'ACA').
        """
        if not keyword or not keyword.strip():
            return []
        return self.get_aeroplanes(callsign=keyword.strip())

    def close(self) -> None:
        """Закрывает соединение с БД."""
        if self._connection is not None and not self._connection.closed:
            self._connection.close()
            logger.debug("Соединение с БД закрыто")
        self._connection = None

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
        with self.connection.cursor(cursor_factory=RealDictCursor) as cur:
            cur.execute(
                "SELECT id, lat_min, lat_max, lon_min, lon_max FROM countries WHERE name = %s", (country_name,)
            )
            result = cur.fetchone()
            return dict(result) if result else None

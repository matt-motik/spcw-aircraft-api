"""Тесты для модуля db_manager."""
from unittest.mock import MagicMock, patch

import pytest
from src.aeroplane import Aeroplane
from src.db_manager import DBManager


class TestDBManager:
    """Тесты для DBManager."""

    def setup_method(self):
        """Подготовка перед каждым тестом."""
        self.config = {
            "host": "localhost",
            "database": "test_db",
            "user": "test_user",
            "password": "test_pass",
            "port": "5432"
        }

    @patch('src.db_manager.psycopg2.connect')
    def test_connection_lazy_creation(self, mock_connect):
        """Тест ленивого создания соединения."""
        mock_connect.return_value = MagicMock()

        db = DBManager()
        # connection еще не создано
        mock_connect.assert_not_called()

        # При обращении создается
        _ = db.connection
        mock_connect.assert_called_once()

    @patch('src.db_manager.psycopg2.connect')
    def test_create_tables(self, mock_connect):
        """Тест создания таблиц."""
        mock_conn = MagicMock()
        mock_cursor = MagicMock()
        mock_conn.cursor.return_value.__enter__.return_value = mock_cursor
        mock_connect.return_value = mock_conn

        db = DBManager()
        db.create_tables()

        # Проверяем вызовы CREATE TABLE
        create_calls = [call for call in mock_cursor.execute.call_args_list
                        if "CREATE TABLE" in str(call)]
        assert len(create_calls) >= 2  # countries и aeroplanes
        mock_conn.commit.assert_called()

    @patch('src.db_manager.psycopg2.connect')
    def test_insert_country(self, mock_connect):
        """Тест вставки страны."""
        mock_conn = MagicMock()
        mock_cursor = MagicMock()
        mock_cursor.fetchone.return_value = [1]  # возвращаем id
        mock_conn.cursor.return_value.__enter__.return_value = mock_cursor
        mock_connect.return_value = mock_conn

        db = DBManager()
        country_id = db.insert_country("Test Country", -90, 90, -180, 180)

        assert country_id == 1
        mock_conn.commit.assert_called()

    @patch('src.db_manager.psycopg2.connect')
    def test_add_country(self, mock_connect):
        """Тест добавления страны."""
        mock_conn = MagicMock()
        mock_cursor = MagicMock()
        mock_cursor.fetchone.return_value = [1]
        mock_conn.cursor.return_value.__enter__.return_value = mock_cursor
        mock_connect.return_value = mock_conn

        db = DBManager()
        bbox = {"lamin": -90, "lamax": 90, "lomin": -180, "lomax": 180}
        country_id = db.add_country("Test Country", bbox)

        assert country_id == 1

    @patch('src.db_manager.psycopg2.connect')
    def test_insert_aeroplane(self, mock_connect):
        """Тест вставки самолета."""
        mock_conn = MagicMock()
        mock_cursor = MagicMock()
        mock_conn.cursor.return_value.__enter__.return_value = mock_cursor
        mock_connect.return_value = mock_conn

        db = DBManager()
        db.insert_aeroplane(
            icao24="ABC123",
            callsign="TEST123",
            origin_country="Russia",
            longitude=30.0,
            latitude=60.0,
            altitude=10000.0,
            velocity=200.0,
            on_ground=False,
            country_id=1
        )

        # Проверяем, что INSERT выполнен
        mock_cursor.execute.assert_called_once()
        sql = mock_cursor.execute.call_args[0][0]
        assert "INSERT INTO aeroplanes" in sql

    @patch('src.db_manager.psycopg2.connect')
    def test_add_aeroplane(self, mock_connect):
        """Тест добавления самолета."""
        mock_conn = MagicMock()
        mock_cursor = MagicMock()
        mock_conn.cursor.return_value.__enter__.return_value = mock_cursor
        mock_connect.return_value = mock_conn

        db = DBManager()
        plane = Aeroplane(
            icao24="ABC123",
            callsign="TEST123",
            origin_country="Russia",
            longitude=30.0,
            latitude=60.0,
            altitude=10000.0,
            velocity=200.0,
            on_ground=False,
            country_id=1
        )
        db.add_aeroplane(plane)

        mock_cursor.execute.assert_called_once()
        mock_conn.commit.assert_called()

    @patch('src.db_manager.psycopg2.connect')
    def test_get_all_aeroplanes(self, mock_connect):
        """Тест получения всех самолетов."""
        mock_conn = MagicMock()
        mock_cursor = MagicMock()
        mock_cursor.fetchall.return_value = [
            {"icao24": "ABC123", "callsign": "TEST123", "origin_country": "Russia",
             "longitude": 30.0, "latitude": 60.0, "altitude": 10000.0,
             "velocity": 200.0, "on_ground": False, "country_id": 1}
        ]
        mock_conn.cursor.return_value.__enter__.return_value = mock_cursor
        mock_connect.return_value = mock_conn

        db = DBManager()
        planes = db.get_all_aeroplanes()

        assert len(planes) == 1
        assert planes[0].icao24 == "ABC123"

    @patch('src.db_manager.psycopg2.connect')
    def test_get_avg_speed(self, mock_connect):
        """Тест получения средней скорости."""
        mock_conn = MagicMock()
        mock_cursor = MagicMock()
        mock_cursor.fetchone.return_value = [250.5]
        mock_conn.cursor.return_value.__enter__.return_value = mock_cursor
        mock_connect.return_value = mock_conn

        db = DBManager()
        avg_speed = db.get_avg_speed()

        assert avg_speed == 250.5

    @patch('src.db_manager.psycopg2.connect')
    def test_get_aeroplanes_with_higher_speed(self, mock_connect):
        """Тест получения самолетов со скоростью выше средней."""
        mock_conn = MagicMock()
        mock_cursor = MagicMock()
        mock_cursor.fetchall.return_value = [
            {"icao24": "ABC123", "callsign": "TEST123", "origin_country": "Russia",
             "longitude": 30.0, "latitude": 60.0, "altitude": 10000.0,
             "velocity": 300.0, "on_ground": False, "country_id": 1}
        ]
        mock_conn.cursor.return_value.__enter__.return_value = mock_cursor
        mock_connect.return_value = mock_conn

        db = DBManager()
        planes = db.get_aeroplanes_with_higher_speed(limit=5)

        assert len(planes) == 1
        assert planes[0].velocity == 300.0

    @patch('src.db_manager.psycopg2.connect')
    def test_get_aeroplanes_with_keyword(self, mock_connect):
        """Тест поиска самолетов по позывному."""
        mock_conn = MagicMock()
        mock_cursor = MagicMock()
        mock_cursor.fetchall.return_value = [
            {"icao24": "ABC123", "callsign": "AAL123", "origin_country": "USA",
             "longitude": 30.0, "latitude": 60.0, "altitude": 10000.0,
             "velocity": 200.0, "on_ground": False, "country_id": 1}
        ]
        mock_conn.cursor.return_value.__enter__.return_value = mock_cursor
        mock_connect.return_value = mock_conn

        db = DBManager()
        planes = db.get_aeroplanes_with_keyword("AAL")

        assert len(planes) == 1
        assert "AAL" in planes[0].callsign

    @patch('src.db_manager.psycopg2.connect')
    def test_get_country(self, mock_connect):
        """Тест получения страны."""
        mock_conn = MagicMock()
        mock_cursor = MagicMock()
        mock_cursor.fetchone.return_value = {"id": 1, "lat_min": -90, "lat_max": 90,
                                             "lon_min": -180, "lon_max": 180}
        mock_conn.cursor.return_value.__enter__.return_value = mock_cursor
        mock_connect.return_value = mock_conn

        db = DBManager()
        country = db.get_country("Russia")

        assert country["id"] == 1
        assert country["lat_min"] == -90

    @patch('src.db_manager.psycopg2.connect')
    def test_delete_aeroplane(self, mock_connect):
        """Тест удаления самолета."""
        mock_conn = MagicMock()
        mock_cursor = MagicMock()
        mock_conn.cursor.return_value.__enter__.return_value = mock_cursor
        mock_connect.return_value = mock_conn

        db = DBManager()
        plane = Aeroplane(
            icao24="ABC123",
            callsign="TEST123",
            origin_country="Russia",
            longitude=30.0,
            latitude=60.0,
            altitude=10000.0,
            velocity=200.0,
            on_ground=False,
            country_id=1
        )
        db.delete_aeroplane(plane)

        mock_cursor.execute.assert_called_once()
        sql = mock_cursor.execute.call_args[0][0]
        assert "DELETE FROM aeroplanes" in sql


class TestDBManagerAdditional:
    """Дополнительные тесты для DBManager."""

    def setup_method(self):
        """Подготовка перед каждым тестом."""
        self.config = {
            "host": "localhost",
            "database": "test_db",
            "user": "test_user",
            "password": "test_pass",
            "port": "5432"
        }

    @patch('src.db_manager.psycopg2.connect')
    def test_connection_property_reuses_existing(self, mock_connect):
        """Тест повторного использования соединения."""
        mock_conn = MagicMock()
        mock_conn.closed = False
        mock_connect.return_value = mock_conn

        db = DBManager()
        conn1 = db.connection
        conn2 = db.connection

        # Соединение создано только один раз
        mock_connect.assert_called_once()
        assert conn1 is conn2

    @patch('src.db_manager.psycopg2.connect')
    def test_connection_recreates_if_closed(self, mock_connect):
        """Тест пересоздания закрытого соединения."""
        mock_conn = MagicMock()
        mock_connect.return_value = mock_conn

        db = DBManager()

        # Первый вызов - создаем соединение
        conn1 = db.connection
        assert mock_connect.call_count == 1
        assert conn1 is mock_conn

        # Закрываем соединение вручную (симулируем)
        db._connection.closed = True

        # Второй вызов - соединение закрыто, пересоздаем
        mock_connect.return_value = MagicMock()
        conn2 = db.connection
        assert mock_connect.call_count == 2
        assert conn2 is not conn1

    @patch('src.db_manager.psycopg2.connect')
    def test_insert_aeroplane_without_country(self, mock_connect):
        """Тест вставки самолета без country_id."""
        mock_conn = MagicMock()
        mock_cursor = MagicMock()
        mock_conn.cursor.return_value.__enter__.return_value = mock_cursor
        mock_connect.return_value = mock_conn

        db = DBManager()
        db.insert_aeroplane(
            icao24="ABC123",
            callsign="TEST123",
            origin_country="Russia",
            longitude=30.0,
            latitude=60.0,
            altitude=10000.0,
            velocity=200.0,
            on_ground=False,
            country_id=None  # Без страны
        )

        mock_cursor.execute.assert_called_once()
        sql = mock_cursor.execute.call_args[0][0]
        assert "country_id" in sql

    @patch('src.db_manager.psycopg2.connect')
    def test_get_aeroplanes_with_invalid_filter(self, mock_connect):
        """Тест ошибки при некорректном фильтре."""
        mock_connect.return_value = MagicMock()

        db = DBManager()

        with pytest.raises(ValueError, match="Некорректный фильтр: invalid_filter"):
            db.get_aeroplanes(invalid_filter="test")

    @patch('src.db_manager.psycopg2.connect')
    def test_get_aeroplanes_with_all_filters(self, mock_connect):
        """Тест применения всех фильтров одновременно."""
        mock_conn = MagicMock()
        mock_cursor = MagicMock()
        mock_cursor.fetchall.return_value = []
        mock_conn.cursor.return_value.__enter__.return_value = mock_cursor
        mock_connect.return_value = mock_conn

        db = DBManager()
        db.get_aeroplanes(
            origin_country="Russia",
            min_altitude=1000,
            max_altitude=20000,
            min_velocity=100,
            max_velocity=500,
            on_ground=False,
            min_latitude=40,
            max_latitude=70,
            min_longitude=20,
            max_longitude=80,
            country_id=1,
            callsign="AAL"
        )

        # Проверяем, что запрос был выполнен с параметрами
        mock_cursor.execute.assert_called_once()
        sql = mock_cursor.execute.call_args[0][0]
        # Проверяем наличие всех условий в запросе
        assert "origin_country" in sql.upper() or "UPPER(origin_country)" in sql
        assert "altitude" in sql

    @patch('src.db_manager.psycopg2.connect')
    def test_add_multiple_aeroplanes_with_invalid_type(self, mock_connect):
        """Тест ошибки при добавлении не списка."""
        mock_connect.return_value = MagicMock()

        db = DBManager()

        with pytest.raises(TypeError, match="aeroplanes должен быть списком"):
            db.add_multiple_aeroplanes("not a list")  # type: ignore

    @patch('src.db_manager.psycopg2.connect')
    def test_get_countries_and_aeroplanes_count_empty(self, mock_connect):
        """Тест получения статистики когда нет данных."""
        mock_conn = MagicMock()
        mock_cursor = MagicMock()
        mock_cursor.fetchall.return_value = []
        mock_conn.cursor.return_value.__enter__.return_value = mock_cursor
        mock_connect.return_value = mock_conn

        db = DBManager()
        result = db.get_countries_and_aeroplanes_count()

        assert result == []
        mock_cursor.execute.assert_called_once()

    @patch('src.db_manager.psycopg2.connect')
    def test_get_all_aeroplanes_empty(self, mock_connect):
        """Тест получения пустого списка самолетов."""
        mock_conn = MagicMock()
        mock_cursor = MagicMock()
        mock_cursor.fetchall.return_value = []
        mock_conn.cursor.return_value.__enter__.return_value = mock_cursor
        mock_connect.return_value = mock_conn

        db = DBManager()
        planes = db.get_all_aeroplanes()

        assert planes == []
        mock_cursor.execute.assert_called_once()

    @patch('src.db_manager.psycopg2.connect')
    def test_get_avg_speed_no_data(self, mock_connect):
        """Тест получения средней скорости когда нет данных."""
        mock_conn = MagicMock()
        mock_cursor = MagicMock()
        mock_cursor.fetchone.return_value = [None]  # NULL в БД
        mock_conn.cursor.return_value.__enter__.return_value = mock_cursor
        mock_connect.return_value = mock_conn

        db = DBManager()
        avg_speed = db.get_avg_speed()

        assert avg_speed == 0.0

    @patch('src.db_manager.psycopg2.connect')
    def test_get_aeroplanes_with_higher_speed_limit_zero(self, mock_connect):
        """Тест получения самолетов с лимитом <= 0."""
        mock_connect.return_value = MagicMock()

        db = DBManager()
        planes = db.get_aeroplanes_with_higher_speed(limit=0)

        assert planes == []

        # Проверяем, что SQL не выполнялся
        mock_connect.return_value.cursor.assert_not_called()

    @patch('src.db_manager.psycopg2.connect')
    def test_get_aeroplanes_with_higher_speed_no_data(self, mock_connect):
        """Тест получения самолетов со скоростью выше средней когда нет данных."""
        mock_conn = MagicMock()
        mock_cursor = MagicMock()
        mock_cursor.fetchall.return_value = []
        mock_conn.cursor.return_value.__enter__.return_value = mock_cursor
        mock_connect.return_value = mock_conn

        db = DBManager()
        planes = db.get_aeroplanes_with_higher_speed(limit=5)

        assert planes == []
        mock_cursor.execute.assert_called_once()

    @patch('src.db_manager.psycopg2.connect')
    def test_get_country_not_found(self, mock_connect):
        """Тест получения несуществующей страны."""
        mock_conn = MagicMock()
        mock_cursor = MagicMock()
        mock_cursor.fetchone.return_value = None
        mock_conn.cursor.return_value.__enter__.return_value = mock_cursor
        mock_connect.return_value = mock_conn

        db = DBManager()
        country = db.get_country("NonExistent")

        assert country is None

    @patch('src.db_manager.psycopg2.connect')
    def test_close_connection(self, mock_connect):
        """Тест закрытия соединения."""
        mock_conn = MagicMock()
        mock_conn.closed = False
        mock_connect.return_value = mock_conn

        db = DBManager()
        # Создаем соединение
        _ = db.connection

        db.close()

        mock_conn.close.assert_called_once()
        assert db._connection is None

    @patch('src.db_manager.psycopg2.connect')
    def test_close_already_closed(self, mock_connect):
        """Тест закрытия уже закрытого соединения."""
        mock_conn = MagicMock()
        mock_conn.closed = True
        mock_connect.return_value = mock_conn

        db = DBManager()
        # Создаем соединение
        _ = db.connection

        db.close()

        # close не вызывается, так как соединение уже закрыто
        mock_conn.close.assert_not_called()
        assert db._connection is None

    @patch('src.db_manager.psycopg2.connect')
    def test_get_aeroplanes_with_callsign_filter(self, mock_connect):
        """Тест фильтрации по позывному."""
        mock_conn = MagicMock()
        mock_cursor = MagicMock()
        mock_cursor.fetchall.return_value = [
            {"icao24": "ABC123", "callsign": "AAL123", "origin_country": "USA",
             "longitude": 30.0, "latitude": 60.0, "altitude": 10000.0,
             "velocity": 200.0, "on_ground": False, "country_id": 1}
        ]
        mock_conn.cursor.return_value.__enter__.return_value = mock_cursor
        mock_connect.return_value = mock_conn

        db = DBManager()
        planes = db.get_aeroplanes(callsign="AAL")

        assert len(planes) == 1
        assert planes[0].callsign == "AAL123"

        # Проверяем, что в запросе есть LIKE
        sql = mock_cursor.execute.call_args[0][0]
        assert "LIKE" in sql.upper()
        params = mock_cursor.execute.call_args[0][1]
        assert "%AAL%" in params

    @patch('src.db_manager.psycopg2.connect')
    def test_insert_country_existing(self, mock_connect):
        """Тест вставки уже существующей страны."""
        mock_conn = MagicMock()
        mock_cursor = MagicMock()
        # Первый запрос (INSERT) возвращает None (ON CONFLICT DO NOTHING)
        mock_cursor.fetchone.side_effect = [None, [5]]  # потом SELECT возвращает id=5
        mock_conn.cursor.return_value.__enter__.return_value = mock_cursor
        mock_connect.return_value = mock_conn

        db = DBManager()
        country_id = db.insert_country("Existing Country", -90, 90, -180, 180)

        assert country_id == 5
        # Проверяем, что был выполнен SELECT после INSERT
        assert mock_cursor.execute.call_count == 2
        sql_first = mock_cursor.execute.call_args_list[0][0][0]
        sql_second = mock_cursor.execute.call_args_list[1][0][0]
        assert "INSERT" in sql_first.upper()
        assert "SELECT" in sql_second.upper()
        mock_conn.commit.assert_called()

    @patch('src.db_manager.psycopg2.connect')
    def test_add_multiple_aeroplanes_valid(self, mock_connect):
        """Тест успешного добавления нескольких самолетов."""
        mock_conn = MagicMock()
        mock_cursor = MagicMock()
        mock_conn.cursor.return_value.__enter__.return_value = mock_cursor
        mock_connect.return_value = mock_conn

        db = DBManager()

        planes = [
            Aeroplane(
                icao24="ABC123",
                callsign="TEST1",
                origin_country="Russia",
                longitude=30.0,
                latitude=60.0,
                altitude=10000.0,
                velocity=200.0,
                on_ground=False,
                country_id=1
            ),
            Aeroplane(
                icao24="DEF456",
                callsign="TEST2",
                origin_country="Russia",
                longitude=40.0,
                latitude=50.0,
                altitude=8000.0,
                velocity=180.0,
                on_ground=False,
                country_id=1
            ),
        ]

        db.add_multiple_aeroplanes(planes)

        assert mock_cursor.execute.call_count == 2
        mock_conn.commit.assert_called_once()

    @patch('src.db_manager.psycopg2.connect')
    def test_add_multiple_aeroplanes_with_mixed_types(self, mock_connect):
        """Тест ошибки при смешанных типах в списке."""
        mock_connect.return_value = MagicMock()

        db = DBManager()

        plane = Aeroplane(
            icao24="ABC123",
            callsign="TEST",
            origin_country="Russia",
            longitude=30.0,
            latitude=60.0,
            altitude=10000.0,
            velocity=200.0,
            on_ground=False,
            country_id=1
        )

        with pytest.raises(TypeError, match="Все элементы списка должны быть типа Aeroplane"):
            db.add_multiple_aeroplanes([plane, "not a plane"])  # type: ignore

    @patch('src.db_manager.psycopg2.connect')
    def test_connection_creates_connection(self, mock_connect):
        """Тест создания соединения."""
        mock_conn = MagicMock()
        mock_conn.closed = False
        mock_connect.return_value = mock_conn

        db = DBManager()

        assert db._connection is None

        conn = db.connection

        assert conn is mock_conn
        mock_connect.assert_called_once()
        assert db._connection is mock_conn

    @patch('src.db_manager.psycopg2.connect')
    def test_initialize_calls_create_tables(self, mock_connect):
        """Тест что initialize вызывает create_tables."""
        mock_conn = MagicMock()
        mock_cursor = MagicMock()
        mock_conn.cursor.return_value.__enter__.return_value = mock_cursor
        mock_connect.return_value = mock_conn

        db = DBManager()
        db.initialize()

        # Проверяем, что CREATE TABLE вызывался (через create_tables)
        create_calls = [call for call in mock_cursor.execute.call_args_list
                        if "CREATE TABLE" in str(call)]
        assert len(create_calls) >= 2

    @patch('src.db_manager.psycopg2.connect')
    def test_get_aeroplanes_with_keyword_empty(self, mock_connect):
        """Тест поиска с пустым keyword."""
        mock_connect.return_value = MagicMock()

        db = DBManager()

        # Пустая строка
        planes = db.get_aeroplanes_with_keyword("")
        assert planes == []

        # Только пробелы
        planes = db.get_aeroplanes_with_keyword("   ")
        assert planes == []

        # None
        planes = db.get_aeroplanes_with_keyword(None)  # type: ignore
        assert planes == []
"""Тесты для модуля db_initializer."""

from unittest.mock import MagicMock
from unittest.mock import patch

import psycopg2
import pytest

from src.db_initializer import initialize_database


class TestDBInitializer:
    """Тесты для инициализации базы данных."""

    @patch("src.db_initializer.get_db_config")
    @patch("src.db_initializer.psycopg2.connect")
    def test_initialize_database_creates_db_and_user(self, mock_connect, mock_get_config):
        """Тест создания БД и пользователя."""
        # Настройка моков
        mock_get_config.side_effect = [
            {"host": "localhost", "port": "5432", "user": "postgres", "password": "admin"},
            {"database": "test_db", "user": "test_user", "password": "test_pass"},
        ]

        mock_conn = MagicMock()
        mock_cursor = MagicMock()
        mock_conn.cursor.return_value.__enter__.return_value = mock_cursor

        # База данных еще не существует
        mock_cursor.fetchone.side_effect = [None, None]  # DB не существует, пользователь не существует

        mock_connect.return_value = mock_conn

        initialize_database("admin.ini", "database.ini")

        # Проверяем, что autocommit = True
        assert mock_conn.autocommit is True

        # Проверяем вызовы SQL
        assert mock_cursor.execute.call_count >= 3  # SELECT, CREATE DATABASE, CREATE USER

        # Проверяем, что были созданы БД и пользователь
        execute_args = [str(call) for call in mock_cursor.execute.call_args_list]
        assert any("CREATE DATABASE" in str(arg) for arg in execute_args)
        assert any("CREATE USER" in str(arg) for arg in execute_args)

        # Проверяем, что было второе соединение для выдачи прав
        assert mock_connect.call_count == 2

    @patch("src.db_initializer.get_db_config")
    @patch("src.db_initializer.psycopg2.connect")
    def test_initialize_database_skips_existing(self, mock_connect, mock_get_config):
        """Тест пропуска существующих БД и пользователя."""
        mock_get_config.side_effect = [
            {"host": "localhost", "port": "5432", "user": "postgres", "password": "admin"},
            {"database": "test_db", "user": "test_user", "password": "test_pass"},
        ]

        mock_conn = MagicMock()
        mock_cursor = MagicMock()
        mock_conn.cursor.return_value.__enter__.return_value = mock_cursor

        # База данных и пользователь уже существуют
        mock_cursor.fetchone.side_effect = [[1], [1]]  # DB существует, пользователь существует

        mock_connect.return_value = mock_conn

        initialize_database("admin.ini", "database.ini")

        # Проверяем, что CREATE не вызывались
        execute_args = [str(call) for call in mock_cursor.execute.call_args_list]
        create_db_calls = [arg for arg in execute_args if "CREATE DATABASE" in str(arg)]
        create_user_calls = [arg for arg in execute_args if "CREATE USER" in str(arg)]

        assert len(create_db_calls) == 0
        assert len(create_user_calls) == 0

    @patch("src.db_initializer.get_db_config")
    def test_initialize_database_connection_error(self, mock_get_config):
        """Тест ошибки подключения к БД."""
        mock_get_config.side_effect = [
            {"host": "localhost", "port": "5432", "user": "postgres", "password": "wrong"},
            {"database": "test_db", "user": "test_user", "password": "test_pass"},
        ]

        with patch("src.db_initializer.psycopg2.connect") as mock_connect:
            mock_connect.side_effect = psycopg2.OperationalError("Connection failed")

            with pytest.raises(psycopg2.OperationalError):
                initialize_database("admin.ini", "database.ini")

    @patch("src.db_initializer.get_db_config")
    @patch("src.db_initializer.psycopg2.connect")
    def test_initialize_database_grants_privileges(self, mock_connect, mock_get_config):
        """Тест выдачи прав на схему public."""
        mock_get_config.side_effect = [
            {"host": "localhost", "port": "5432", "user": "postgres", "password": "admin"},
            {"database": "test_db", "user": "test_user", "password": "test_pass"},
        ]

        # Создаем два разных connection объекта
        mock_conn_admin = MagicMock()
        mock_cursor_admin = MagicMock()
        mock_conn_admin.cursor.return_value.__enter__.return_value = mock_cursor_admin
        mock_conn_admin.autocommit = True

        mock_conn_target = MagicMock()
        mock_cursor_target = MagicMock()
        mock_conn_target.cursor.return_value.__enter__.return_value = mock_cursor_target
        mock_conn_target.autocommit = True

        # База данных и пользователь не существуют
        mock_cursor_admin.fetchone.side_effect = [None, None]

        # connect возвращает разные объекты при разных вызовах
        mock_connect.side_effect = [mock_conn_admin, mock_conn_target]

        initialize_database("admin.ini", "database.ini")

        # Проверяем, что были созданы БД и пользователь
        admin_calls = [str(call) for call in mock_cursor_admin.execute.call_args_list]
        assert any("CREATE DATABASE" in str(arg) for arg in admin_calls)
        assert any("CREATE USER" in str(arg) for arg in admin_calls)

        # Проверяем выдачу прав
        target_calls = [str(call) for call in mock_cursor_target.execute.call_args_list]
        assert any("GRANT ALL ON SCHEMA public" in str(arg) for arg in target_calls)

        # Проверяем, что оба соединения закрыты
        mock_conn_admin.close.assert_called_once()
        mock_conn_target.close.assert_called_once()

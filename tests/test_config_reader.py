"""Тесты для модуля config_reader."""
import os
import tempfile

import pytest

from src.config_reader import ConfigError, get_db_config


class TestConfigReader:
    """Тесты для чтения конфигурации."""

    def test_get_db_config_success(self):
        """Тест успешного чтения конфига."""
        with tempfile.NamedTemporaryFile(mode='w', suffix='.ini', delete=False) as f:
            f.write("""
[postgresql]
host=localhost
database=test_db
user=test_user
password=test_pass
port=5432
""")
            f.flush()

            config = get_db_config(f.name)

            assert config["host"] == "localhost"
            assert config["database"] == "test_db"
            assert config["user"] == "test_user"
            assert config["password"] == "test_pass"
            assert config["port"] == "5432"

            os.unlink(f.name)

    def test_get_db_config_file_not_found(self):
        """Тест ошибки при отсутствии файла."""
        with pytest.raises(ConfigError, match="Конфигурационный файл не найден"):
            get_db_config("non_existent.ini")

    def test_get_db_config_section_not_found(self):
        """Тест ошибки при отсутствии секции."""
        with tempfile.NamedTemporaryFile(mode='w', suffix='.ini', delete=False) as f:
            f.write("[other_section]\nkey=value\n")
            f.flush()

            with pytest.raises(ConfigError, match="Секция 'postgresql' не найдена"):
                get_db_config(f.name)

            os.unlink(f.name)

    def test_get_db_config_custom_section(self):
        """Тест чтения кастомной секции."""
        with tempfile.NamedTemporaryFile(mode='w', suffix='.ini', delete=False) as f:
            f.write("""
[custom]
host=192.168.1.1
database=custom_db
""")
            f.flush()

            config = get_db_config(f.name, section="custom")

            assert config["host"] == "192.168.1.1"
            assert config["database"] == "custom_db"

            os.unlink(f.name)
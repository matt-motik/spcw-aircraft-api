"""Модуль для чтения конфигурации подключения к БД."""

from configparser import ConfigParser
import os

from .path import get_root_dir


class ConfigError(Exception):
    """Исключение при ошибках чтения конфигурации."""


def get_db_config(filename: str = "database.ini", section: str = "postgresql") -> dict[str, str]:
    """
    Читает параметры подключения к БД из INI-файла.

    Args:
        filename: Имя конфигурационного файла (относительно корня проекта).
        section: Название секции с параметрами БД.

    Returns:
        Словарь с параметрами подключения (все значения — строки).

    Raises:
        ConfigError: Если файл не найден или секция отсутствует.

    Example:
        >>> config = get_db_config()
        >>> print(config["host"])
        localhost
    """
    root_dir = get_root_dir()
    file_path = os.path.join(root_dir, filename)

    if not os.path.exists(file_path):
        raise ConfigError(f"Конфигурационный файл не найден: {file_path}")

    parser = ConfigParser()
    parser.read(file_path)

    if not parser.has_section(section):
        raise ConfigError(f"Секция '{section}' не найдена в файле {file_path}")

    return dict(parser.items(section))

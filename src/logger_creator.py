"""Модуль реализующий создание логгера."""

import logging
import os

from .path import get_log_path


def create_logger(name: str) -> logging.Logger:
    """Функция для создания логгера.

    Args:
        name: има создаваемого логгера

    Returns:
        экземпляр логгера

    Example:

        >>> my_logger = create_logger(__name__)
    """
    logs_dir = get_log_path()
    if not os.path.exists(logs_dir):
        os.makedirs(logs_dir)
    log_path = os.path.join(logs_dir, name + ".log")

    logger = logging.getLogger(name)
    file_handler = logging.FileHandler(log_path, mode="w")
    file_formatter = logging.Formatter("%(asctime)s - %(name)s - %(levelname)s: %(message)s")
    file_handler.setFormatter(file_formatter)
    logger.addHandler(file_handler)
    logger.setLevel(logging.DEBUG)
    return logger

"""Модуль для первоначальной инициализации БД (создание БД и пользователя)."""

import psycopg2
from psycopg2 import sql

from .config_reader import get_db_config
from .logger_creator import create_logger

logger = create_logger(__name__)


def initialize_database(
    admin_config_file: str = "admin.ini",
    app_config_file: str = "database.ini",
) -> None:
    """
    Создаёт БД и пользователя для приложения.

    Подключается к PostgreSQL под админом (postgres), создаёт БД и пользователя,
    даёт права. Используется один раз при первоначальной настройке.

    Args:
        admin_config_file: Конфиг с правами postgres (host, port, user, password).
        app_config_file: Конфиг приложения (для получения пароля нового пользователя).

    Raises:
        ConfigError: Если конфиг не найден.
        psycopg2.Error: При ошибках SQL.
    """
    admin_params = get_db_config(admin_config_file)
    app_params = get_db_config(app_config_file)

    db_name = app_params["database"]
    db_user = app_params["user"]
    db_password = app_params["password"]

    conn = None
    try:
        conn = psycopg2.connect(**admin_params)
        conn.autocommit = True

        with conn.cursor() as cur:
            # Проверить и создать БД
            cur.execute("SELECT 1 FROM pg_database WHERE datname = %s", (db_name,))
            if not cur.fetchone():
                cur.execute(sql.SQL("CREATE DATABASE {}").format(sql.Identifier(db_name)))
                logger.info("База %s создана", db_name)

            # Проверить и создать пользователя
            cur.execute("SELECT 1 FROM pg_roles WHERE rolname = %s", (db_user,))
            if not cur.fetchone():
                cur.execute(
                    sql.SQL("CREATE USER {} WITH PASSWORD {}").format(
                        sql.Identifier(db_user), sql.Literal(db_password)
                    )
                )
                logger.info("Пользователь %s создан", db_user)

            # Выдать права
            conn_target = psycopg2.connect(
                host=admin_params["host"],
                port=admin_params["port"],
                user=admin_params["user"],
                password=admin_params["password"],
                database=db_name,
            )
            conn_target.autocommit = True
            with conn_target.cursor() as cur_target:
                cur_target.execute(sql.SQL("GRANT ALL ON SCHEMA public TO {}").format(sql.Identifier(db_user)))
                logger.info("Права на схему public выданы %s", db_user)
            conn_target.close()
    finally:
        if conn:
            conn.close()

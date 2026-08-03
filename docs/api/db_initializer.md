# Модуль: `db_initializer.py`

*Сгенерировано: 2026-07-28 00:29:33*

---

<div id="initialize_database"></div>

## initialize_database

**Тип:** function

**Кратко:** Создаёт БД и пользователя для приложения.

### Полная документация

```python
Создаёт БД и пользователя для приложения.

Подключается к PostgreSQL под админом (postgres), создаёт БД и пользователя,
даёт права. Используется один раз при первоначальной настройке.

Args:
    admin_config_file: Конфиг с правами postgres (host, port, user, password).
    app_config_file: Конфиг приложения (для получения пароля нового пользователя).

Raises:
    ConfigError: Если конфиг не найден.
    psycopg2.Error: При ошибках SQL.
```

---


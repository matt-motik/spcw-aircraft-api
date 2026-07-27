# Модуль: `db_manager.py`

*Сгенерировано: 2026-07-28 00:29:33*

---

<div id="DBManager"></div>

## DBManager

**Тип:** class

**Кратко:** Класс для работы с данными в PostgreSQL.

### Полная документация

```python
Класс для работы с данными в PostgreSQL.

Подключается к БД, создаёт таблицы, выполняет запросы.
Использует библиотеку psycopg2.
```

---

<div id="DBManager.connection"></div>

## DBManager.connection

**Тип:** method

**Кратко:** Ленивое создание соединения.

### Полная документация

```python
Ленивое создание соединения.
```

---

<div id="DBManager.initialize"></div>

## DBManager.initialize

**Тип:** method

**Кратко:** Подготовка хранилища — создание таблиц.

### Полная документация

```python
Подготовка хранилища — создание таблиц.
```

---

<div id="DBManager.create_tables"></div>

## DBManager.create_tables

**Тип:** method

**Кратко:** Создаёт таблицы countries и aeroplanes.

### Полная документация

```python
Создаёт таблицы countries и aeroplanes.
```

---

<div id="DBManager.insert_country"></div>

## DBManager.insert_country

**Тип:** method

**Кратко:** Добавляет страну в таблицу.

### Полная документация

```python
Добавляет страну в таблицу.

Returns:
    id созданной записи.
```

---

<div id="DBManager.add_country"></div>

## DBManager.add_country

**Тип:** method

**Кратко:** Добавляет страну в хранилище.

### Полная документация

```python
Добавляет страну в хранилище.

Returns:
    id страны или None, если хранилище не поддерживает страны.
```

---

<div id="DBManager.insert_aeroplane"></div>

## DBManager.insert_aeroplane

**Тип:** method

**Кратко:** Добавляет самолёт в таблицу.

### Полная документация

```python
Добавляет самолёт в таблицу.
```

---

<div id="DBManager.add_aeroplane"></div>

## DBManager.add_aeroplane

**Тип:** method

**Кратко:** Добавляет один самолёт в БД.

### Полная документация

```python
Добавляет один самолёт в БД.
```

---

<div id="DBManager.add_multiple_aeroplanes"></div>

## DBManager.add_multiple_aeroplanes

**Тип:** method

**Кратко:** Пакетное добавление/обновление списка самолётов с однократным сохранением.

### Полная документация

```python
Пакетное добавление/обновление списка самолётов с однократным сохранением.

Args:
    aeroplanes: Список объектов Aeroplane.

Raises:
    TypeError: Если передан объект не типа List[Aeroplane].
```

---

<div id="DBManager.delete_aeroplane"></div>

## DBManager.delete_aeroplane

**Тип:** method

**Кратко:** Удаляет самолёт из БД по icao24.

### Полная документация

```python
Удаляет самолёт из БД по icao24.
```

---

<div id="DBManager.get_aeroplanes"></div>

## DBManager.get_aeroplanes

**Тип:** method

**Кратко:** Возвращает список самолётов, удовлетворяющих заданным фильтрам.

### Полная документация

```python
Возвращает список самолётов, удовлетворяющих заданным фильтрам.

Args:
    **filters: Именованные параметры для фильтрации.
               Поддерживаемые ключи зависят от реализации.
               Например: origin_country='Russia', min_altitude=10000.

Returns:
    Список объектов Aeroplane, соответствующих критериям.

Raises:
    ValueError: Если переданы некорректные ключи фильтрации.
```

---

<div id="DBManager.get_countries_and_aeroplanes_count"></div>

## DBManager.get_countries_and_aeroplanes_count

**Тип:** method

**Кратко:** Получает список всех стран и количество самолётов в их воздушных пространствах.

### Полная документация

```python
Получает список всех стран и количество самолётов в их воздушных пространствах.
```

---

<div id="DBManager.get_all_aeroplanes"></div>

## DBManager.get_all_aeroplanes

**Тип:** method

**Кратко:** Получает список всех воздушных судов.

### Полная документация

```python
Получает список всех воздушных судов.
```

---

<div id="DBManager.get_avg_speed"></div>

## DBManager.get_avg_speed

**Тип:** method

**Кратко:** Получает среднюю скорость по самолётам.

### Полная документация

```python
Получает среднюю скорость по самолётам.
```

---

<div id="DBManager.get_aeroplanes_with_higher_speed"></div>

## DBManager.get_aeroplanes_with_higher_speed

**Тип:** method

**Кратко:** Получает топ-N самолётов со скоростью выше средней.

### Полная документация

```python
Получает топ-N самолётов со скоростью выше средней.

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
```

---

<div id="DBManager.get_aeroplanes_with_keyword"></div>

## DBManager.get_aeroplanes_with_keyword

**Тип:** method

**Кратко:** Получает самолёты, в позывном которых содержится keyword.

### Полная документация

```python
Получает самолёты, в позывном которых содержится keyword.

Args:
    keyword: Подстрока для поиска (например, 'ACA').
```

---

<div id="DBManager.close"></div>

## DBManager.close

**Тип:** method

**Кратко:** Закрывает соединение с БД.

### Полная документация

```python
Закрывает соединение с БД.
```

---

<div id="DBManager.get_country"></div>

## DBManager.get_country

**Тип:** method

**Кратко:** Получает данные о стране из хранилища.

### Полная документация

```python
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
```

---

<div id="connection"></div>

## connection

**Тип:** function

**Кратко:** Ленивое создание соединения.

### Полная документация

```python
Ленивое создание соединения.
```

---

<div id="initialize"></div>

## initialize

**Тип:** function

**Кратко:** Подготовка хранилища — создание таблиц.

### Полная документация

```python
Подготовка хранилища — создание таблиц.
```

---

<div id="create_tables"></div>

## create_tables

**Тип:** function

**Кратко:** Создаёт таблицы countries и aeroplanes.

### Полная документация

```python
Создаёт таблицы countries и aeroplanes.
```

---

<div id="insert_country"></div>

## insert_country

**Тип:** function

**Кратко:** Добавляет страну в таблицу.

### Полная документация

```python
Добавляет страну в таблицу.

Returns:
    id созданной записи.
```

---

<div id="add_country"></div>

## add_country

**Тип:** function

**Кратко:** Добавляет страну в хранилище.

### Полная документация

```python
Добавляет страну в хранилище.

Returns:
    id страны или None, если хранилище не поддерживает страны.
```

---

<div id="insert_aeroplane"></div>

## insert_aeroplane

**Тип:** function

**Кратко:** Добавляет самолёт в таблицу.

### Полная документация

```python
Добавляет самолёт в таблицу.
```

---

<div id="add_aeroplane"></div>

## add_aeroplane

**Тип:** function

**Кратко:** Добавляет один самолёт в БД.

### Полная документация

```python
Добавляет один самолёт в БД.
```

---

<div id="add_multiple_aeroplanes"></div>

## add_multiple_aeroplanes

**Тип:** function

**Кратко:** Пакетное добавление/обновление списка самолётов с однократным сохранением.

### Полная документация

```python
Пакетное добавление/обновление списка самолётов с однократным сохранением.

Args:
    aeroplanes: Список объектов Aeroplane.

Raises:
    TypeError: Если передан объект не типа List[Aeroplane].
```

---

<div id="delete_aeroplane"></div>

## delete_aeroplane

**Тип:** function

**Кратко:** Удаляет самолёт из БД по icao24.

### Полная документация

```python
Удаляет самолёт из БД по icao24.
```

---

<div id="get_aeroplanes"></div>

## get_aeroplanes

**Тип:** function

**Кратко:** Возвращает список самолётов, удовлетворяющих заданным фильтрам.

### Полная документация

```python
Возвращает список самолётов, удовлетворяющих заданным фильтрам.

Args:
    **filters: Именованные параметры для фильтрации.
               Поддерживаемые ключи зависят от реализации.
               Например: origin_country='Russia', min_altitude=10000.

Returns:
    Список объектов Aeroplane, соответствующих критериям.

Raises:
    ValueError: Если переданы некорректные ключи фильтрации.
```

---

<div id="get_countries_and_aeroplanes_count"></div>

## get_countries_and_aeroplanes_count

**Тип:** function

**Кратко:** Получает список всех стран и количество самолётов в их воздушных пространствах.

### Полная документация

```python
Получает список всех стран и количество самолётов в их воздушных пространствах.
```

---

<div id="get_all_aeroplanes"></div>

## get_all_aeroplanes

**Тип:** function

**Кратко:** Получает список всех воздушных судов.

### Полная документация

```python
Получает список всех воздушных судов.
```

---

<div id="get_avg_speed"></div>

## get_avg_speed

**Тип:** function

**Кратко:** Получает среднюю скорость по самолётам.

### Полная документация

```python
Получает среднюю скорость по самолётам.
```

---

<div id="get_aeroplanes_with_higher_speed"></div>

## get_aeroplanes_with_higher_speed

**Тип:** function

**Кратко:** Получает топ-N самолётов со скоростью выше средней.

### Полная документация

```python
Получает топ-N самолётов со скоростью выше средней.

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
```

---

<div id="get_aeroplanes_with_keyword"></div>

## get_aeroplanes_with_keyword

**Тип:** function

**Кратко:** Получает самолёты, в позывном которых содержится keyword.

### Полная документация

```python
Получает самолёты, в позывном которых содержится keyword.

Args:
    keyword: Подстрока для поиска (например, 'ACA').
```

---

<div id="close"></div>

## close

**Тип:** function

**Кратко:** Закрывает соединение с БД.

### Полная документация

```python
Закрывает соединение с БД.
```

---

<div id="get_country"></div>

## get_country

**Тип:** function

**Кратко:** Получает данные о стране из хранилища.

### Полная документация

```python
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
```

---


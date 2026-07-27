# Модуль: `base_storage.py`

*Сгенерировано: 2026-07-28 00:29:33*

---

<div id="BaseStorage"></div>

## BaseStorage

**Тип:** class

**Кратко:** Абстрактный базовый класс для хранилища данных о самолётах.

### Полная документация

```python
Абстрактный базовый класс для хранилища данных о самолётах.

Определяет интерфейс для добавления, получения и удаления записей.
Конкретные реализации (JSON, CSV, БД) должны переопределить все методы.
```

---

<div id="BaseStorage.add_aeroplane"></div>

## BaseStorage.add_aeroplane

**Тип:** method

**Кратко:** Добавляет запись о самолёте в хранилище.

### Полная документация

```python
Добавляет запись о самолёте в хранилище.

Args:
    aeroplane: Экземпляр класса Aeroplane.

Raises:
    TypeError: Если передан объект не типа Aeroplane.
    FileNotFoundError: Если файл хранилища не найден (при необходимости).
```

---

<div id="BaseStorage.add_multiple_aeroplanes"></div>

## BaseStorage.add_multiple_aeroplanes

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

<div id="BaseStorage.get_aeroplanes"></div>

## BaseStorage.get_aeroplanes

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

<div id="BaseStorage.delete_aeroplane"></div>

## BaseStorage.delete_aeroplane

**Тип:** method

**Кратко:** Удаляет запись о самолёте из хранилища.

### Полная документация

```python
Удаляет запись о самолёте из хранилища.

Сравнение производится по уникальному идентификатору icao24.

Args:
    aeroplane: Экземпляр Aeroplane, который требуется удалить.

Raises:
    ValueError: Если самолёт с таким icao24 не найден в хранилище.
```

---

<div id="BaseStorage.add_country"></div>

## BaseStorage.add_country

**Тип:** method

**Кратко:** Добавляет страну в хранилище.

### Полная документация

```python
Добавляет страну в хранилище.

Returns:
    id страны или None, если хранилище не поддерживает страны.
```

---

<div id="BaseStorage.get_country"></div>

## BaseStorage.get_country

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

<div id="BaseStorage.initialize"></div>

## BaseStorage.initialize

**Тип:** method

**Кратко:** Подготовка хранилища (создание таблиц, файлов и т.д.).

### Полная документация

```python
Подготовка хранилища (создание таблиц, файлов и т.д.).
```

---

<div id="BaseStorage.close"></div>

## BaseStorage.close

**Тип:** method

**Кратко:** Закрывает хранилище если поддерживает.

### Полная документация

```python
Закрывает хранилище если поддерживает.
```

---

<div id="BaseStorage.get_aeroplanes_with_keyword"></div>

## BaseStorage.get_aeroplanes_with_keyword

**Тип:** method

**Кратко:** Получает самолёты, в позывном которых содержится keyword.

### Полная документация

```python
Получает самолёты, в позывном которых содержится keyword.

Args:
    keyword: Подстрока для поиска (например, 'AFL').
```

---

<div id="add_aeroplane"></div>

## add_aeroplane

**Тип:** function

**Кратко:** Добавляет запись о самолёте в хранилище.

### Полная документация

```python
Добавляет запись о самолёте в хранилище.

Args:
    aeroplane: Экземпляр класса Aeroplane.

Raises:
    TypeError: Если передан объект не типа Aeroplane.
    FileNotFoundError: Если файл хранилища не найден (при необходимости).
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

<div id="delete_aeroplane"></div>

## delete_aeroplane

**Тип:** function

**Кратко:** Удаляет запись о самолёте из хранилища.

### Полная документация

```python
Удаляет запись о самолёте из хранилища.

Сравнение производится по уникальному идентификатору icao24.

Args:
    aeroplane: Экземпляр Aeroplane, который требуется удалить.

Raises:
    ValueError: Если самолёт с таким icao24 не найден в хранилище.
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

<div id="initialize"></div>

## initialize

**Тип:** function

**Кратко:** Подготовка хранилища (создание таблиц, файлов и т.д.).

### Полная документация

```python
Подготовка хранилища (создание таблиц, файлов и т.д.).
```

---

<div id="close"></div>

## close

**Тип:** function

**Кратко:** Закрывает хранилище если поддерживает.

### Полная документация

```python
Закрывает хранилище если поддерживает.
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
    keyword: Подстрока для поиска (например, 'AFL').
```

---


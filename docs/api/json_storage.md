# Модуль: `json_storage.py`

*Сгенерировано: 2026-07-27 23:14:50*

---

<div id="JsonStorage"></div>

## JsonStorage

**Тип:** class

**Кратко:** Класс для хранилища данных о самолётах.

### Полная документация

```python
Класс для хранилища данных о самолётах.

Определяет Класс для добавления, получения и удаления записей.
```

---

<div id="JsonStorage.initialize"></div>

## JsonStorage.initialize

**Тип:** method

**Кратко:** JSON-файл создаётся при первом сохранении.

### Полная документация

```python
JSON-файл создаётся при первом сохранении.
```

---

<div id="JsonStorage.add_aeroplane"></div>

## JsonStorage.add_aeroplane

**Тип:** method

**Кратко:** Добавляет запись о самолёте в хранилище.

### Полная документация

```python
Добавляет запись о самолёте в хранилище.

Args:
    aeroplane: Экземпляр класса Aeroplane.

Raises:
    TypeError: Если передан объект не типа Aeroplane.
```

---

<div id="JsonStorage.add_multiple_aeroplanes"></div>

## JsonStorage.add_multiple_aeroplanes

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

<div id="JsonStorage.get_aeroplanes"></div>

## JsonStorage.get_aeroplanes

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

<div id="JsonStorage.delete_aeroplane"></div>

## JsonStorage.delete_aeroplane

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

<div id="JsonStorage.add_country"></div>

## JsonStorage.add_country

**Тип:** method

**Кратко:** Добавляет страну в хранилище.

### Полная документация

```python
Добавляет страну в хранилище.

Returns:
    id страны или None, если хранилище не поддерживает страны.
```

---

<div id="JsonStorage.get_country"></div>

## JsonStorage.get_country

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

<div id="JsonStorage.close"></div>

## JsonStorage.close

**Тип:** method

**Кратко:** Закрывает хранилище. Для JSON — ничего не делает.

### Полная документация

```python
Закрывает хранилище. Для JSON — ничего не делает.
```

---

<div id="JsonStorage.get_aeroplanes_with_keyword"></div>

## JsonStorage.get_aeroplanes_with_keyword

**Тип:** method

**Кратко:** Получает самолёты, в позывном которых содержится keyword.

### Полная документация

```python
Получает самолёты, в позывном которых содержится keyword.
```

---

<div id="initialize"></div>

## initialize

**Тип:** function

**Кратко:** JSON-файл создаётся при первом сохранении.

### Полная документация

```python
JSON-файл создаётся при первом сохранении.
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

<div id="close"></div>

## close

**Тип:** function

**Кратко:** Закрывает хранилище. Для JSON — ничего не делает.

### Полная документация

```python
Закрывает хранилище. Для JSON — ничего не делает.
```

---

<div id="get_aeroplanes_with_keyword"></div>

## get_aeroplanes_with_keyword

**Тип:** function

**Кратко:** Получает самолёты, в позывном которых содержится keyword.

### Полная документация

```python
Получает самолёты, в позывном которых содержится keyword.
```

---


# Модуль: `aeroplanes_api.py`

*Сгенерировано: 2026-07-05 02:04:14*

---

<div id="AeroplanesAPI"></div>

## AeroplanesAPI

**Тип:** class

**Кратко:** Класс для работы с API nominatim.openstreetmap.org и opensky-network.org.

### Полная документация

```python
Класс для работы с API nominatim.openstreetmap.org и opensky-network.org.

Реализует получение bounding box страны и списка самолётов в её воздушном пространстве.
```

---

<div id="AeroplanesAPI.get_country_bbox"></div>

## AeroplanesAPI.get_country_bbox

**Тип:** method

**Кратко:** Получает bounding box страны через Nominatim API.

### Полная документация

```python
Получает bounding box страны через Nominatim API.

Args:
    country_name: Название страны (например, "Spain", "Russia")

Returns:
    Словарь с координатами: {'latmin': , 'lonmin': , 'latmax': , 'lonmax': }

Raises:
    RuntimeError: Если страна не найдена или запрос неуспешен.
```

---

<div id="AeroplanesAPI.get_aeroplanes"></div>

## AeroplanesAPI.get_aeroplanes

**Тип:** method

**Кратко:** Получает список самолётов в воздушном пространстве указанной страны.

### Полная документация

```python
Получает список самолётов в воздушном пространстве указанной страны.

1. Получает bounding box страны.
2. Делает запрос к OpenSky API.

Args:
    country_name: Название страны.

Returns:
    Сырой список состояний от OpenSky API (list[list]).

Raises:
    RuntimeError: При ошибках API или если страна не найдена.
```

---

<div id="get_country_bbox"></div>

## get_country_bbox

**Тип:** function

**Кратко:** Получает bounding box страны через Nominatim API.

### Полная документация

```python
Получает bounding box страны через Nominatim API.

Args:
    country_name: Название страны (например, "Spain", "Russia")

Returns:
    Словарь с координатами: {'latmin': , 'lonmin': , 'latmax': , 'lonmax': }

Raises:
    RuntimeError: Если страна не найдена или запрос неуспешен.
```

---

<div id="get_aeroplanes"></div>

## get_aeroplanes

**Тип:** function

**Кратко:** Получает список самолётов в воздушном пространстве указанной страны.

### Полная документация

```python
Получает список самолётов в воздушном пространстве указанной страны.

1. Получает bounding box страны.
2. Делает запрос к OpenSky API.

Args:
    country_name: Название страны.

Returns:
    Сырой список состояний от OpenSky API (list[list]).

Raises:
    RuntimeError: При ошибках API или если страна не найдена.
```

---


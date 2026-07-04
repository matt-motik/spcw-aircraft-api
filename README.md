# SkyPro Модуль ООП Трекер Самолётов
Курсовая работа по интеграции с внешними API.  
Программа получает данные о самолётах в реальном времени, сохраняет их в JSON-хранилище и позволяет фильтровать/сортировать результаты.

### 🚀 Возможности программы
 Получение bounding box страны через **Nominatim API**
- Получение списка самолётов в воздушном пространстве через **OpenSky Network API**
- Сохранение данных в JSON-файл с возможностью добавления, обновления и удаления записей
- Фильтрация самолётов по:
  - стране регистрации
  - диапазону высот
  - диапазону скоростей
  - нахождению на земле / в воздухе
  - географическим координатам (bounding box)
- Сортировка по высоте (и скорости при равной высоте)
- Вывод топ-N самолётов
- Работа в офлайн-режиме (использование кэшированных данных при недоступности API)


## Содержание
- [Технологии](#технологии)
- [Установка](#установка)
- [Разработка](#разработка)
- [Тестирование](#тестирование)
- [Deploy и CI/CD](#deploy-и-cicd)
- [Contributing](#contributing)
- [FAQ](#faq)
- [To do](#to-do)
- [Команда проекта](#команда-проекта)


<div id="технологии"></div>

## Технологии
- [Python](https://www.python.org/)
- [pytest](https://docs.pytest.org/) — тестирование с покрытием
- [poetry](https://python-poetry.org/) — управление зависимостями

[//]: # (- [requests]&#40;https://docs.python-requests.org/&#41; — HTTP-запросы к API конвертации валют)

<div id="установка"></div>

## Установка
Для управления зависимостями в проекте используется [Poetry](https://python-poetry.org).

1. Клонируйте репозиторий:
```
git clone https://github.com/matt-motik/spcw-aircraft-api.git
cd sp-oop
poetry install
```

<div id="разработка"></div>

## Разработка
<!-- СЕКЦИЯ_AUTO_API: СТАРТ -->
### 📚 Документация API

*Этот раздел генерируется автоматически из docstring.*

| Модуль | Функция/Класс | Краткое описание |
|--------|---------------|------------------|
| [**`aeroplane.py`**](docs/api/aeroplane.md) | | |
| | [📦 Aeroplane](docs/api/aeroplane.md#Aeroplane) | Класс, представляющий данные о самолёте. |
| | [⚙️ Aeroplane.icao24](docs/api/aeroplane.md#Aeroplane.icao24) | Геттер. Уникальный идентификатор борта (транспондера). |
| | [⚙️ Aeroplane.icao24](docs/api/aeroplane.md#Aeroplane.icao24) | Сеттер. Уникальный идентификатор борта (транспондера). |
| | [⚙️ Aeroplane.callsign](docs/api/aeroplane.md#Aeroplane.callsign) | Позывной рейса. |
| | [⚙️ Aeroplane.callsign](docs/api/aeroplane.md#Aeroplane.callsign) | Сеттер. Позывной рейса. |
| | [⚙️ Aeroplane.origin_country](docs/api/aeroplane.md#Aeroplane.origin_country) | Страна регистрации. |
| | [⚙️ Aeroplane.origin_country](docs/api/aeroplane.md#Aeroplane.origin_country) | Сеттер. Страна регистрации. |
| | [⚙️ Aeroplane.longitude](docs/api/aeroplane.md#Aeroplane.longitude) | Долгота (°). |
| | [⚙️ Aeroplane.longitude](docs/api/aeroplane.md#Aeroplane.longitude) | Сеттер. Долгота (°). |
| | [⚙️ Aeroplane.latitude](docs/api/aeroplane.md#Aeroplane.latitude) | Широта (°). |
| | [⚙️ Aeroplane.latitude](docs/api/aeroplane.md#Aeroplane.latitude) | Сеттер. Широта (°). |
| | [⚙️ Aeroplane.altitude](docs/api/aeroplane.md#Aeroplane.altitude) | Барометрическая высота, м. |
| | [⚙️ Aeroplane.altitude](docs/api/aeroplane.md#Aeroplane.altitude) | Сеттер. Барометрическая высота, м. |
| | [⚙️ Aeroplane.velocity](docs/api/aeroplane.md#Aeroplane.velocity) | Скорость относительно земли, м/с. |
| | [⚙️ Aeroplane.velocity](docs/api/aeroplane.md#Aeroplane.velocity) | Сеттер. Скорость относительно земли, м/с. |
| | [⚙️ Aeroplane.on_ground](docs/api/aeroplane.md#Aeroplane.on_ground) | Флаг нахождения на земле. |
| | [⚙️ Aeroplane.on_ground](docs/api/aeroplane.md#Aeroplane.on_ground) | Сеттер. Флаг нахождения на земле. |
| | [⚙️ Aeroplane.cast_to_object_list](docs/api/aeroplane.md#Aeroplane.cast_to_object_list) | Преобразует сырой список состояний от OpenSky API в список объектов Aeroplane. |
| | [⚙️ Aeroplane.to_dict](docs/api/aeroplane.md#Aeroplane.to_dict) | Сериализация в словарь. |
| | [⚙️ Aeroplane.from_dict](docs/api/aeroplane.md#Aeroplane.from_dict) | Десериализация из словаря. |
| | [🔧 icao24](docs/api/aeroplane.md#icao24) | Геттер. Уникальный идентификатор борта (транспондера). |
| | [🔧 icao24](docs/api/aeroplane.md#icao24) | Сеттер. Уникальный идентификатор борта (транспондера). |
| | [🔧 callsign](docs/api/aeroplane.md#callsign) | Позывной рейса. |
| | [🔧 callsign](docs/api/aeroplane.md#callsign) | Сеттер. Позывной рейса. |
| | [🔧 origin_country](docs/api/aeroplane.md#origin_country) | Страна регистрации. |
| | [🔧 origin_country](docs/api/aeroplane.md#origin_country) | Сеттер. Страна регистрации. |
| | [🔧 longitude](docs/api/aeroplane.md#longitude) | Долгота (°). |
| | [🔧 longitude](docs/api/aeroplane.md#longitude) | Сеттер. Долгота (°). |
| | [🔧 latitude](docs/api/aeroplane.md#latitude) | Широта (°). |
| | [🔧 latitude](docs/api/aeroplane.md#latitude) | Сеттер. Широта (°). |
| | [🔧 altitude](docs/api/aeroplane.md#altitude) | Барометрическая высота, м. |
| | [🔧 altitude](docs/api/aeroplane.md#altitude) | Сеттер. Барометрическая высота, м. |
| | [🔧 velocity](docs/api/aeroplane.md#velocity) | Скорость относительно земли, м/с. |
| | [🔧 velocity](docs/api/aeroplane.md#velocity) | Сеттер. Скорость относительно земли, м/с. |
| | [🔧 on_ground](docs/api/aeroplane.md#on_ground) | Флаг нахождения на земле. |
| | [🔧 on_ground](docs/api/aeroplane.md#on_ground) | Сеттер. Флаг нахождения на земле. |
| | [🔧 cast_to_object_list](docs/api/aeroplane.md#cast_to_object_list) | Преобразует сырой список состояний от OpenSky API в список объектов Aeroplane. |
| | [🔧 to_dict](docs/api/aeroplane.md#to_dict) | Сериализация в словарь. |
| | [🔧 from_dict](docs/api/aeroplane.md#from_dict) | Десериализация из словаря. |
| [**`aeroplanes_api.py`**](docs/api/aeroplanes_api.md) | | |
| | [📦 AeroplanesAPI](docs/api/aeroplanes_api.md#AeroplanesAPI) | Класс для работы с API nominatim.openstreetmap.org и opensky-network.org. |
| | [⚙️ AeroplanesAPI.get_country_bbox](docs/api/aeroplanes_api.md#AeroplanesAPI.get_country_bbox) | Получает bounding box страны через Nominatim API. |
| | [⚙️ AeroplanesAPI.get_aeroplanes](docs/api/aeroplanes_api.md#AeroplanesAPI.get_aeroplanes) | Получает список самолётов в воздушном пространстве указанной страны. |
| | [🔧 get_country_bbox](docs/api/aeroplanes_api.md#get_country_bbox) | Получает bounding box страны через Nominatim API. |
| | [🔧 get_aeroplanes](docs/api/aeroplanes_api.md#get_aeroplanes) | Получает список самолётов в воздушном пространстве указанной страны. |
| [**`base_api.py`**](docs/api/base_api.md) | | |
| | [📦 BaseAPI](docs/api/base_api.md#BaseAPI) | Абстрактный класс для работы с внешними API. |
| | [⚙️ BaseAPI.get_country_bbox](docs/api/base_api.md#BaseAPI.get_country_bbox) | Метод получения bounding box страны. |
| | [⚙️ BaseAPI.get_aeroplanes](docs/api/base_api.md#BaseAPI.get_aeroplanes) | Метод получения списка самолётов. |
| | [🔧 get_country_bbox](docs/api/base_api.md#get_country_bbox) | Метод получения bounding box страны. |
| | [🔧 get_aeroplanes](docs/api/base_api.md#get_aeroplanes) | Метод получения списка самолётов. |
| [**`base_storage.py`**](docs/api/base_storage.md) | | |
| | [📦 BaseStorage](docs/api/base_storage.md#BaseStorage) | Абстрактный базовый класс для хранилища данных о самолётах. |
| | [⚙️ BaseStorage.add_aeroplane](docs/api/base_storage.md#BaseStorage.add_aeroplane) | Добавляет запись о самолёте в хранилище. |
| | [⚙️ BaseStorage.get_aeroplanes](docs/api/base_storage.md#BaseStorage.get_aeroplanes) | Возвращает список самолётов, удовлетворяющих заданным фильтрам. |
| | [⚙️ BaseStorage.delete_aeroplane](docs/api/base_storage.md#BaseStorage.delete_aeroplane) | Удаляет запись о самолёте из хранилища. |
| | [🔧 add_aeroplane](docs/api/base_storage.md#add_aeroplane) | Добавляет запись о самолёте в хранилище. |
| | [🔧 get_aeroplanes](docs/api/base_storage.md#get_aeroplanes) | Возвращает список самолётов, удовлетворяющих заданным фильтрам. |
| | [🔧 delete_aeroplane](docs/api/base_storage.md#delete_aeroplane) | Удаляет запись о самолёте из хранилища. |
| [**`json_storage.py`**](docs/api/json_storage.md) | | |
| | [📦 JsonStorage](docs/api/json_storage.md#JsonStorage) | Класс для хранилища данных о самолётах. |
| | [⚙️ JsonStorage.add_aeroplane](docs/api/json_storage.md#JsonStorage.add_aeroplane) | Добавляет запись о самолёте в хранилище. |
| | [⚙️ JsonStorage.add_multiple_aeroplanes](docs/api/json_storage.md#JsonStorage.add_multiple_aeroplanes) | Пакетное добавление/обновление списка самолётов с однократным сохранением. |
| | [⚙️ JsonStorage.get_aeroplanes](docs/api/json_storage.md#JsonStorage.get_aeroplanes) | Возвращает список самолётов, удовлетворяющих заданным фильтрам. |
| | [⚙️ JsonStorage.delete_aeroplane](docs/api/json_storage.md#JsonStorage.delete_aeroplane) | Удаляет запись о самолёте из хранилища. |
| | [🔧 add_aeroplane](docs/api/json_storage.md#add_aeroplane) | Добавляет запись о самолёте в хранилище. |
| | [🔧 add_multiple_aeroplanes](docs/api/json_storage.md#add_multiple_aeroplanes) | Пакетное добавление/обновление списка самолётов с однократным сохранением. |
| | [🔧 get_aeroplanes](docs/api/json_storage.md#get_aeroplanes) | Возвращает список самолётов, удовлетворяющих заданным фильтрам. |
| | [🔧 delete_aeroplane](docs/api/json_storage.md#delete_aeroplane) | Удаляет запись о самолёте из хранилища. |
| [**`logger_creator.py`**](docs/api/logger_creator.md) | | |
| | [🔧 create_logger](docs/api/logger_creator.md#create_logger) | Функция для создания логгера. |
| [**`main.py`**](docs/api/main.md) | | |
| | [🔧 input_float](docs/api/main.md#input_float) | Запрашивает у пользователя ввод дробного числа через консоль. |
| | [🔧 input_int](docs/api/main.md#input_int) | Запрашивает у пользователя ввод целого числа через консоль. |
| | [🔧 input_bool](docs/api/main.md#input_bool) | Запрашивает у пользователя подтверждение действия через консоль. |
| | [🔧 sort_aeroplanes](docs/api/main.md#sort_aeroplanes) | Сортирует самолёты по убыванию высоты (и скорости при равной высоте). |
| | [🔧 get_top_aeroplanes](docs/api/main.md#get_top_aeroplanes) | Получает первые top_n самолёта. |
| | [🔧 print_aeroplanes](docs/api/main.md#print_aeroplanes) | Печатает список самолётов. |
| | [🔧 user_interaction](docs/api/main.md#user_interaction) | Функция для взаимодействия с пользователем. |
| | [🔧 main](docs/api/main.md#main) | Основная функция запуска. |
| [**`path.py`**](docs/api/path.md) | | |
| | [🔧 get_log_path](docs/api/path.md#get_log_path) | Функция для получения пути к папке с логами. |
| | [🔧 get_root_dir](docs/api/path.md#get_root_dir) | Функция для получения пути к корневой папке проекта. |
| | [🔧 get_data_dir](docs/api/path.md#get_data_dir) | Функция для получения пути к папке с данными. |

> 📘 **Полная документация** с примерами и описанием параметров доступна в папке [`docs/api`](docs/api).

<!-- СЕКЦИЯ_AUTO_API: КОНЕЦ -->
### Требования
В разработке
### Установка зависимостей
```poetry install```
### Запуск программы
```poetry run python main.py```
### Создание билда
В разработке

<div id="тестирование"></div>

## 🧪 Тестирование
main.py не тестируется
<!-- СЕКЦИЯ_AUTO_TEST: СТАРТ -->

*Этот раздел генерируется автоматически на основании данных `poetry run pytest`.*

### 📊 Результаты тестов SRC

```
📈 Покрытие кода:
tests/test_aeroplane.py ............................                     [ 47%]
tests/test_aeroplanes_api.py ..........                                  [ 64%]
tests/test_json_storage.py ................                              [ 91%]
tests/test_logger_creator.py ..                                          [ 94%]
tests/test_path.py ...                                                   [100%]
src/__init__.py             0      0   100%
src/aeroplane.py          168      0   100%
src/aeroplanes_api.py      49      0   100%
src/base_api.py             7      0   100%
src/base_storage.py        11      0   100%
src/json_storage.py       117      0   100%
src/logger_creator.py      15      0   100%
src/path.py                10      0   100%
TOTAL                     377      0   100%
Coverage HTML written to dir htmlcov/src

🎯 Результаты тестов src:
tests/test_aeroplane.py ............................                     [ 47%]
tests/test_aeroplanes_api.py ..........                                  [ 64%]
tests/test_json_storage.py ................                              [ 91%]
tests/test_logger_creator.py ..                                          [ 94%]
tests/test_path.py ...                                                   [100%]
================================ tests coverage ================================
-----------------------------------------------------
-----------------------------------------------------
============================== 59 passed in 0.16s ==============================
```

> 📊 **HTML отчёт покрытия**: [`htmlcov/index.html`](htmlcov/src/index.html)



<!-- СЕКЦИЯ_AUTO_TEST: КОНЕЦ -->
## Deploy и CI/CD
В разработке


## Contributing
В разработке — [Contributing.md](./CONTRIBUTING.md).

## FAQ
В разработке

## To do
- [x] Структура проекта, `pyproject.toml`, `README.md`, `.gitignore`
- [x] Виртуальное окружение, установка зависимостей через Poetry
- [x] `readme_gen.py` — скрипт генерации README, и покрытия тестами
- [x] `lint.ps1` — скрипт литеров, форматеров, типизаторов и др
- [x] [main.py](main.py) — Точка входа в приложение.
- [x] [aeroplane.py](src/aeroplane.py) — Модуль класса, моделирующего данные самолёта.
- [x] [aeroplanes_api.py](src/aeroplanes_api.py) - Модуль класса для работы с внешними API (Nominatim + OpenSky).
- [x] [base_api.py](src/base_api.py) - Модуль базового класса для работы с внешними API.
- [x] [base_storage.py](src/base_storage.py) - Модуль базового класса для работы с хранилищем самолётов.
- [x] [json_storage.py](src/json_storage.py) - Модуль класса для работы с JSON-хранилищем самолётов.
- [x] [logger_creator.py](src/logger_creator.py) - Модуль реализующий создание логгера.
- [x] [path.py](src/path.py) - Модуль реализующий работу с путями.
- [x] Логирование важных функций
- [x] Написать тесты для всей новой функциональности
- [x] Проверить линтеры (`flake8`, `mypy`, `pydocstyle`, `black`, `isort`)
- [x] Финальная вычитка документации и обновление README
- [x] Обновить документацию

## Команда проекта
- Matvey Bakirov — [mabakirov@gmail.com](mailto:mabakirov@gmail.com) — Back-End Engineer
 
"""Точка входа в приложение."""

from src.aeroplane import Aeroplane
from src.aeroplanes_api import AeroplanesAPI
from src.base_api import BaseAPI
from src.base_storage import BaseStorage
from src.db_initializer import initialize_database
from src.db_manager import DBManager
from src.json_storage import JsonStorage


def input_float(prompt: str) -> float | None:
    """Запрашивает у пользователя ввод дробного числа через консоль.

    Args:
        prompt: Текст приглашения для ввода.

    Returns:
        float
        None: если отказаться от ввода или нажать ввод пропустив ввод.

    Example:
        >>> # При вводе 'y' в консоль:
        >>> input_float("Введите число: ")
        3.14
    """
    raw = input(prompt).strip()
    if not raw:
        return None
    try:
        return float(raw)
    except ValueError:
        print("❌ Введите число или оставьте поле пустым для пропуска")
        return input_float(prompt)


def input_int(prompt: str) -> int | None:
    """Запрашивает у пользователя ввод целого числа через консоль.

    Args:
        prompt: Текст приглашения для ввода.

    Returns:
        int
        None: если отказаться от ввода или нажать ввод пропустив ввод.

    Example:
        >>> # При вводе 'y' в консоль:
        >>> input_int("Введите число: ")
        5
    """
    raw = input(prompt).strip()
    if not raw:
        return None
    try:
        return int(raw)
    except ValueError:
        print("❌ Введите целое число или оставьте поле пустым для пропуска")
        return input_int(prompt)


def input_bool(prompt: str = "(y/n): ") -> bool | None:
    """Запрашивает у пользователя подтверждение действия через консоль.

    Args:
        prompt: Текст приглашения для ввода.

    Returns:
        True при вводе 'y', 'yes', 'д' или 'да'.
        False при вводе 'n', 'no', 'н' или 'нет'.

    Example:
        >>> # При вводе 'y' в консоль:
        >>> input_bool("Вернуть буль? (y/n): ")
        True
    """
    raw = input(prompt).strip().lower()
    if raw in ("y", "yes", "д", "да", "true", "on", "1"):
        return True
    elif raw in ("n", "no", "н", "нет", "false", "off", "0"):
        return False
    elif not raw:
        return None
    else:
        print("❌  Введите 'y' (да) или 'n' (нет) или оставьте поле пустым для пропуска.")
        return input_bool(prompt)


def sort_aeroplanes(aeroplanes: list[Aeroplane]) -> list[Aeroplane]:
    """Сортирует самолёты по убыванию высоты (и скорости при равной высоте)."""
    return sorted(aeroplanes, reverse=True)


def get_top_aeroplanes(aeroplanes: list[Aeroplane], top_n: int) -> list[Aeroplane]:
    """Получает первые top_n самолёта."""
    if top_n > len(aeroplanes):
        return aeroplanes
    else:
        return aeroplanes[:top_n]


def print_aeroplanes(aeroplanes: list[Aeroplane]) -> None:
    """Печатает список самолётов."""
    if isinstance(aeroplanes, list):
        print(f"Печатаем {len(aeroplanes)} самолётов:")
        print(*aeroplanes, sep="\n")


def load_initial_countries(api: BaseAPI, storage: BaseStorage) -> None:
    """Загружает начальные данные по 4+ странам."""
    countries = ["Russia", "Germany", "Turkey", "Poland", "Italy", "Spain", "China", "Japan", "Brazil", "Finnland"]
    storage.initialize()

    print(f"\nЗагрузка данных по {len(countries)} странам...")
    success_count = 0

    for country_name in countries:
        try:
            bbox = api.get_country_bbox(country_name)
            country_id = storage.add_country(country_name, bbox)
            raw_planes = api.get_aeroplanes(country_name)
            planes = Aeroplane.cast_to_object_list(raw_planes, country_id=country_id)
            storage.add_multiple_aeroplanes(planes)
            print(f"  ✅ {country_name}: {len(planes)} самолётов")
            success_count += 1
        except RuntimeError as e:
            print(f"  ❌ {country_name}: {e}")

    print(f"\nЗагружено данных по {success_count} из {len(countries)} стран.")


def user_interaction(api: BaseAPI, storage: BaseStorage) -> None:
    """Функция для взаимодействия с пользователем."""
    country = input("Введите название страны: ")
    # 1. Сохраняем страну (если хранилище поддерживает)
    bbox = None
    country_id = None

    try:
        bbox = api.get_country_bbox(country)
        country_id = storage.add_country(country, bbox)
    except RuntimeError:
        # API недоступен — проверяем хранилище
        country_data = storage.get_country(country)
        if country_data:
            bbox = {
                "lamin": country_data["lat_min"],
                "lamax": country_data["lat_max"],
                "lomin": country_data["lon_min"],
                "lomax": country_data["lon_max"],
            }
            country_id = country_data["id"]
            print(f"Использую данные о стране '{country}' из хранилища.")
        else:
            print("Не удалось определить границы страны, координатный фильтр не будет применён.")

    # 2. Запрашиваем самолёты
    try:
        raw_planes = api.get_aeroplanes(country)
        aeroplanes = Aeroplane.cast_to_object_list(raw_planes, country_id=country_id)
        storage.add_multiple_aeroplanes(aeroplanes)
        print(f"Получено {len(aeroplanes)} самолётов с OpenSky.")
    except RuntimeError as e:
        print(f"Не удалось получить данные: {e}. Использую данные из хранилища.")

    show_statistics(storage)

    # 3. Фильтрация пользователем
    top_n = input_int("Введите количество самолетов для вывода в топ N: ")
    if top_n is None:
        print("Ввод отменён.")
        return
    if top_n <= 0:
        print("Должно быть больше 0. Выход.")
        return

    filters = {}
    if bbox:
        filters["min_latitude"] = bbox["lamin"]
        filters["max_latitude"] = bbox["lamax"]
        filters["min_longitude"] = bbox["lomin"]
        filters["max_longitude"] = bbox["lomax"]
    if origin_country := input("Страна регистрации (Enter чтобы пропустить): ").strip():
        filters["origin_country"] = origin_country
    if min_alt := input_float("Минимальная высота: "):
        filters["min_altitude"] = min_alt
    if max_alt := input_float("Максимальная высота: "):
        filters["max_altitude"] = max_alt
    if min_vel := input_float("Минимальная скорость: "):
        filters["min_velocity"] = min_vel
    if max_vel := input_float("Максимальная скорость: "):
        filters["max_velocity"] = max_vel
    on_ground = input_bool("На земле (да/нет): ")
    if on_ground is not None:
        filters["on_ground"] = on_ground

    filtered = storage.get_aeroplanes(**filters)
    if filtered:
        print(f"Найдено {len(filtered)} соответствующих запросу самолётов.")
    else:
        print("Самолёты, соответствующие запросу, не найдены.")

    sorted_aeroplanes = sort_aeroplanes(filtered)
    top_aeroplanes = get_top_aeroplanes(sorted_aeroplanes, top_n)
    print_aeroplanes(top_aeroplanes)

    print("\n" + "=" * 60)
    print("ПОИСК ПО ПОЗЫВНОМУ (по всем самолетам в хранилище)")
    print("=" * 60)

    callsign_keyword = input("Введите ключевое слово для поиска в позывном (Enter чтобы пропустить): ").strip()
    if callsign_keyword:
        keyword_results = storage.get_aeroplanes_with_keyword(callsign_keyword)
        if keyword_results:
            print(f"\n✅ Найдено {len(keyword_results)} самолётов с '{callsign_keyword}' в позывном:")
            print_aeroplanes(keyword_results[:20])
            if len(keyword_results) > 20:
                print(f"  ... и еще {len(keyword_results) - 20} самолетов")
        else:
            print(f"❌ Самолёты с '{callsign_keyword}' в позывном не найдены.")
    else:
        print("Поиск по позывному пропущен.")


def show_statistics(storage: BaseStorage) -> None:
    """Показывает статистику по самолетам."""
    if not isinstance(storage, DBManager):
        print("Статистика доступна только при работе с БД")
        return

    print("\n" + "=" * 60)
    print("📊 СТАТИСТИКА ПО САМОЛЕТАМ")
    print("=" * 60)

    # 1. Страны и количество самолетов
    countries_stats = storage.get_countries_and_aeroplanes_count()
    print("\n СТРАНЫ И КОЛИЧЕСТВО САМОЛЕТОВ:")
    for item in countries_stats:
        print(f"  {item['name']}: {item['aeroplanes_count']} самолетов")

    # 2. Все самолеты
    all_planes = storage.get_all_aeroplanes()
    print(f"\n ВСЕГО САМОЛЕТОВ: {len(all_planes)}")

    # 3. Средняя скорость
    avg_speed = storage.get_avg_speed()
    print(f"\n  СРЕДНЯЯ СКОРОСТЬ: {avg_speed:.2f} м/с ({avg_speed * 3.6:.2f} км/ч)")

    # 4. Самые быстрые самолеты
    fast_planes = storage.get_aeroplanes_with_higher_speed(5)
    print("\n ТОП-5 САМЫХ БЫСТРЫХ САМОЛЕТОВ:")
    if fast_planes:
        for i, plane in enumerate(fast_planes, 1):
            print(f"  {i}. {plane}")  # ✅ Используем __str__!
    else:
        print("  Нет данных")


def choose_storage() -> BaseStorage:
    """Выбор хранилища пользователем."""
    print("Выберите хранилище:")
    print("1. PostgreSQL (БД)")
    print("2. JSON-файл")

    choice = input("Ваш выбор (1/2): ").strip()

    if choice == "2":
        return JsonStorage("aeroplanes.json")
    return DBManager()


def main() -> None:
    """Основная функция запуска."""
    storage = choose_storage()
    storage.initialize()
    opensky_api = AeroplanesAPI()
    # Загрузка начальных данных
    load_initial_countries(opensky_api, storage)

    # Интерактивный режим
    while True:
        user_interaction(opensky_api, storage)
        if input_bool("\nПродолжить работу? (y/n): ") is False:
            print("До свидания!")
            break

    storage.close()


if __name__ == "__main__":
    initialize_database()
    main()

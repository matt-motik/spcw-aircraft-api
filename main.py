# Создание экземпляра класса для работы с API сайтов с самолетами
from src.base_api import BaseAPI
from src.json_storage import JsonStorage
from src.aeroplane import Aeroplane
from src.aeroplanes_api import AeroplanesAPI

def input_float(prompt: str) -> float | None:
    raw = input(prompt).strip()
    if not raw:
        return None
    try:
        return float(raw)
    except ValueError:
        print("❌ Введите число или оставьте поле пустым для пропуска")
        return input_float(prompt)

def input_int(prompt: str) -> int | None:
    raw = input(prompt).strip()
    if not raw:
        return None
    try:
        return int(raw)
    except ValueError:
        print("❌ Введите целое число или оставьте поле пустым для пропуска")
        return input_int(prompt)

def input_bool(prompt: str = "(y/n): ") -> bool| None:
    """Запрашивает у пользователя подтверждение действия через консоль.

    Args:
        prompt: Текст приглашения для ввода.

    Returns:
        True при вводе 'y', 'yes', 'д' или 'да'.
        False при вводе 'n', 'no', 'н' или 'нет'.

    Example:
        >>> # При вводе 'y' в консоль:
        >>> confirm("Вернуть буль? (y/n): ")
        True
    """
    raw = input(prompt).strip().lower()
    if raw in ("y", "yes", "д", "да", "true", "on","1"):
        return True
    elif raw in ("n", "no", "н", "нет", "false", "off", "0"):
        return False
    elif not raw:
        return None
    else:
        print("Пожалуйста, введите 'y' (да) или 'n' (нет).")
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



def print_aeroplanes(aeroplanes: list[Aeroplane]):
    """Печатает список самолётов"""
    if isinstance(aeroplanes, list):
        print(f"Печатаем {len(aeroplanes)} самолётов:")
        print(*aeroplanes, sep="\n")

# Функция для взаимодействия с пользователем
def user_interaction(api: BaseAPI, storage: JsonStorage) -> None:
    country = input("Введите название страны: ")
    try:
        aeroplanes = api.get_aeroplanes(country)
        aeroplanes = Aeroplane.cast_to_object_list(aeroplanes)
        storage.add_multiple_aeroplanes(aeroplanes)
        print(f"Получено {len(aeroplanes)} самолётов с OpenSky.")
    except RuntimeError as e:
        print(f"Не удалось получить данные: {e}. Использую данные из хранилища.")
    try:
        bbox = api.get_country_bbox(country)
    except RuntimeError:
        bbox = None
        print("Не удалось определить границы страны, координатный фильтр не будет применён.")

    top_n = input_int("Введите количество самолетов для вывода в топ N:")
    if top_n is None:
        print("Ввод отменён.")
        return
    if top_n <= 0:
        print("Должно быть больше 0. Выход.")
        return

    filters = {}
    if bbox:
        filters['min_latitude'] = bbox['lamin']
        filters['max_latitude'] = bbox['lamax']
        filters['min_longitude'] = bbox['lomin']
        filters['max_longitude'] = bbox['lomax']
    if origin_country := input("Страна регистрации (Enter чтобы пропустить): ").strip():
        filters['origin_country'] = origin_country
    if min_alt := input_float("Минимальная высота: "):
        filters['min_altitude'] = min_alt
    if max_alt := input_float("Максимальная высота: "):
        filters['max_altitude'] = max_alt
    if min_vel := input_float("Минимальная скорость: "):
        filters['min_velocity'] = min_vel
    if max_vel := input_float("Максимальная скорость: "):
        filters['max_velocity'] = max_vel
    if on_ground := input_bool("На земле (да/нет): "):
        filters['on_ground'] = on_ground


    filtered = storage.get_aeroplanes(**filters)
    if filtered:
        print(f"Найдено {len(filtered)} соответствующих запросу самолётов.")
    else:
        print("Самолёты, соответствующие запросу, не найдены.")
        return

    sorted_aeroplanes = sort_aeroplanes(filtered)
    top_aeroplanes = get_top_aeroplanes(sorted_aeroplanes, top_n)
    print_aeroplanes(top_aeroplanes)


if __name__ == "__main__":
    json_aeroplanes_storage = JsonStorage("aeroplanes.json")
    opensky_api = AeroplanesAPI()
    user_interaction(opensky_api, json_aeroplanes_storage)
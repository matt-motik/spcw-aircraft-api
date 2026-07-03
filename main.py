# Создание экземпляра класса для работы с API сайтов с самолетами
from src.base_storage import BaseStorage
from src.base_api import BaseAPI
from src.json_storage import JsonStorage
from src.aeroplane import Aeroplane
from src.aeroplanes_api import AeroplanesAPI

# api = AeroplanesAPI()
#
# # Получение информации о самолетах с opensky-network.org
# aeroplanes = api.get_aeroplanes('Spain')
#
# # Преобразование набора данных в список объектов
# aeroplanes = Aeroplane.cast_to_object_list(aeroplanes)
#
# # Пример работы конструктора класса с одним самолетом
# aeroplane = Aeroplane("UAL1621",
#                       "",
#                       "United States",
#                       0,
#                       0,
#                       10203.18,
#                       268.79,
#                       False)
#
# # Сохранение информации в файл
# storage = JsonStorage("aeroplanes.json")
# storage.add_aeroplane(aeroplane)
# storage.delete_aeroplane(aeroplane)


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
        print(*aeroplanes, sep="\n")

# Функция для взаимодействия с пользователем
def user_interaction(api: BaseAPI, storage: JsonStorage) -> None:
    country = input("Введите название страны: ")
    aeroplanes = api.get_aeroplanes(country)
    aeroplanes = Aeroplane.cast_to_object_list(aeroplanes)
    storage.add_multiple_aeroplanes(aeroplanes)

    top_n = int(input("Введите количество самолетов для вывода в топ N: "))

    filters = {}
    if origin_country := input("Страна регистрации (Enter чтобы пропустить): ").strip():
        filters['origin_country'] = origin_country
    if min_alt := input("Минимальная высота: ").strip():
        filters['min_altitude'] = min_alt
    if max_alt := input("Максимальная высота: ").strip():
        filters['max_altitude'] = max_alt
    if min_vel := input("Минимальная скорость: ").strip():
        filters['min_velocity'] = min_vel
    if max_vel := input("Максимальная скорость: ").strip():
        filters['max_velocity'] = max_vel
    if on_ground := input("На земле: ").strip():
        filters['on_ground'] = on_ground


    filtered = storage.get_aeroplanes(**filters)

    sorted_aeroplanes = sort_aeroplanes(filtered)
    top_aeroplanes = get_top_aeroplanes(sorted_aeroplanes, top_n)
    print_aeroplanes(top_aeroplanes)


if __name__ == "__main__":
    json_aeroplanes_storage = JsonStorage("aeroplanes.json")
    opensky_api = AeroplanesAPI()
    user_interaction(opensky_api, json_aeroplanes_storage)
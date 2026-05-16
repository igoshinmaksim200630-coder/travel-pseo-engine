import csv
import os
from config import DATA_FILE, BASE_TRAIN_FARE, PER_KM_TRAIN_COST, BASE_BUS_FARE, PER_KM_BUS_COST

def load_and_process_routes():
    """
    Загружает маршруты из CSV по индексам (так как файл не имеет заголовков),
    валидирует данные и рассчитывает стоимость поездки.
    """
    if not os.path.exists(DATA_FILE):
        raise FileNotFoundError(f"Критическая ошибка: База данных не найдена по пути {DATA_FILE}")

    processed_routes = []

    with open(DATA_FILE, mode='r', encoding='utf-8') as file:
        # Используем обычный reader вместо DictReader
        reader = csv.reader(file)
        
        for row in reader:
            # Пропускаем пустые или неполные строки, чтобы избежать ошибок
            if not row or len(row) < 6:
                continue

            try:
                # В нашей базе дистанция идет 5-м элементом (индекс 4)
                distance = float(row[4])
            except (ValueError, TypeError, IndexError):
                continue

            # 1. Алгоритм расчета цен на Поезд
            train_price = round(BASE_TRAIN_FARE + (distance * PER_KM_TRAIN_COST))
            
            # 2. Алгоритм расчета цен на Автобус
            bus_price = round(BASE_BUS_FARE + (distance * PER_KM_BUS_COST))
            
            # 3. Алгоритм расчета цен на Самолет (только для дистанций > 500 км)
            if distance > 500:
                plane_price = round(24 + (distance * 0.03))
                plane_time = f"{round((distance / 750) + 2.0, 1)} h"
            else:
                plane_price = "N/A"
                plane_time = "N/A (Too close)"

            # Формируем чистый словарь данных для одного маршрута, используя индексы
            route_data = {
                "start": row[0],
                "end": row[1],
                "start_country": row[2],
                "end_country": row[3],
                "distance": distance,
                "train_time": row[5],  # t_time из базы
                "bus_time": f"{round((distance / 75) + 1.0, 1)} h",
                "plane_time": plane_time,
                "train_price": train_price,
                "bus_price": bus_price,
                "plane_price": plane_price,
                "slug": f"how-to-get-from-{row[0].lower()}-to-{row[1].lower()}"
            }
            
            processed_routes.append(route_data)

    print(f" LOG: Дата-движок успешно обработал {len(processed_routes)} маршрутов.")
    return processed_routes
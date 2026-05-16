import csv
import os
from config import DATA_FILE, BASE_TRAIN_FARE, PER_KM_TRAIN_COST, BASE_BUS_FARE, PER_KM_BUS_COST

def load_and_process_routes():
    """
    Загружает маршруты из CSV по индексам, валидирует данные,
    вычищает лишние пробелы и рассчитывает стоимость поездки.
    """
    if not os.path.exists(DATA_FILE):
        raise FileNotFoundError(f"Критическая ошибка: База данных не найдена по пути {DATA_FILE}")

    processed_routes = []

    with open(DATA_FILE, mode='r', encoding='utf-8') as file:
        reader = csv.reader(file)
        
        for row in reader:
            if not row or len(row) < 6:
                continue

            try:
                distance = float(row[4])
            except (ValueError, TypeError, IndexError):
                continue

            # Алгоритмы ценообразования
            train_price = round(BASE_TRAIN_FARE + (distance * PER_KM_TRAIN_COST))
            bus_price = round(BASE_BUS_FARE + (distance * PER_KM_BUS_COST))
            
            if distance > 500:
                plane_price = round(24 + (distance * 0.03))
                plane_time = f"{round((distance / 750) + 2.0, 1)} h"
            else:
                plane_price = "N/A"
                plane_time = "N/A (Too close)"

            # Безопасно вычищаем строки от случайных пробелов на концах
            start_city = row[0].strip()
            end_city = row[1].strip()

            route_data = {
                "start": start_city,
                "end": end_city,
                "start_country": row[2].strip(),
                "end_country": row[3].strip(),
                "distance": distance,
                "train_time": row[5].strip(),
                "bus_time": f"{round((distance / 75) + 1.0, 1)} h",
                "plane_time": plane_time,
                "train_price": train_price,
                "bus_price": bus_price,
                "plane_price": plane_price,
                "slug": f"how-to-get-from-{start_city.lower().replace(' ', '-')}-to-{end_city.lower().replace(' ', '-')}"
            }
            
            processed_routes.append(route_data)

    print(f"⚙️ LOG: Дата-движок успешно обработал {len(processed_routes)} маршрутов.")
    return processed_routes
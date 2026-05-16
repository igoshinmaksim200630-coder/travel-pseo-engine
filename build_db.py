import csv
import itertools
from geopy.distance import geodesic

# Расширенный список топ-35 туристических городов Европы
CITIES = [
    {"name": "London", "country": "United Kingdom", "lat": 51.5074, "lon": -0.1278},
    {"name": "Paris", "country": "France", "lat": 48.8566, "lon": 2.3522},
    {"name": "Berlin", "country": "Germany", "lat": 52.5200, "lon": 13.4050},
    {"name": "Amsterdam", "country": "Netherlands", "lat": 52.3676, "lon": 4.9041},
    {"name": "Rome", "country": "Italy", "lat": 41.9028, "lon": 12.4964},
    {"name": "Madrid", "country": "Spain", "lat": 40.4168, "lon": -3.7038},
    {"name": "Vienna", "country": "Austria", "lat": 48.2082, "lon": 16.3738},
    {"name": "Prague", "country": "Czech Republic", "lat": 50.0755, "lon": 14.4378},
    {"name": "Brussels", "country": "Belgium", "lat": 50.8503, "lon": 4.3517},
    {"name": "Munich", "country": "Germany", "lat": 48.1351, "lon": 11.5820},
    {"name": "Frankfurt", "country": "Germany", "lat": 50.1109, "lon": 8.6821},
    {"name": "Zurich", "country": "Switzerland", "lat": 47.3769, "lon": 8.5417},
    {"name": "Milan", "country": "Italy", "lat": 45.4642, "lon": 9.1900},
    {"name": "Barcelona", "country": "Spain", "lat": 41.3851, "lon": 2.1734},
    {"name": "Hannover", "country": "Germany", "lat": 52.3759, "lon": 9.7320},
    {"name": "Lisbon", "country": "Portugal", "lat": 38.7223, "lon": -9.1393},
    {"name": "Budapest", "country": "Hungary", "lat": 47.4979, "lon": 19.0402},
    {"name": "Warsaw", "country": "Poland", "lat": 52.2297, "lon": 21.0122},
    {"name": "Copenhagen", "country": "Denmark", "lat": 55.6761, "lon": 12.5683},
    {"name": "Stockholm", "country": "Sweden", "lat": 59.3293, "lon": 18.0686},
    {"name": "Vienna", "country": "Austria", "lat": 48.2082, "lon": 16.3738},
    {"name": "Venice", "country": "Italy", "lat": 45.4343, "lon": 12.3388},
    {"name": "Florence", "country": "Italy", "lat": 43.7696, "lon": 11.2558},
    {"name": "Dublin", "country": "Ireland", "lat": 53.3498, "lon": -6.2603},
    {"name": "Edinburgh", "country": "United Kingdom", "lat": 55.9533, "lon": -3.1883},
    {"name": "Oslo", "country": "Norway", "lat": 59.9139, "lon": 10.7522},
    {"name": "Helsinki", "country": "Finland", "lat": 60.1699, "lon": 24.9384},
    {"name": "Krakow", "country": "Poland", "lat": 50.0647, "lon": 19.9450},
    {"name": "Geneva", "country": "Switzerland", "lat": 46.2044, "lon": 6.1432},
    {"name": "Lyon", "country": "France", "lat": 45.7640, "lon": 4.8357},
    {"name": "Marseille", "country": "France", "lat": 43.2965, "lon": 5.3698},
    {"name": "Valencia", "country": "Spain", "lat": 39.4699, "lon": -0.3763},
    {"name": "Porto", "country": "Portugal", "lat": 41.1579, "lon": -8.6291},
    {"name": "Athens", "country": "Greece", "lat": 37.9838, "lon": 23.7275},
    {"name": "Hamburg", "country": "Germany", "lat": 53.5511, "lon": 9.9937}
]

def format_time(hours):
    h = int(hours)
    m = int((hours - h) * 60)
    return f"{h}h {m}m" if h > 0 else f"{m}m"

def generate_routes():
    # Исключаем дубликаты городов с одинаковым именем (например, Вена добавлена дважды)
    unique_cities = {c['name']: c for c in CITIES}.values()
    pairs = list(itertools.permutations(unique_cities, 2))
    
    with open('travel_routes.csv', mode='w', encoding='utf-8', newline='') as file:
        writer = csv.writer(file)
        writer.writerow([
            'from_city', 'to_city', 'country_from', 'country_to', 
            'distance_km', 'train_time', 'train_price', 
            'bus_time', 'bus_price', 'flight_time', 'flight_price',
            'meta_title', 'meta_description', 'slug'
        ])
        
        for start, end in pairs:
            coords_start = (start['lat'], start['lon'])
            coords_end = (end['lat'], end['lon'])
            distance = round(geodesic(coords_start, coords_end).kilometers * 1.25)
            
            if distance < 40: 
                continue
            
            # Наземный транспорт
            t_time = (distance / 120) + 0.5
            t_price = round(19 + (distance * 0.08))
            
            b_time = (distance / 75) + 1.0
            b_price = round(7 + (distance * 0.04))
            
            # Авиа-транспорт (актуален только для дистанций > 500 км)
            if distance > 500:
                f_time = format_time((distance / 750) + 2.0) # 750 км/ч скорость самолета + 2 часа в аэропорту
                f_price = round(24 + (distance * 0.03)) # База 24€ + 0.03€ за км
            else:
                f_time = "N/A (Too close)"
                f_price = "N/A"
            
            slug = f"how-to-get-from-{start['name'].lower()}-to-{end['name'].lower()}"
            
            # Автоматическая генерация уникальных SEO мета-тегов
            meta_title = f"How to Get From {start['name']} to {end['name']}: Budget Travel Guide"
            meta_description = f"Discover the cheapest and fastest ways to travel from {start['name']} ({start['country']}) to {end['name']} ({end['country']}) by train, bus, or flight. Distance: {distance} km."
            
            writer.writerow([
                start['name'], end['name'], start['country'], end['country'], 
                distance, format_time(t_time), t_price, 
                format_time(b_time), b_price, f_time, f_price,
                meta_title, meta_description, slug
            ])

if __name__ == "__main__":
    generate_routes()
    print("СТАНОК ОБНОВЛЕН: Новая база travel_routes.csv создана!")
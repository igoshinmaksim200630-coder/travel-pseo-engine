import os

# Глобальные настройки проекта
BASE_DIR = os.path.dirname(os.path.abspath(__file__))

# Пути к данным и шаблонам
DATA_FILE = os.path.join(BASE_DIR, "travel_routes.csv")
TEMPLATES_DIR = os.path.join(BASE_DIR, "templates")
OUTPUT_DIR = os.path.join(BASE_DIR, "public")

# Настройки сайта (Замени на свой URL после покупки домена, пока оставляем так)
SITE_URL = "https://travel-pseo-engine.pages.dev"
SITE_NAME = "EuroTransit Analytics"

# Параметры партнерской программы (Сюда потом вставим твой реальный ID)
PARTNER_ID = "321456" 
PARTNER_URL_TEMPLATE = "https://omio.sjv.io/c/{partner_id}/123456/9331?u=https://www.omio.com/search-frontend/results?departureStation={start}&arrivalStation={end}"

# Экономика и ценообразование
BASE_TRAIN_FARE = 24  # базовый тариф евро
PER_KM_TRAIN_COST = 0.03

BASE_BUS_FARE = 7
PER_KM_BUS_COST = 0.04
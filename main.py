from modules.db_loader import load_and_process_routes
from modules.html_compiler import compile_site_pages

def main():
    print("🚀 [START] Запуск pSEO-движка нового поколения v2.0...")
    
    # Спринт 1: Дата-инженер собирает и пересчитывает базу данных
    try:
        routes_data = load_and_process_routes()
    except Exception as e:
        print(f"❌ Критическая ошибка при загрузке данных: {e}")
        return

    # Спринт 2: Строитель собирает новые страницы по премиум-шаблонам
    print("📦 Начинаем компиляцию страниц...")
    compile_site_pages(routes_data)
    
    print("🎉 [SUCCESS] Конвейер успешно завершил работу! Проверь папку 'public'.")

if __name__ == "__main__":
    main()
import os
from config import TEMPLATES_DIR, OUTPUT_DIR, SITE_NAME, PARTNER_URL_TEMPLATE, PARTNER_ID

def compile_site_pages(routes_list):
    """
    Берет список обработанных маршрутов и генерирует 
    из них новые HTML-страницы методом безопасной замены .replace()
    """
    os.makedirs(OUTPUT_DIR, exist_ok=True)

    # Загружаем шаблоны
    with open(os.path.join(TEMPLATES_DIR, "base_landing.html"), "r", encoding="utf-8") as f:
        landing_template = f.read()

    with open(os.path.join(TEMPLATES_DIR, "base_route.html"), "r", encoding="utf-8") as f:
        route_template = f.read()

    routes_links_html = []

    # Генерируем внутренние страницы маршрутов
    for route in routes_list:
        partner_url = PARTNER_URL_TEMPLATE.format(
            partner_id=PARTNER_ID,
            start=route['start'].lower(),
            end=route['end'].lower()
        )

        plane_price_display = f"€{route['plane_price']}" if route['plane_price'] != "N/A" else "N/A"

        # Пошагово наполняем шаблон маршрута
        page_html = route_template
        replacements_route = {
            "{site_name}": SITE_NAME,
            "{start}": route['start'],
            "{end}": route['end'],
            "{start_country}": route['start_country'],
            "{end_country}": route['end_country'],
            "{distance}": str(route['distance']),
            "{train_time}": route['train_time'],
            "{bus_time}": route['bus_time'],
            "{plane_time}": route['plane_time'],
            "{train_price}": str(route['train_price']),
            "{bus_price}": str(route['bus_price']),
            "{plane_price_display}": plane_price_display,
            "{partner_url}": partner_url
        }
        
        for placeholder, value in replacements_route.items():
            page_html = page_html.replace(placeholder, value)

        route_filename = f"{route['slug']}.html"
        with open(os.path.join(OUTPUT_DIR, route_filename), "w", encoding="utf-8") as f:
            f.write(page_html)

        # Создаем плитку-ссылку для главной страницы
        link_card = f"""
        <a href="{route_filename}" class="bg-white border border-slate-200 p-5 rounded-2xl shadow-sm hover:shadow-md hover:border-indigo-500 transition flex items-center justify-between group">
            <div>
                <div class="font-bold text-slate-900 group-hover:text-indigo-600 transition">{route['start']} → {route['end']}</div>
                <div class="text-xs text-slate-400 font-medium mt-1">{route['distance']} km • {route['start_country']}</div>
            </div>
            <i data-lucide="chevron-right" class="w-5 h-5 text-slate-300 group-hover:text-indigo-500 group-hover:translate-x-1 transition-all"></i>
        </a>
        """
        routes_links_html.append(link_card)

    # Собираем главную страницу (index.html)
    all_links_string = "\n".join(routes_links_html)
    
    compiled_landing_html = landing_template
    replacements_landing = {
        "{site_name}": SITE_NAME,
        "{routes_links}": all_links_string
    }
    
    for placeholder, value in replacements_landing.items():
        compiled_landing_html = compiled_landing_html.replace(placeholder, value)

    with open(os.path.join(OUTPUT_DIR, "index.html"), "w", encoding="utf-8") as f:
        f.write(compiled_landing_html)

    print(f"📦 LOG: Компилятор успешно собрал {len(routes_links_html)} веб-страниц в папке 'public'!")
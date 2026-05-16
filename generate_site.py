import csv
import os
from jinja2 import Environment, FileSystemLoader

os.makedirs("public", exist_ok=True)
env = Environment(loader=FileSystemLoader('.'))
template = env.get_template('template.html')

def build_site():
    count = 0
    routes_list = []

    # 1. Читаем базу данных
    with open('travel_routes.csv', mode='r', encoding='utf-8') as file:
        reader = csv.DictReader(file)
        for row in reader:
            # Генерируем отдельную страницу маршрута
            html_output = template.render(**row)
            file_path = f"public/{row['slug']}.html"
            with open(file_path, 'w', encoding='utf-8') as out_file:
                out_file.write(html_output)
            
            # Сохраняем данные для главной страницы и карты сайта
            routes_list.append({
                'title': f"{row['from_city']} to {row['to_city']}",
                'slug': f"{row['slug']}.html"
            })
            count += 1

    # 2. АВТО-ГЕНЕРАЦИЯ ГЛАВНОЙ СТРАНИЦЫ (Каталог для Google)
    index_html = """
    <!DOCTYPE html>
    <html lang="en">
    <head>
        <meta charset="UTF-8">
        <title>European Travel & Transport Directory</title>
        <style>
            body { font-family: -apple-system, sans-serif; max-width: 900px; margin: 0 auto; padding: 40px; background: #f7fafc; }
            h1 { color: #1a365d; text-align: center; }
            .grid { display: grid; grid-template-columns: repeat(auto-fill, minmax(250px, 1fr)); gap: 15px; margin-top: 30px; }
            a { background: white; padding: 15px; border-radius: 6px; text-decoration: none; color: #2b6cb0; font-weight: 500; border: 1px solid #e2e8f0; text-align: center; box-shadow: 0 2px 4px rgba(0,0,0,0.02); }
            a:hover { background: #e2e8f0; }
        </style>
    </head>
    <body>
        <h1>European Transport Route Directory</h1>
        <div class="grid">
    """
    for route in routes_list:
        index_html += f'        <a href="{route["slug"]}">{route["title"]}</a>\n'
    
    index_html += """    </div>
    </body>
    </html>"""
    
    with open("public/index.html", "w", encoding="utf-8") as index_file:
        index_file.write(index_html)

    # 3. АВТО-ГЕНЕРАЦИЯ SITEMAP.XML (Документ, который мы скормим Google)
    # Замени 'https://yourdomain.pages.dev' на свой будущий URL от Cloudflare
    site_url = "https://yourdomain.pages.dev" 
    sitemap_xml = '<?xml version="1.0" encoding="UTF-8"?>\n<urlset xmlns="http://www.sitemaps.org/schemas/sitemap/0.9">\n'
    
    # Добавляем главную страницу в карту
    sitemap_xml += f'  <url>\n    <loc>{site_url}/</loc>\n    <priority>1.0</priority>\n  </url>\n'
    
    # Добавляем все 1122 страницы
    for route in routes_list:
        sitemap_xml += f'  <url>\n    <loc>{site_url}/{route["slug"]}</loc>\n    <priority>0.8</priority>\n  </url>\n'
    sitemap_xml += '</urlset>'
    
    with open("public/sitemap.xml", "w", encoding="utf-8") as sitemap_file:
        sitemap_file.write(sitemap_xml)

    print(f"ГОТОВО: 1122 страницы, index.html и sitemap.xml успешно созданы в папке 'public'!")

if __name__ == "__main__":
    build_site()
from jinja2 import Environment, FileSystemLoader
from pathlib import Path

# Загружаем шаблоны из папки templates/
env = Environment(
    loader=FileSystemLoader("templates"),
    autoescape=False  # Markdown уже HTML — не экранируем
)

# Загружаем шаблоны
page_template = env.get_template("page.html")
base_template = env.get_template("base.html")

def render_page(title, content, date=None):
    """
    Собирает финальный HTML.
    title — строка
    content — HTML после markdown
    date — опциональная дата из front matter
    """

    # Рендер внутренней части (page.html)
    inner_html = page_template.render(
        title=title,
        content=content,
        date=date
    )

    # Вставляем получившийся фрагмент в base.html
    final_html = base_template.render(
        title=title,
        content=inner_html
    )

    return final_html

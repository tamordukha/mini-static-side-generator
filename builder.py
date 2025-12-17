from pathlib import Path
import shutil
import os
import time
from http.server import HTTPServer, SimpleHTTPRequestHandler

from parser import parse_markdown_file 
from renderer import render_page        

CONTENT_DIR = Path("content")
SITE_DIR = Path("site")
ASSETS_DIR = Path("assets")

# --- BUILD ---
def build(force=False):
    print("Build started!")
    """
    Собирает сайт.
    force=True  -> пересобрать все файлы, игнорируя mtime.
    """
    SITE_DIR.mkdir(parents=True, exist_ok=True)
    copied = copy_assets()

    print(f"Building site -> {SITE_DIR} (force={force})")
    built = 0
    skipped = 0

    for md_path in CONTENT_DIR.rglob("*.md"):
        # относительный путь внутри content, чтобы сохранить структуру
        rel = md_path.relative_to(CONTENT_DIR)
        out_path = SITE_DIR / rel.with_suffix(".html")
        out_path.parent.mkdir(parents=True, exist_ok=True)

        # инкрементальная проверка: если html старше md - пересобрать
        if not force and out_path.exists():
            md_mtime = md_path.stat().st_mtime
            html_mtime = out_path.stat().st_mtime
            if html_mtime >= md_mtime:
                skipped += 1
                print(f"Skip (unchanged): {rel} -> {out_path.name}")
                continue

        # парсим md
        parsed = parse_markdown_file(md_path)
        title = parsed.get("metadata", {}).get("title") or md_path.stem
        date = parsed.get("metadata", {}).get("date")
        content_html = parsed.get("content", "None")

        # рендерим финальную страницу
        final_html = render_page(title=title, content=content_html, date=date)

        # сохраняем
        out_path.write_text(final_html, encoding="utf-8")
        built += 1
        print(f"Built: {rel} -> {out_path}")

    print(f"Done. Built: {built}. Skipped: {skipped}. Assets copied: {copied}.")


# --- CLEAN ---
def clean():
    """Удаляет папку site/ и создаёт её заново пустой."""
    if SITE_DIR.exists():
        print(f"Removing {SITE_DIR} ...")
        shutil.rmtree(SITE_DIR)
    SITE_DIR.mkdir(parents=True, exist_ok=True)
    print(f"Created empty {SITE_DIR}")


# --- ASSETS COPY ---
def copy_assets():
    """
    Копирует папку assets/ -> site/assets/.
    Возвращает True если скопировано, False если assets/ не найден.
    """
    if not ASSETS_DIR.exists():
        return False

    dest = SITE_DIR / ASSETS_DIR.name

    try:
        shutil.copytree(ASSETS_DIR, dest, dirs_exist_ok=True)
    except TypeError:
        if dest.exists():
            shutil.rmtree(dest)
        shutil.copytree(ASSETS_DIR, dest)
    print(f"Copied assets: {ASSETS_DIR} -> {dest}")
    return True


# --- SERVE ---
def serve(host="127.0.0.1", port=8000):
    """
    Запускает локальный HTTP-сервер, который обслуживает папку site/.
    Блокирует поток до Ctrl+C.
    """
    if not SITE_DIR.exists():
        print("Site directory does not exist. Run build() first.")
        return

    os.chdir("site")
    server = HTTPServer(("localhost", 8000), SimpleHTTPRequestHandler)

    print("Serving at http://localhost:8000")
    print("Press CTRL+C to stop")

    try:
        server.serve_forever()
    except KeyboardInterrupt:
        print("\nServer stopped")
    finally:
        server.server_close()





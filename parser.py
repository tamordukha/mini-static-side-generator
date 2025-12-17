import re
from pathlib import Path
import markdown


FRONT_MATTER_PATTERN = re.compile(r"^---\n(.*?)\n---\n(.*)$", re.DOTALL)


def parse_markdown_file(path: Path) -> dict:
    """Читает .md файл, возвращает dict: {content_html, metadata}"""

    text = path.read_text(encoding="utf-8")

    metadata = {}
    markdown_text = text

    # 1) Парсим front-matter (если есть)
    match = FRONT_MATTER_PATTERN.match(text)
    if match:
        raw_meta = match.group(1)
        markdown_text = match.group(2)

        metadata = parse_front_matter(raw_meta)

    # 2) Превращаем Markdown → HTML
    html = markdown.markdown(
        markdown_text,
        extensions=["fenced_code", "tables"]
    )

    return {
        "content": html,
        "metadata": metadata
    }


def parse_front_matter(raw_meta: str) -> dict:
    
    metadata = {}

    for line in raw_meta.split("\n"):
        if ":" not in line:
            continue

        key, value = line.split(":", 1)
        key = key.strip()
        value = value.strip()

        # массивы вида [a, b, c]
        if value.startswith("[") and value.endswith("]"):
            value = value[1:-1].strip()
            if value:
                value = [item.strip() for item in value.split(",")]
            else:
                value = []

        metadata[key] = value

    return metadata

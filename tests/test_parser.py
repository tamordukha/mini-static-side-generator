from parser import parse_front_matter, parse_markdown_file
import re
import tempfile
import pathlib as Path

FRONT_MATTER_PATTERN = re.compile(r"^---\n(.*?)\n---\n(.*)$", re.DOTALL)

def test_parse_front_matter():
    raw_meta = """
    title: My Page
    date: 2025-12-01
    tags: [python, blog]
    """

    result_meta = parse_front_matter(raw_meta)
    test_title = result_meta["title"]
    test_date = result_meta["date"]
    test_tags = result_meta["tags"]

    assert test_title=="My Page"
    assert test_date=="2025-12-01"
    assert test_tags==["python", "blog"]


def test_parse_markdown_file():
    md_content = """
    ---
    title: My project
    date: 2025-12-17
    tags: [python, blog]
    ---
    # Заголовок статьи
    Это основной текст в формате **Markdown**.
    """

    with tempfile.NamedTemporaryFile(mode="w", suffix=".md", encoding="utf-8", delete=True) as tmp:
        tmp.write(md_content)
        tmp.flush()

        path = Path(tmp.name)
        result = parse_markdown_file(path)

        # Проверяем metadata
        assert result["metadata"]["title"] == "My project"
        assert result["metadata"]["date"] == "2025-12-17"
        assert result["metadata"]["tags"] == ["python", "blog"]

        # Проверяем, что контент стал HTML
        assert "<h1>" in result["content"]
        assert "<strong>" in result["content"]

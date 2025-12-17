from renderer import render_page

def test_render_page_basic():
    html = render_page(
        title="Test Page",
        content="<p>Hello</p>",
        date="2025-01-01"
    )

    assert isinstance(html, str)
    assert "Test Page" in html
    assert "<p>Hello</p>" in html
    assert "2025-01-01" in html

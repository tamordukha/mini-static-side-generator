# Mini Static Site Generator

A simple static site generator written in Python.  
It converts Markdown files into HTML using Jinja2 templates and builds a fully static website.

## Features
- Markdown to HTML conversion
- Front-matter metadata support (title, date, tags)
- Jinja2 templating (base and page templates)
- Static asset copying (CSS, images)
- CLI commands: build, clean, serve
- Local development server
- Unit tests with pytest
- CI pipeline with GitHub Actions

## Project Structure
- `content/` — Markdown pages
- `templates/` — HTML templates
- `site/` — Generated static site
- `parser.py` — Markdown & metadata parsing
- `renderer.py` — HTML rendering
- `builder.py` — Site building logic
- `cli.py` — Command line interface

## Usage

python cli.py build
python cli.py serve

Open your browser at:
http://localhost:8000/

## Requirements

Python 3.10+

## Author

Tamerlan Ordukhanov


Built as a learning project to understand static site generators.
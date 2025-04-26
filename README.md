# 🕸️ Web Scraper CLI

A versatile command-line web scraper for extracting content from websites with support for various selectors, formats, and pagination.

## ✨ Features

- 🌐 Scrape content from any website
- 🔍 Extract specific elements using CSS selectors
- 📊 Save data in multiple formats (text, JSON, CSV)
- 📃 Navigate through paginated content
- 🤖 Respect robots.txt by default
- ⏱️ Configurable delay between requests to avoid overloading servers
- 🧩 Extract specific attributes from HTML elements
- 🔄 Customize user agent and request parameters

## 📋 Requirements

- Python 3.6 or higher
- requests library
- beautifulsoup4 library

## 🚀 Installation

1. Clone this repository:
```bash
git clone https://github.com/0xAthen4/web-scraper-cli.git
cd web-scraper-cli
```

2. Install requirements:
```bash
pip install -r requirements.txt
```

3. Make the script executable (Unix/Linux/macOS):
```bash
chmod +x main.py
```

## 🔍 Usage

```bash
python main.py <URL> [options]
```

## ⚙️ Options

### Basic Options:
- `url`: URL to scrape (required)
- `-s, --selector`: CSS selector to extract specific elements
- `-a, --attributes`: Comma-separated list of attributes to extract (text, html, href, src, etc.)
- `-f, --format`: Output format (text, json, csv)
- `-o, --output`: Output file path

### Request Options:
- `-u, --user-agent`: User-Agent string
- `-t, --timeout`: Request timeout in seconds (default: 30)
- `-d, --delay`: Delay between requests in seconds (default: 2)
- `--no-robots`: Ignore robots.txt

### Pagination Options:
- `-p, --pages`: Maximum number of pages to scrape (default: 1)
- `-n, --next-page`: CSS selector for the next page link

### Other Options:
- `-v, --verbose`: Verbose output
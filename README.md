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

## 📝 Examples

### Extract all paragraphs from a webpage:
```bash
python main.py https://example.com -s "p"
```

### Extract headlines with their text:
```bash
python main.py https://example.com -s "h1, h2, h3" -a text
```

### Extract links with their URLs and text:
```bash
bashpython main.py https://example.com -s "a" -a href,text
```

### Extract images with their source URLs and alt text:
```bash
python main.py https://example.com -s "img" -a src,alt
```

### Save output to a JSON file:
```bash
python main.py https://example.com -s "article" -f json -o articles.json
```

### Extract data from a paginated site (5 pages):
```bash
python main.py https://example.com/page/1 -s ".post" -p 5 -n ".pagination a.next"
```

### Extract product information from an e-commerce site:
```bash
python main.py https://example.com/products -s ".product" -a text,html -f csv -o products.csv
```

### Download full HTML content:
```bash
python main.py https://example.com -o website.html
```

### Use a custom user agent:
```bash
python main.py https://example.com -u "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36"
```

## 🧩 Advanced Usage

### Using Complex CSS Selectors

You can use advanced CSS selectors to target specific elements:

- Select elements by class:
  ```bash
  python main.py https://example.com -s ".classname"
  ```
  
- Select elements by ID:
  ```bash
  python main.py https://example.com -s "#elementid"
  ```
  
-  Select elements by attribute:
  ```bash
  python main.py https://example.com -s "a[target='_blank']"
  ```
  
-  Combine selectors:
  ```bash
  python main.py https://example.com -s "article.post h2, article.post p:first-child"
  ```
  
### Extracting Specific Attributes
The `-a` option allows you to extract specific attributes from elements:

- `text`: Get the text content of an element
- `html`: Get the HTML content of an element
- `href`: Get the href attribute of links
- `src`: Get the src attribute of images/media
- Any other HTML attribute: `class`, `id`, `title`, etc.

### Pagination Strategies
For sites with different pagination structures:

- Next button with a specific class:
  ```bash
  python main.py https://example.com -n ".pagination .next"
  ```

- Next button with specific text:
  ```bash
  python main.py https://example.com -n "a:contains('Next')"
  ```

- Page number links:
  ```bash
  python main.py https://example.com -n ".pagination a:last-child"
  ```
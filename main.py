#!/usr/bin/env python3

import argparse
import os
import sys
import json
import csv
import time
import random
import requests
from bs4 import BeautifulSoup
from urllib.parse import urlparse, urljoin
import urllib.robotparser
from datetime import datetime

# Default values
DEFAULT_TIMEOUT = 30
DEFAULT_DELAY = 2
DEFAULT_USER_AGENT = "Mozilla/5.0 (compatible; PythonWebScraper/1.0; +https://github.com/yourusername/web-scraper)"

class WebScraper:
    def __init__(self, url, selector=None, attributes=None, output_format="text", 
                 output_file=None, user_agent=DEFAULT_USER_AGENT, timeout=DEFAULT_TIMEOUT, 
                 delay=DEFAULT_DELAY, respect_robots=True, max_pages=1, next_page=None, 
                 verbose=False):
        self.url = url
        self.selector = selector
        self.attributes = attributes.split(",") if attributes else []
        self.output_format = output_format
        self.output_file = output_file
        self.user_agent = user_agent
        self.timeout = timeout
        self.delay = delay
        self.respect_robots = respect_robots
        self.max_pages = max_pages
        self.next_page = next_page
        self.verbose = verbose
        self.data = []
        self.session = requests.Session()
        self.session.headers.update({"User-Agent": user_agent})
        
    def log(self, message):
        """Print message if verbose mode is enabled"""
        if self.verbose:
            print(f"[{datetime.now().strftime('%H:%M:%S')}] {message}")
    
    def can_fetch(self, url):
        """Check if the URL can be fetched according to robots.txt"""
        if not self.respect_robots:
            return True
        
        parsed_url = urlparse(url)
        robots_url = f"{parsed_url.scheme}://{parsed_url.netloc}/robots.txt"
        
        try:
            rp = urllib.robotparser.RobotFileParser()
            rp.set_url(robots_url)
            rp.read()
            return rp.can_fetch(self.user_agent, url)
        except Exception as e:
            self.log(f"Error checking robots.txt: {e}")
            return True  # If we can't check robots.txt, assume it's okay to fetch
    
    def fetch_page(self, url):
        """Fetch a page and return its content"""
        if not self.can_fetch(url):
            print(f"Error: robots.txt disallows access to {url}")
            return None
        
        try:
            self.log(f"Fetching {url}")
            response = self.session.get(url, timeout=self.timeout)
            response.raise_for_status()
            return response.text
        except requests.RequestException as e:
            print(f"Error fetching {url}: {e}")
            return None
    
    def extract_data(self, html, selector):
        """Extract data from HTML using the given CSS selector"""
        soup = BeautifulSoup(html, 'html.parser')
        elements = soup.select(selector) if selector else [soup]
        
        page_data = []
        for element in elements:
            item = {}
            
            # If no attributes specified, get text or full HTML
            if not self.attributes:
                item["content"] = element.get_text(strip=True) if selector else str(element)
                page_data.append(item)
                continue
            
            # Extract specified attributes
            for attr in self.attributes:
                if attr == "text":
                    item[attr] = element.get_text(strip=True)
                elif attr == "html":
                    item[attr] = str(element)
                elif attr == "href" and element.name == "a":
                    item[attr] = element.get("href", "")
                elif attr == "src" and element.name in ["img", "iframe", "video", "source"]:
                    item[attr] = element.get("src", "")
                else:
                    item[attr] = element.get(attr, "")
            
            page_data.append(item)
        
        return page_data
    
    def find_next_page(self, html, current_url):
        """Find the URL of the next page using the provided selector"""
        if not self.next_page:
            return None
        
        soup = BeautifulSoup(html, 'html.parser')
        next_elements = soup.select(self.next_page)
        
        if not next_elements:
            return None
        
        # Try to find href attribute in the element or its children
        next_url = None
        for element in next_elements:
            if element.name == "a":
                next_url = element.get("href")
            else:
                links = element.find_all("a")
                if links:
                    next_url = links[0].get("href")
            
            if next_url:
                break
        
        if not next_url:
            return None
        
        # Make sure the URL is absolute
        return urljoin(current_url, next_url)
    
    def scrape(self):
        """Scrape data from the website"""
        current_url = self.url
        pages_scraped = 0
        
        while current_url and pages_scraped < self.max_pages:
            # Delay between requests
            if pages_scraped > 0:
                delay = self.delay + random.uniform(0, 1)
                self.log(f"Waiting for {delay:.2f} seconds before next request")
                time.sleep(delay)
            
            # Fetch the page
            html = self.fetch_page(current_url)
            if not html:
                break
            
            # Extract data from the page
            if self.selector:
                page_data = self.extract_data(html, self.selector)
                self.data.extend(page_data)
                self.log(f"Extracted {len(page_data)} items from {current_url}")
            else:
                self.data.append({"url": current_url, "html": html})
                self.log(f"Saved full HTML from {current_url}")
            
            # Increment the counter
            pages_scraped += 1
            
            # Find the next page if pagination is enabled
            if pages_scraped < self.max_pages and self.next_page:
                current_url = self.find_next_page(html, current_url)
                if not current_url:
                    self.log("No next page found, stopping")
                    break
            else:
                current_url = None
        
        self.log(f"Finished scraping {pages_scraped} pages")
        return self.data
    
    def save_data(self):
        """Save the scraped data to a file"""
        if not self.output_file:
            self.print_data()
            return
        
        if self.output_format == "json":
            self.save_as_json()
        elif self.output_format == "csv":
            self.save_as_csv()
        else:  # text
            self.save_as_text()
    
    def print_data(self):
        """Print the scraped data to the console"""
        if not self.data:
            print("No data extracted")
            return
        
        if self.output_format == "json":
            print(json.dumps(self.data, indent=2))
        elif self.output_format == "csv":
            if not self.attributes and not self.selector:
                for item in self.data:
                    print(item.get("html", ""))
            else:
                fields = list(self.data[0].keys())
                print(",".join(fields))
                for item in self.data:
                    print(",".join(f'"{str(item.get(field, "")).replace("""", """""")}"' for field in fields))
        else:  # text
            if not self.attributes and not self.selector:
                for item in self.data:
                    print(item.get("html", ""))
            else:
                for item in self.data:
                    if "text" in item:
                        print(item["text"])
                    elif "content" in item:
                        print(item["content"])
                    else:
                        print(str(item))
    
    def save_as_json(self):
        """Save the scraped data as JSON"""
        try:
            with open(self.output_file, 'w', encoding='utf-8') as f:
                json.dump(self.data, f, indent=2, ensure_ascii=False)
            print(f"Data saved to {self.output_file} in JSON format")
        except Exception as e:
            print(f"Error saving data to {self.output_file}: {e}")
    
    def save_as_csv(self):
        """Save the scraped data as CSV"""
        try:
            if not self.data:
                print("No data to save")
                return
            
            # Determine CSV fields
            if not self.attributes and not self.selector:
                fields = ["url", "html"]
            else:
                fields = list(self.data[0].keys())
            
            with open(self.output_file, 'w', newline='', encoding='utf-8') as f:
                writer = csv.DictWriter(f, fieldnames=fields)
                writer.writeheader()
                writer.writerows(self.data)
            
            print(f"Data saved to {self.output_file} in CSV format")
        except Exception as e:
            print(f"Error saving data to {self.output_file}: {e}")
    
    def save_as_text(self):
        """Save the scraped data as plain text"""
        try:
            with open(self.output_file, 'w', encoding='utf-8') as f:
                if not self.attributes and not self.selector:
                    for item in self.data:
                        f.write(item.get("html", "") + "\n\n")
                else:
                    for item in self.data:
                        if "text" in item:
                            f.write(item["text"] + "\n\n")
                        elif "content" in item:
                            f.write(item["content"] + "\n\n")
                        else:
                            f.write(str(item) + "\n\n")
            
            print(f"Data saved to {self.output_file} in text format")
        except Exception as e:
            print(f"Error saving data to {self.output_file}: {e}")

def main():
    parser = argparse.ArgumentParser(description="A versatile web scraper command-line tool")
    
    # Required arguments
    parser.add_argument("url", help="URL to scrape")
    
    # Selector options
    parser.add_argument("-s", "--selector", help="CSS selector to extract specific elements")
    parser.add_argument("-a", "--attributes", help="Comma-separated list of attributes to extract (text, html, href, src, etc.)")
    
    # Output options
    parser.add_argument("-f", "--format", choices=["text", "json", "csv"], default="text", help="Output format (default: text)")
    parser.add_argument("-o", "--output", help="Output file path")
    
    # Request options
    parser.add_argument("-u", "--user-agent", default=DEFAULT_USER_AGENT, help="User-Agent string")
    parser.add_argument("-t", "--timeout", type=int, default=DEFAULT_TIMEOUT, help=f"Request timeout in seconds (default: {DEFAULT_TIMEOUT})")
    parser.add_argument("-d", "--delay", type=float, default=DEFAULT_DELAY, help=f"Delay between requests in seconds (default: {DEFAULT_DELAY})")
    parser.add_argument("--no-robots", action="store_true", help="Ignore robots.txt")
    
    # Pagination options
    parser.add_argument("-p", "--pages", type=int, default=1, help="Maximum number of pages to scrape (default: 1)")
    parser.add_argument("-n", "--next-page", help="CSS selector for the next page link")
    
    # Other options
    parser.add_argument("-v", "--verbose", action="store_true", help="Verbose output")
    
    args = parser.parse_args()
    
    # Create and run the scraper
    scraper = WebScraper(
        url=args.url,
        selector=args.selector,
        attributes=args.attributes,
        output_format=args.format,
        output_file=args.output,
        user_agent=args.user_agent,
        timeout=args.timeout,
        delay=args.delay,
        respect_robots=not args.no_robots,
        max_pages=args.pages,
        next_page=args.next_page,
        verbose=args.verbose
    )
    
    scraper.scrape()
    scraper.save_data()

if __name__ == "__main__":
    main()

#!/usr/bin/env python3
"""
TechGuideHQ Web Scraping & Asset Extraction Tool
Extracts titles, headings, links, and forms from target web pages.
Author: TechGuideHQ (@TechGuideHQ1)
License: MIT
"""

import sys
import urllib.request
import urllib.error
from html.parser import HTMLParser
from urllib.parse import urljoin, urlparse

class SimpleHTMLParser(HTMLParser):
    def __init__(self, base_url):
        super().__init__()
        self.base_url = base_url
        self.title = ""
        self.in_title = False
        self.headings = []
        self.current_heading = None
        self.links = []
        self.forms_detected = 0

    def handle_starttag(self, tag, attrs):
        if tag == 'title':
            self.in_title = True
        elif tag in ['h1', 'h2', 'h3']:
            self.current_heading = tag
        elif tag == 'a':
            for name, value in attrs:
                if name == 'href' and value:
                    full_url = urljoin(self.base_url, value)
                    if full_url not in self.links:
                        self.links.append(full_url)
        elif tag == 'form':
            self.forms_detected += 1

    def handle_endtag(self, tag):
        if tag == 'title':
            self.in_title = False
        elif tag in ['h1', 'h2', 'h3']:
            self.current_heading = None

    def handle_data(self, data):
        cleaned_data = data.strip()
        if not cleaned_data:
            return
        if self.in_title:
            self.title += cleaned_data
        elif self.current_heading in ['h1', 'h2', 'h3']:
            self.headings.append(f"[{self.current_heading.upper()}] {cleaned_data}")

class Colors:
    CYAN = '\033[96m'
    GREEN = '\033[92m'
    WARNING = '\033[93m'
    FAIL = '\033[91m'
    RESET = '\033[0m'
    BOLD = '\033[1m'

def scrape_website(target_url):
    if not target_url.startswith('http://') and not target_url.startswith('https://'):
        target_url = 'https://' + target_url

    print(f"\n{Colors.BOLD}[*] Scraping target: {target_url}{Colors.RESET}")
    
    req = urllib.request.Request(
        target_url,
        headers={'User-Agent': 'Mozilla/5.0 (TechGuideHQ-Scraper/1.0)'}
    )

    try:
        with urllib.request.urlopen(req, timeout=10) as response:
            html_content = response.read().decode('utf-8', errors='ignore')
            
            parser = SimpleHTMLParser(target_url)
            parser.feed(html_content)

            print(f"\n{Colors.GREEN}[+] Page Title:{Colors.RESET} {parser.title or 'No title found'}")
            print(f"{Colors.GREEN}[+] Forms Detected:{Colors.RESET} {parser.forms_detected}")
            
            print(f"\n{Colors.CYAN}[--- Headings Extracted ({len(parser.headings)}) ---]{Colors.RESET}")
            for h in parser.headings[:10]: # Display first 10 headings
                print(f"  {h}")

            print(f"\n{Colors.CYAN}[--- Hyperlinks Discovered ({len(parser.links)}) ---]{Colors.RESET}")
            for link in parser.links[:10]: # Display first 10 links
                print(f"  -> {link}")

    except urllib.error.HTTPError as e:
        print(f"{Colors.FAIL}[!] HTTP Error {e.code}: Failed to retrieve page.{Colors.RESET}")
    except urllib.error.URLError as e:
        print(f"{Colors.FAIL}[!] Connection Error: {e.reason}{Colors.RESET}")
    except Exception as e:
        print(f"{Colors.FAIL}[!] Unexpected Error: {e}{Colors.RESET}")

def main():
    if len(sys.argv) < 2:
        target = input(f"{Colors.BOLD}[?] Enter website URL to scrape: {Colors.RESET}").strip()
        if not target:
            target = "https://example.com"
    else:
        target = sys.argv[1]

    scrape_website(target)
    print(f"\n{Colors.GREEN}[✓] Scraping Operation Complete.{Colors.RESET}\n")

if __name__ == "__main__":
    main()

#!/usr/bin/env python3
"""
TechGuideHQ Elite Recursive Web Crawler & Asset Hunter (Requests Edition)
Uses the requests library for robust TLS handling, session management, and scraping.
Author: TechGuideHQ (@TechGuideHQ1)
License: MIT
"""

import sys
import re
import json
from urllib.parse import urlparse, urljoin
from html.parser import HTMLParser

try:
    import requests
except ImportError:
    print("[!] Error: 'requests' module not found. Install it via: pip install requests")
    sys.exit(1)

class BeastParser(HTMLParser):
    def __init__(self, base_url):
        super().__init__()
        self.base_url = base_url
        self.title = ""
        self.in_title = False
        self.links = set()
        self.forms = []
        self.current_form = None
        self.comments = []

    def handle_starttag(self, tag, attrs):
        attrs_dict = dict(attrs)
        if tag == 'title':
            self.in_title = True
        elif tag == 'a' and 'href' in attrs_dict:
            full_url = urljoin(self.base_url, attrs_dict['href'])
            if urlparse(full_url).netloc == urlparse(self.base_url).netloc:
                self.links.add(full_url)
        elif tag == 'form':
            self.current_form = {'action': attrs_dict.get('action', ''), 'method': attrs_dict.get('method', 'get').upper(), 'inputs': []}
            self.forms.append(self.current_form)
        elif tag == 'input' and self.current_form is not None:
            self.current_form['inputs'].append({
                'name': attrs_dict.get('name', ''),
                'type': attrs_dict.get('type', 'text'),
                'value': attrs_dict.get('value', '')
            })

    def handle_endtag(self, tag):
        if tag == 'title':
            self.in_title = False
        elif tag == 'form':
            self.current_form = None

    def handle_data(self, data):
        if self.in_title:
            self.title += data.strip()

    def handle_comment(self, data):
        cleaned = data.strip()
        if cleaned:
            self.comments.append(cleaned)

class Colors:
    CYAN = '\033[96m'
    GREEN = '\033[92m'
    WARNING = '\033[93m'
    FAIL = '\033[91m'
    RESET = '\033[0m'
    BOLD = '\033[1m'

def beast_crawl(start_url, max_pages=5):
    if not start_url.startswith('http://') and not start_url.startswith('https://'):
        start_url = 'https://' + start_url

    visited = set()
    queue = [start_url]
    master_report = {'target': start_url, 'pages_scanned': []}

    print(f"\n{Colors.BOLD}[*] Initializing Requests Beast Crawler on: {start_url}{Colors.RESET}")

    session = requests.Session()
    session.headers.update({
        'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/122.0.0.0 Safari/537.36',
        'Accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,image/webp,*/*;q=0.8',
        'Accept-Language': 'en-US,en;q=0.5',
    })

    while queue and len(visited) < max_pages:
        url = queue.pop(0)
        if url in visited:
            continue
        
        visited.add(url)
        print(f"  {Colors.CYAN}[+] Crawling ({len(visited)}/{max_pages}): {url}{Colors.RESET}")

        try:
            # timeout set to 12 seconds, allowing SSL verify bypass if strict firewalls interfere
            resp = session.get(url, timeout=12, verify=True)
            html = resp.text
            
            parser = BeastParser(url)
            parser.feed(html)

            emails = list(set(re.findall(r'[a-zA-Z0-9._%+-]+@[a-zA-Z0-9.-]+\.[a-zA-Z]{2,}', html)))
            phones = list(set(re.findall(r'\+?[0-9][0-9()\-\s]{7,}[0-9]', html)))
            secrets = list(set(re.findall(r'(?:api[_-]?key|secret|token|auth)[=:]["\']([a-zA-Z0-9_\-]{16,})["\']', html, re.IGNORECASE)))

            page_data = {
                'url': url,
                'status_code': resp.status_code,
                'title': parser.title,
                'forms': parser.forms,
                'comments': parser.comments,
                'extracted_emails': emails,
                'extracted_phones': phones,
                'potential_secrets': secrets
            }
            master_report['pages_scanned'].append(page_data)
            print(f"    {Colors.GREEN}[✓] Successfully scraped (Status: {resp.status_code}){Colors.RESET}")

            for link in parser.links:
                if link not in visited:
                    queue.append(link)

        except requests.exceptions.SSLError:
            print(f"    {Colors.WARNING}[!] SSL Certificate verification failed on {url}. Retrying without verification...{Colors.RESET}")
            try:
                resp = session.get(url, timeout=12, verify=False)
                html = resp.text
                parser = BeastParser(url)
                parser.feed(html)
                master_report['pages_scanned'].append({
                    'url': url, 'status_code': resp.status_code, 'title': parser.title, 'forms': parser.forms, 'comments': parser.comments
                })
                print(f"    {Colors.GREEN}[✓] Scraped successfully with SSL verification disabled.{Colors.RESET}")
            except Exception as e:
                print(f"    {Colors.FAIL}[!] Bypass failed: {e}{Colors.RESET}")
        except Exception as e:
            print(f"    {Colors.FAIL}[!] Request Error on {url}: {e}{Colors.RESET}")

    print(f"\n{Colors.GREEN}[✓] Crawl Complete. Saving structured report...{Colors.RESET}")
    report_filename = "beast_scan_report.json"
    with open(report_filename, 'w') as f:
        json.dump(master_report, f, indent=4)
    print(f"  {Colors.BOLD}[+] Report saved to: {report_filename}{Colors.RESET}")

    total_forms = sum(len(p.get('forms', [])) for p in master_report['pages_scanned'])
    print(f"  {Colors.GREEN}[✓] Total Pages Scanned Successfully:{Colors.RESET} {len(master_report['pages_scanned'])}")
    print(f"  {Colors.GREEN}[✓] Total Forms Mapped:{Colors.RESET} {total_forms}")

def main():
    if len(sys.argv) < 2:
        target = input(f"{Colors.BOLD}[?] Enter target domain to beast crawl: {Colors.RESET}").strip()
        if not target:
            target = "https://example.com"
    else:
        target = sys.argv[1]

    beast_crawl(target)

if __name__ == "__main__":
    main()

#!/usr/bin/env python3
"""
TechGuideHQ Advanced Recon & Attack Surface Engine
Professional-Grade Enumeration, CORS Auditing & Header Security Suite
Author: TechGuideHQ (@TechGuideHQ1)
License: MIT
"""

import sys
import socket
import ssl
import urllib.request
import urllib.error
from urllib.parse import urlparse
import concurrent.futures

class EliteColors:
    HEADER = '\033[95m'
    CYAN = '\033[96m'
    GREEN = '\033[92m'
    WARNING = '\033[93m'
    FAIL = '\033[91m'
    RESET = '\033[0m'
    BOLD = '\033[1m'
    DIM = '\033[2m'

def print_elite_banner():
    print(f"""{EliteColors.CYAN}{EliteColors.BOLD}
====================================================================
           TECHGUIDEHQ ELITE ATTACK SURFACE RECON ENGINE            
        Offensive Recon, Defensive Auditing & CORS Analysis         
===================================================================={EliteColors.RESET}""")

def audit_cors(url):
    print(f"\n{EliteColors.BOLD}[*] Auditing Cross-Origin Resource Sharing (CORS) Misconfigurations...{EliteColors.RESET}")
    test_origin = "https://evil-attacker-domain.com"
    req = urllib.request.Request(
        url,
        headers={
            'User-Agent': 'Mozilla/5.0 (TechGuideHQ-SecurityScanner/3.0)',
            'Origin': test_origin
        }
    )
    try:
        with urllib.request.urlopen(req, timeout=8) as resp:
            acao = resp.headers.get('Access-Control-Allow-Origin')
            acac = resp.headers.get('Access-Control-Allow-Credentials')
            
            if acao == '*':
                print(f"  {EliteColors.WARNING}[!] Vulnerability Found: Wildcard CORS ('*') enabled. Any origin can read data.{EliteColors.RESET}")
            elif acao == test_origin:
                print(f"  {EliteColors.FAIL}[!] Critical Misconfiguration: Reflected Origin! The server trusts arbitrary malicious origins ('{test_origin}').{EliteColors.RESET}")
                if acac == 'true':
                    print(f"  {EliteColors.FAIL}[!] CRITICAL: Access-Control-Allow-Credentials is set to TRUE with reflected origin! Full session hijacking vector.{EliteColors.RESET}")
            else:
                print(f"  {EliteColors.GREEN}[✓] CORS Policy Appears Secure (Origin isolated).{EliteColors.RESET}")
    except Exception as e:
        print(f"  {EliteColors.DIM}[i] CORS probe skipped or blocked: {e}{EliteColors.RESET}")

def perform_deep_recon(target):
    if not target.startswith('http://') and not target.startswith('https://'):
        url = 'https://' + target
        domain = target
    else:
        url = target
        domain = urlparse(target).netloc

    print(f"\n{EliteColors.BOLD}[+] Initializing Target Profile: {domain}{EliteColors.RESET}")
    
    # 1. DNS & Network Footprinting
    try:
        ip = socket.gethostbyname(domain)
        print(f"  {EliteColors.GREEN}[✓] Resolved IPv4 Address:{EliteColors.RESET} {ip}")
    except socket.gaierror as e:
        print(f"  {EliteColors.FAIL}[!] DNS Resolution Failed:{EliteColors.RESET} {e}")
        return

    # 2. Deep SSL Cipher & Certificate Audit
    print(f"  {EliteColors.CYAN}[*] Performing Deep TLS Handshake Inspection...{EliteColors.RESET}")
    ctx = ssl.create_default_context()
    try:
        with socket.create_connection((domain, 443), timeout=8) as sock:
            with ctx.wrap_socket(sock, server_hostname=domain) as ssock:
                cert = ssock.getpeercert()
                cipher = ssock.cipher()
                issuer = dict(x[0] for x in cert.get('issuer', []))
                print(f"    {EliteColors.GREEN}[✓] Cipher Suite:{EliteColors.RESET} {cipher[0]} ({cipher[1]} bits)")
                print(f"    {EliteColors.GREEN}[✓] Certificate Issuer:{EliteColors.RESET} {issuer.get('organizationName', 'Unknown')}")
                print(f"    {EliteColors.GREEN}[✓] Expiration Date:{EliteColors.RESET} {cert.get('notAfter')}")
    except Exception as e:
        print(f"    {EliteColors.WARNING}[!] TLS Handshake Warning / WAF Blocked: {e}{EliteColors.RESET}")

    # 3. Comprehensive Header & Security Posture Audit
    print(f"  {EliteColors.CYAN}[*] Running Strict Security Header Enumeration...{EliteColors.RESET}")
    try:
        req = urllib.request.Request(url, headers={'User-Agent': 'Mozilla/5.0 (TechGuideHQ-SecurityScanner/3.0)'})
        with urllib.request.urlopen(req, timeout=8) as resp:
            headers = dict(resp.headers)
            controls = {
                'Strict-Transport-Security': 'Protects against protocol downgrade attacks (HSTS)',
                'Content-Security-Policy': 'Mitigates Cross-Site Scripting (XSS) & Data Injection',
                'X-Frame-Options': 'Prevents Clickjacking UI redressing',
                'X-Content-Type-Options': 'Blocks MIME-sniffing vulnerabilities',
                'Permissions-Policy': 'Restricts sensitive browser API access'
            }
            
            for header, desc in controls.items():
                if headers.get(header) or headers.get(header.lower()):
                    print(f"    {EliteColors.GREEN}[Secure] {header}{EliteColors.RESET}")
                else:
                    print(f"    {EliteColors.WARNING}[Vulnerable/Missing] {header} -> {desc}{EliteColors.RESET}")
    except Exception as e:
        print(f"    {EliteColors.FAIL}[!] Header Audit Refused/Timed out: {e}{EliteColors.RESET}")

    # 4. Run Advanced CORS Check
    audit_cors(url)

def main():
    print_elite_banner()
    if len(sys.argv) < 2:
        target = input(f"{EliteColors.BOLD}[?] Enter target domain for elite reconnaissance: {EliteColors.RESET}").strip()
        if not target:
            target = "example.com"
    else:
        target = sys.argv[1]

    perform_deep_recon(target)
    print(f"\n{EliteColors.CYAN}[✓] Elite Reconnaissance Scan Complete.{EliteColors.RESET}\n")

if __name__ == "__main__":
    main()

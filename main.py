#!/usr/bin/env python3
"""
TechGuideHQ Toolkit - Master Command Center (Elite Edition)
Unified Interface for Offensive Recon, CORS Auditing & Automation
Author: TechGuideHQ (@TechGuideHQ1)
License: MIT
"""

import sys
import os

class Colors:
    CYAN = '\033[96m'
    GREEN = '\033[92m'
    WARNING = '\033[93m'
    FAIL = '\033[91m'
    RESET = '\033[0m'
    BOLD = '\033[1m'

def print_banner():
    print(f"""{Colors.CYAN}{Colors.BOLD}
====================================================================
           TECHGUIDEHQ MASTER TOOLKIT & SECURITY LAB (ELITE)        
        Offensive Recon, Attack Surface Analysis & Automation       
===================================================================={Colors.RESET}""")

def main():
    while True:
        print_banner()
        print(f"{Colors.BOLD}Select an Operational Module:{Colors.RESET}")
        print("  [1] Run Elite Attack Surface Recon & CORS Audit")
        print("  [2] Run Media Watermarking Automation")
        print("  [3] Exit Toolkit")
        
        choice = input(f"\n{Colors.CYAN}TechGuideHQ-Toolkit (Elite) > {Colors.RESET}").strip()
        
        if choice == '1':
            target = input(f"\n{Colors.BOLD}[?] Enter target domain (e.g., target.com): {Colors.RESET}").strip()
            if target:
                os.system(f"python3 automation/pro_recon_engine.py {target}")
            else:
                os.system("python3 automation/pro_recon_engine.py example.com")
        elif choice == '2':
            watermark_script = "automation/watermark_images.py"
            if os.path.exists(watermark_script):
                os.system(f"python3 {watermark_script}")
            else:
                print(f"  {Colors.FAIL}[!] Error: Watermarking script missing.{Colors.RESET}")
        elif choice == '3':
            print(f"\n{Colors.GREEN}[*] Shutting down Toolkit. Stay secure, stay elite.{Colors.RESET}\n")
            break
        else:
            print(f"{Colors.FAIL}[!] Invalid selection.{Colors.RESET}")
        
        input(f"\n{Colors.BOLD}[Press Enter to return to main menu]{Colors.RESET}")

if __name__ == "__main__":
    main()

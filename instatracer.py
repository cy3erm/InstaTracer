#!/usr/bin/env python3
"""
InstaTracer - Instagram Intelligence Tool
Educational security research tool
Created by CyberM
"""

import requests
import json
import re
import time
import random
import uuid
import os
import sys
from datetime import datetime
from colorama import init, Fore, Style

init(autoreset=True)

def clear_screen():
    os.system('clear' if os.name == 'posix' else 'cls')

def show_banner():
    banner = f"""
{Fore.CYAN}{Style.BRIGHT}
╔═══════════════════════════════════════════════════════════════════════════════════════════════════════╗
║           $$$$$$\                       $$\            $$$$$$$$\                                      ║
║           \_$$  _|                      $$ |           \__$$  __|                                     ║
║             $$ |  $$$$$$$\   $$$$$$$\ $$$$$$\    $$$$$$\  $$ | $$$$$$\  $$$$$$\   $$$$$$$\  $$$$$$\   ║
║             $$ |  $$  __$$\ $$  _____|\_$$  _|   \____$$\ $$ |$$  __$$\ \____$$\ $$  _____|$$  __$$\  ║
║             $$ |  $$ |  $$ |\$$$$$$\    $$ |     $$$$$$$ |$$ |$$ |  \__|$$$$$$$ |$$ /      $$$$$$$$ | ║
║             $$ |  $$ |  $$ | \____$$\   $$ |$$\ $$  __$$ |$$ |$$ |     $$  __$$ |$$ |      $$   ____| ║
║          $$$$$$\ $$ |  $$ |$$$$$$$  |  \$$$$  |\$$$$$$$ |$$ |$$ |     \$$$$$$$ |\$$$$$$$\ \$$$$$$$\   ║
║          \______|\__|  \__|\_______/    \____/  \_______|\__|\__|      \_______| \_______| \_______|  ║
║                         Instagram Intelligence Tool                                                   ║
║                         Created by CyberM                                                             ║
║                                                                                                       ║
╠═══════════════════════════════════════════════════════════════════════════════════════════════════════╣
║                                                                                                       ║
║  {Fore.GREEN}[1]{Fore.WHITE} Check Single Account                                                                             ║
║  {Fore.GREEN}[2]{Fore.WHITE} Bulk Check from File                                                                             ║
║  {Fore.GREEN}[3]{Fore.WHITE} View Statistics                                                                                  ║
║  {Fore.GREEN}[4]{Fore.WHITE} Export Results                                                                                   ║
║  {Fore.GREEN}[5]{Fore.WHITE} Clear Screen                                                                                     ║
║  {Fore.GREEN}[0]{Fore.WHITE} Exit                                                                                             ║
║                                                                                                       ║
╚═══════════════════════════════════════════════════════════════════════════════════════════════════════╝
{Style.RESET_ALL}
"""
    print(banner)

COUNTRY_CODES = {
    '+1': 'USA/Canada', '+34': 'Spain', '+212': 'Morocco', '+213': 'Algeria',
    '+44': 'United Kingdom', '+33': 'France', '+49': 'Germany', '+39': 'Italy',
    '+351': 'Portugal', '+91': 'India', '+86': 'China', '+81': 'Japan',
    '+55': 'Brazil', '+61': 'Australia', '+7': 'Russia', '+20': 'Egypt',
    '+90': 'Turkey', '+966': 'Saudi Arabia', '+971': 'UAE', '+972': 'Israel',
}

EMAIL_PROVIDERS = {
    'gmail.com': 'Google', 'yahoo.com': 'Yahoo', 'hotmail.com': 'Microsoft',
    'outlook.com': 'Microsoft', 'protonmail.com': 'ProtonMail', 'icloud.com': 'Apple',
}

USER_AGENTS = [
    'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36',
    'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/537.36',
]


class InstaTracer:
    def __init__(self, verbose=False):
        self.verbose = verbose
        self.session = requests.Session()
        self.results = []
        self._update_headers()

    def _update_headers(self):
        self.session.headers.update({
            'user-agent': random.choice(USER_AGENTS),
            'accept': '*/*',
            'content-type': 'application/x-www-form-urlencoded',
        })

    def _get_csrf(self):
        try:
            self.session.get('https://www.instagram.com/', timeout=10)
            return self.session.cookies.get('csrftoken')
        except:
            return None

    def _extract_country(self, phone):
        if not phone:
            return None, None
        match = re.match(r'(\+\d{1,4})', phone)
        if match:
            code = match.group(1)
            for prefix, country in COUNTRY_CODES.items():
                if phone.startswith(prefix):
                    return prefix, country
            return code, COUNTRY_CODES.get(code, 'Unknown')
        return None, None

    def check_account(self, username):
        time.sleep(random.uniform(1, 1.5))
        csrf = self._get_csrf()
        if not csrf:
            return None
        self.session.headers.update({'x-csrftoken': csrf})
        variables = {
            "params": {
                "event_request_id": str(uuid.uuid4()),
                "next_uri": "",
                "search_query": username,
                "waterfall_id": str(uuid.uuid4())
            }
        }
        data = {
            "variables": json.dumps(variables),
            "doc_id": "26178667145161478"
        }
        try:
            response = self.session.post(
                'https://www.instagram.com/api/graphql',
                data=data,
                timeout=15
            )
            if response.status_code == 429:
                return None
            if response.status_code != 200:
                return None
            result = response.json()
            search = result.get('data', {}).get('caa_ar_ig_account_search', {})
            if search.get('cipher'):
                return {
                    'exists': True,
                    'contact_points': search.get('contact_points', [])
                }
            return {'exists': False}
        except Exception as e:
            if self.verbose:
                print(f"{Fore.RED}[-] Error: {e}")
            return None

    def get_profile(self, username):
        """Get profile info - same headers as working curl"""
        
        time.sleep(random.uniform(1.5, 2.5))
        
        try:
            # Create a new session for profile request
            profile_session = requests.Session()
            
            url = f"https://i.instagram.com/api/v1/users/web_profile_info/?username={username}"
            
            # EXACT headers that curl used (working)
            profile_session.headers.update({
                'User-Agent': 'Instagram 269.0.0.18.80 (iPhone; iOS 16_5; en_US; en; scale=3.00; 1170x2532; 428809312)',
                'Accept': 'application/json',
                'X-IG-App-ID': '936619743392459',
            })
            
            response = profile_session.get(url, timeout=10)
            
            if response.status_code == 200:
                data = response.json()
                user = data.get('data', {}).get('user', {})
                
                if self.verbose:
                    print(f"{Fore.GREEN}[+] Profile loaded: {user.get('full_name', username)}")
                
                return {
                    'followers': user.get('edge_followed_by', {}).get('count', 0),
                    'following': user.get('edge_follow', {}).get('count', 0),
                    'posts': user.get('edge_owner_to_timeline_media', {}).get('count', 0),
                    'is_verified': user.get('is_verified', False),
                    'is_private': user.get('is_private', False),
                    'full_name': user.get('full_name', ''),
                    'bio': user.get('biography', '')[:300],
                }
            else:
                if self.verbose:
                    print(f"{Fore.YELLOW}[!] Profile API returned {response.status_code}")
                
        except Exception as e:
            if self.verbose:
                print(f"{Fore.YELLOW}[!] Profile error: {e}")
        
        return {}

    def analyze(self, username):
        result = {
            'username': username,
            'exists': False,
            'email': None,
            'email_provider': None,
            'phone': None,
            'country': None,
            'followers': 0,
            'following': 0,
            'posts': 0,
            'is_verified': False,
            'is_private': False,
            'full_name': '',
            'bio': '',
            'timestamp': datetime.now().isoformat()
        }
        
        check = self.check_account(username)
        if not check or not check.get('exists'):
            return result
        
        result['exists'] = True
        
        for contact in check.get('contact_points', []):
            if contact.get('type') == 'EMAIL':
                result['email'] = contact.get('contact_point')
                if result['email'] and '@' in result['email']:
                    domain = result['email'].split('@')[1].lower()
                    result['email_provider'] = EMAIL_PROVIDERS.get(domain, domain)
            elif contact.get('type') == 'PHONE':
                result['phone'] = contact.get('contact_point')
                _, country = self._extract_country(result['phone'])
                result['country'] = country
        
        profile = self.get_profile(username)
        result.update(profile)
        
        return result

    def print_result(self, result):
        if not result['exists']:
            print(f"\n{Fore.RED}❌ {result['username']}: Account does not exist")
            return
        
        print(f"\n{Fore.GREEN}{Style.BRIGHT}✅ {result['username']}: Account exists!{Style.RESET_ALL}")
        
        if result['full_name']:
            print(f"   {Fore.CYAN}👤 Name:{Fore.WHITE} {result['full_name']}")
        if result['bio']:
            bio = result['bio'][:80] + '...' if len(result['bio']) > 80 else result['bio']
            print(f"   {Fore.CYAN}📝 Bio:{Fore.WHITE} {bio}")
        
        if result['followers']:
            print(f"   {Fore.CYAN}👥 Followers:{Fore.WHITE} {result['followers']:,}")
            print(f"   {Fore.CYAN}🔄 Following:{Fore.WHITE} {result['following']:,}")
            print(f"   {Fore.CYAN}📸 Posts:{Fore.WHITE} {result['posts']:,}")
        
        if result['is_private']:
            print(f"   {Fore.YELLOW}🔒 Private account")
        if result['is_verified']:
            print(f"   {Fore.BLUE}✓ Verified")
        
        if result['email']:
            print(f"   {Fore.CYAN}📧 Email:{Fore.WHITE} {result['email']} ({result['email_provider']})")
        if result['phone']:
            print(f"   {Fore.CYAN}📱 Phone:{Fore.WHITE} {result['phone']}")
        if result['country']:
            print(f"   {Fore.CYAN}🌍 Country:{Fore.WHITE} {result['country']}")

    def single_check(self):
        clear_screen()
        show_banner()
        username = input(f"\n{Fore.CYAN}[?] Enter Instagram username: {Fore.WHITE}").strip()
        if not username:
            print(f"{Fore.RED}[-] Username required")
            input(f"\n{Fore.YELLOW}Press Enter to continue...")
            return
        print(f"\n{Fore.YELLOW}[*] Checking {username}...{Fore.WHITE}")
        result = self.analyze(username)
        self.print_result(result)
        self.results.append(result)
        input(f"\n{Fore.YELLOW}Press Enter to continue...")

    def bulk_check(self):
        clear_screen()
        show_banner()
        filename = input(f"\n{Fore.CYAN}[?] Enter filename with usernames (one per line): {Fore.WHITE}").strip()
        if not os.path.exists(filename):
            print(f"{Fore.RED}[-] File not found: {filename}")
            input(f"\n{Fore.YELLOW}Press Enter to continue...")
            return
        with open(filename, 'r') as f:
            usernames = [line.strip() for line in f if line.strip()]
        print(f"\n{Fore.GREEN}[+] Loaded {len(usernames)} usernames{Fore.WHITE}")
        for i, username in enumerate(usernames):
            print(f"\n{Fore.YELLOW}[{i+1}/{len(usernames)}] Checking {username}...{Fore.WHITE}")
            result = self.analyze(username)
            self.print_result(result)
            self.results.append(result)
        input(f"\n{Fore.YELLOW}Press Enter to continue...")

    def show_stats(self):
        clear_screen()
        show_banner()
        if not self.results:
            print(f"\n{Fore.YELLOW}[!] No results yet. Run some checks first.{Fore.WHITE}")
            input(f"\n{Fore.YELLOW}Press Enter to continue...")
            return
        accounts = [r for r in self.results if r['exists']]
        print(f"\n{Fore.CYAN}{'='*50}")
        print(f"{Fore.CYAN}📊 STATISTICS{Fore.WHITE}")
        print(f"{Fore.CYAN}{'='*50}")
        print(f"Total checks: {len(self.results)}")
        print(f"Accounts found: {len(accounts)}")
        if accounts:
            countries = {}
            for r in accounts:
                if r['country']:
                    countries[r['country']] = countries.get(r['country'], 0) + 1
            if countries:
                print(f"\n{Fore.YELLOW}🌍 Country Distribution:{Fore.WHITE}")
                for country, count in sorted(countries.items(), key=lambda x: x[1], reverse=True):
                    print(f"   {country}: {count}")
        input(f"\n{Fore.YELLOW}Press Enter to continue...")

    def export_results(self):
        clear_screen()
        show_banner()
        if not self.results:
            print(f"\n{Fore.YELLOW}[!] No results to export.{Fore.WHITE}")
            input(f"\n{Fore.YELLOW}Press Enter to continue...")
            return
        filename = input(f"\n{Fore.CYAN}[?] Export filename (default: results.json): {Fore.WHITE}").strip()
        if not filename:
            filename = "results.json"
        with open(filename, 'w') as f:
            json.dump(self.results, f, indent=2, default=str)
        print(f"\n{Fore.GREEN}[+] Results saved to {filename}{Fore.WHITE}")
        input(f"\n{Fore.YELLOW}Press Enter to continue...")


def main():
    tracer = InstaTracer(verbose=True)  # Enable verbose to see debug output
    while True:
        clear_screen()
        show_banner()
        choice = input(f"\n{Fore.CYAN}[?] Select option (0-5): {Fore.WHITE}").strip()
        if choice == '1':
            tracer.single_check()
        elif choice == '2':
            tracer.bulk_check()
        elif choice == '3':
            tracer.show_stats()
        elif choice == '4':
            tracer.export_results()
        elif choice == '5':
            clear_screen()
            show_banner()
        elif choice == '0':
            clear_screen()
            print(f"\n{Fore.GREEN}👋 Thanks for using InstaTracer - CyberM{Fore.WHITE}\n")
            sys.exit(0)
        else:
            print(f"\n{Fore.RED}[-] Invalid option{Fore.WHITE}")
            time.sleep(1)


if __name__ == '__main__':
    main()

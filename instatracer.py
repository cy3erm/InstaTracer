#!/usr/bin/env python3
"""
InstaTracer - Instagram Intelligence Tool
Educational security research tool
"""

import requests
import json
import re
import time
import random
import argparse
import uuid
from datetime import datetime
from colorama import init, Fore, Style

init(autoreset=True)

COUNTRY_CODES = {
    '+1': 'USA/Canada',
    '+7': 'Russia/Kazakhstan',
    '+20': 'Egypt',
    '+27': 'South Africa',
    '+30': 'Greece',
    '+31': 'Netherlands',
    '+32': 'Belgium',
    '+33': 'France',
    '+34': 'Spain',
    '+36': 'Hungary',
    '+39': 'Italy',
    '+40': 'Romania',
    '+41': 'Switzerland',
    '+43': 'Austria',
    '+44': 'United Kingdom',
    '+45': 'Denmark',
    '+46': 'Sweden',
    '+47': 'Norway',
    '+48': 'Poland',
    '+49': 'Germany',
    '+51': 'Peru',
    '+52': 'Mexico',
    '+53': 'Cuba',
    '+54': 'Argentina',
    '+55': 'Brazil',
    '+56': 'Chile',
    '+57': 'Colombia',
    '+58': 'Venezuela',
    '+60': 'Malaysia',
    '+61': 'Australia',
    '+62': 'Indonesia',
    '+63': 'Philippines',
    '+64': 'New Zealand',
    '+65': 'Singapore',
    '+66': 'Thailand',
    '+81': 'Japan',
    '+82': 'South Korea',
    '+84': 'Vietnam',
    '+86': 'China',
    '+90': 'Turkey',
    '+91': 'India',
    '+92': 'Pakistan',
    '+93': 'Afghanistan',
    '+94': 'Sri Lanka',
    '+95': 'Myanmar',
    '+98': 'Iran',
    '+212': 'Morocco',
    '+213': 'Algeria',
    '+216': 'Tunisia',
    '+218': 'Libya',
    '+220': 'Gambia',
    '+221': 'Senegal',
    '+222': 'Mauritania',
    '+223': 'Mali',
    '+224': 'Guinea',
    '+225': 'Ivory Coast',
    '+226': 'Burkina Faso',
    '+227': 'Niger',
    '+228': 'Togo',
    '+229': 'Benin',
    '+230': 'Mauritius',
    '+231': 'Liberia',
    '+232': 'Sierra Leone',
    '+233': 'Ghana',
    '+234': 'Nigeria',
    '+235': 'Chad',
    '+236': 'Central African Republic',
    '+237': 'Cameroon',
    '+238': 'Cape Verde',
    '+239': 'Sao Tome',
    '+240': 'Equatorial Guinea',
    '+241': 'Gabon',
    '+242': 'Republic of Congo',
    '+243': 'DR Congo',
    '+244': 'Angola',
    '+245': 'Guinea-Bissau',
    '+246': 'Diego Garcia',
    '+247': 'Ascension Island',
    '+248': 'Seychelles',
    '+249': 'Sudan',
    '+250': 'Rwanda',
    '+251': 'Ethiopia',
    '+252': 'Somalia',
    '+253': 'Djibouti',
    '+254': 'Kenya',
    '+255': 'Tanzania',
    '+256': 'Uganda',
    '+257': 'Burundi',
    '+258': 'Mozambique',
    '+260': 'Zambia',
    '+261': 'Madagascar',
    '+262': 'Reunion',
    '+263': 'Zimbabwe',
    '+264': 'Namibia',
    '+265': 'Malawi',
    '+266': 'Lesotho',
    '+267': 'Botswana',
    '+268': 'Eswatini',
    '+269': 'Comoros',
    '+290': 'Saint Helena',
    '+291': 'Eritrea',
    '+297': 'Aruba',
    '+298': 'Faroe Islands',
    '+299': 'Greenland',
    '+350': 'Gibraltar',
    '+351': 'Portugal',
    '+352': 'Luxembourg',
    '+353': 'Ireland',
    '+354': 'Iceland',
    '+355': 'Albania',
    '+356': 'Malta',
    '+357': 'Cyprus',
    '+358': 'Finland',
    '+359': 'Bulgaria',
    '+370': 'Lithuania',
    '+371': 'Latvia',
    '+372': 'Estonia',
    '+373': 'Moldova',
    '+374': 'Armenia',
    '+375': 'Belarus',
    '+376': 'Andorra',
    '+377': 'Monaco',
    '+378': 'San Marino',
    '+379': 'Vatican City',
    '+380': 'Ukraine',
    '+381': 'Serbia',
    '+382': 'Montenegro',
    '+383': 'Kosovo',
    '+385': 'Croatia',
    '+386': 'Slovenia',
    '+387': 'Bosnia and Herzegovina',
    '+389': 'North Macedonia',
    '+420': 'Czech Republic',
    '+421': 'Slovakia',
    '+423': 'Liechtenstein',
    '+500': 'Falkland Islands',
    '+501': 'Belize',
    '+502': 'Guatemala',
    '+503': 'El Salvador',
    '+504': 'Honduras',
    '+505': 'Nicaragua',
    '+506': 'Costa Rica',
    '+507': 'Panama',
    '+508': 'Saint Pierre and Miquelon',
    '+509': 'Haiti',
    '+590': 'Guadeloupe',
    '+591': 'Bolivia',
    '+592': 'Guyana',
    '+593': 'Ecuador',
    '+594': 'French Guiana',
    '+595': 'Paraguay',
    '+596': 'Martinique',
    '+597': 'Suriname',
    '+598': 'Uruguay',
    '+599': 'Netherlands Antilles',
    '+670': 'East Timor',
    '+672': 'Australian External Territories',
    '+673': 'Brunei',
    '+674': 'Nauru',
    '+675': 'Papua New Guinea',
    '+676': 'Tonga',
    '+677': 'Solomon Islands',
    '+678': 'Vanuatu',
    '+679': 'Fiji',
    '+680': 'Palau',
    '+681': 'Wallis and Futuna',
    '+682': 'Cook Islands',
    '+683': 'Niue',
    '+685': 'Samoa',
    '+686': 'Kiribati',
    '+687': 'New Caledonia',
    '+688': 'Tuvalu',
    '+689': 'French Polynesia',
    '+690': 'Tokelau',
    '+691': 'Micronesia',
    '+692': 'Marshall Islands',
    '+800': 'International Freephone',
    '+808': 'International Shared Cost',
    '+850': 'North Korea',
    '+852': 'Hong Kong',
    '+853': 'Macau',
    '+855': 'Cambodia',
    '+856': 'Laos',
    '+870': 'Inmarsat',
    '+878': 'Universal Personal Telecommunications',
    '+880': 'Bangladesh',
    '+881': 'Mobile Satellite System',
    '+882': 'International Networks',
    '+886': 'Taiwan',
    '+960': 'Maldives',
    '+961': 'Lebanon',
    '+962': 'Jordan',
    '+963': 'Syria',
    '+964': 'Iraq',
    '+965': 'Kuwait',
    '+966': 'Saudi Arabia',
    '+967': 'Yemen',
    '+968': 'Oman',
    '+970': 'Palestine',
    '+971': 'United Arab Emirates',
    '+972': 'Israel',
    '+973': 'Bahrain',
    '+974': 'Qatar',
    '+975': 'Bhutan',
    '+976': 'Mongolia',
    '+977': 'Nepal',
    '+992': 'Tajikistan',
    '+993': 'Turkmenistan',
    '+994': 'Azerbaijan',
    '+995': 'Georgia',
    '+996': 'Kyrgyzstan',
    '+998': 'Uzbekistan',
}

EMAIL_PROVIDERS = {
    'gmail.com': 'Google',
    'yahoo.com': 'Yahoo',
    'hotmail.com': 'Microsoft',
    'outlook.com': 'Microsoft',
    'protonmail.com': 'ProtonMail',
    'icloud.com': 'Apple',
    'aol.com': 'AOL',
    'mail.com': 'Mail.com',
    'yandex.com': 'Yandex',
    'mail.ru': 'Mail.ru',
    'qq.com': 'QQ',
    '163.com': 'NetEase',
    'zoho.com': 'Zoho',
    'fastmail.com': 'Fastmail',
    'gmx.com': 'GMX',
}

USER_AGENTS = [
    'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36',
    'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/537.36',
]


class InstaTracer:
    def __init__(self, verbose=False):
        self.verbose = verbose
        self.session = requests.Session()
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
        try:
            session = requests.Session()
            url = f"https://i.instagram.com/api/v1/users/web_profile_info/?username={username}"

            session.headers.update({
                'User-Agent': 'Instagram 269.0.0.18.80 (iPhone; iOS 16_5; en_US; en; scale=3.00; 1170x2532; 428809312)',
                'Accept': 'application/json',
                'X-IG-App-ID': '936619743392459',
            })

            response = session.get(url, timeout=10)

            if response.status_code == 200:
                data = response.json()
                user = data.get('data', {}).get('user', {})

                return {
                    'followers': user.get('edge_followed_by', {}).get('count', 0),
                    'following': user.get('edge_follow', {}).get('count', 0),
                    'posts': user.get('edge_owner_to_timeline_media', {}).get('count', 0),
                    'is_verified': user.get('is_verified', False),
                    'is_private': user.get('is_private', False),
                    'full_name': user.get('full_name', ''),
                    'bio': user.get('biography', '')[:300],
                }

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
            print(f"{Fore.RED}❌ {result['username']}: Account does not exist")
            return

        print(f"\n{Fore.GREEN}✅ {result['username']}: Account exists!")

        if result['full_name']:
            print(f"   👤 Name: {result['full_name']}")

        if result['bio']:
            bio = result['bio'][:80] + '...' if len(result['bio']) > 80 else result['bio']
            print(f"   📝 Bio: {bio}")

        if result['followers']:
            print(f"   👥 Followers: {result['followers']:,}")
            print(f"   🔄 Following: {result['following']:,}")
            print(f"   📸 Posts: {result['posts']:,}")

        if result['is_private']:
            print(f"   🔒 Private account")

        if result['is_verified']:
            print(f"   ✓ Verified")

        if result['email']:
            print(f"   📧 Email: {result['email']} ({result['email_provider']})")

        if result['phone']:
            print(f"   📱 Phone: {result['phone']}")

        if result['country']:
            print(f"   🌍 Country: {result['country']}")


def main():
    parser = argparse.ArgumentParser(description='InstaTracer - Instagram Intelligence Tool')
    parser.add_argument('-u', '--username', help='Instagram username to check')
    parser.add_argument('-f', '--file', help='File with usernames (one per line)')
    parser.add_argument('-o', '--output', help='Output file (JSON or CSV)')
    parser.add_argument('-v', '--verbose', action='store_true', help='Verbose output')

    args = parser.parse_args()

    if not args.username and not args.file:
        parser.print_help()
        return

    tracer = InstaTracer(verbose=args.verbose)

    if args.username:
        result = tracer.analyze(args.username)
        tracer.print_result(result)
        if args.output:
            with open(args.output, 'w') as f:
                json.dump(result, f, indent=2)
            print(f"\n[+] Results saved to {args.output}")

    elif args.file:
        with open(args.file, 'r') as f:
            usernames = [line.strip() for line in f if line.strip()]

        results = []
        for username in usernames:
            result = tracer.analyze(username)
            tracer.print_result(result)
            results.append(result)

        if args.output:
            with open(args.output, 'w') as f:
                json.dump(results, f, indent=2)
            print(f"\n[+] Results saved to {args.output}")


if __name__ == '__main__':
    main()

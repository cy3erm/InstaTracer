# InstaTracer 🔍

[![License: MIT](https://img.shields.io/badge/License-MIT-yellow.svg)](https://opensource.org/licenses/MIT)
[![Python 3.8+](https://img.shields.io/badge/python-3.8+-blue.svg)](https://www.python.org/downloads/)

> **⚠️ EDUCATIONAL PURPOSE ONLY**  
> This tool is for security research and educational purposes. Use only on accounts you own or have explicit permission to test.

---

## What It Does

InstaTracer reveals what Instagram's public APIs expose:

- **Account existence** - Check if a username is taken
- **Country of origin** - From phone number prefix (masked)
- **Email domain** - Gmail, Yahoo, etc. (masked email)
- **Profile data** - Followers, following, posts, bio
- **Account status** - Private/Public, Verified

---

## Features

| Feature | Description |
|---------|-------------|
| Single check | Check one Instagram username |
| Bulk check | Check multiple usernames from file |
| Country detection | Detect user country from phone prefix |
| Email provider | Detect email domain (Google, Yahoo, etc.) |
| Profile stats | Followers, following, posts count |
| Bio extraction | Extract bio and full name |
| Private detection | Detect if account is private |
| Verified badge | Detect verified accounts |
| Export | JSON and CSV export |

---

## Installation

```bash
git clone https://github.com/cyberm/InstaTracer.git
cd InstaTracer
pip install -r requirements.txt
```
---
## Usage

**Command Line**

Single username:

```bash
python instatracer.py -u username
```
**Bulk from file:**

```bash
python instatracer.py -f usernames.txt -o results.json
```
**Verbose mode:**

```bash
python instatracer.py -u username -v
```
## Python Module

```python
from instatracer import InstaTracer

tracer = InstaTracer()
result = tracer.analyze('username')

print(f"Exists: {result['exists']}")
print(f"Country: {result['country']}")
print(f"Followers: {result['followers']}")
print(f"Email: {result['email']}")
```
## Example Output
```text
✅ username: Account exists!
   👤 Name: username
   📝 Bio: bio
   👥 Followers: XXX
   🔄 Following: XXX
   📸 Posts: XX
   🔒 Private account
   📧 Email: u*******e@gmail.com (Google)
   📱 Phone: +1 *** ** ** 21
   🌍 Country: US
```
## File Format

**usernames.txt (one per line):**

```text
username
username2
username3
```
## Ethical Guidelines
**DO :**
- Test on your own Instagram accounts

- Use in authorized security assessments

- Research privacy implications

- Report vulnerabilities through official channels

**DON'T :**
- Use for harassment or stalking

- Scrape without permission

- Violate Instagram's Terms of Service

- Sell or misuse the data

## License
MIT License - See LICENSE file for details.

## Author
**CyberM**

**Made for educational purposes. Use responsibly.**

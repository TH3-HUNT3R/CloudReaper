# 💀 CloudReaper
### The Ultimate Cloudflare Bypass & Reconnaissance Tool

[![Python 3.8+](https://img.shields.io/badge/python-3.8+-blue.svg)](https://www.python.org/downloads/)
[![License: MIT](https://img.shields.io/badge/License-MIT-yellow.svg)](https://opensource.org/licenses/MIT)

**CloudReaper** is a professional-grade offensive security tool designed to expose the origin IP address behind Cloudflare protection. It combines advanced OSINT techniques with intelligent verification to bypass WAF protection.

> *"I see you."*

![CloudReaper Banner](https://img.shields.io/badge/CloudReaper-v2.0-red?style=for-the-badge)

---

## 🚀 Features

### 🧠 Multi-Source OSINT Engine
- **DNS History Lookup** - Queries ViewDNS.info for historical records
- **SSL Certificate Transparency** - Scrapes crt.sh for subdomain leaks
- **SPF Record Harvesting** - Extracts IPs from TXT/SPF records
- **Subdomain Enumeration** - Multi-threaded DNS brute-forcing

### ⚡ Intelligent Scanning
- **Smart Cloudflare Detection** - Pre-scan validation with early exit
- **Extended Port Coverage** - Scans bypass ports (80, 443, 81, 8080, 8443, 2052-2096)
- **Multi-threaded Performance** - Configurable thread count
- **Custom Wordlist Support** - Use your own subdomain lists

### ⚖️ Advanced Verification Engine
- **Multi-Factor Scoring System**:
  - HTML Title Matching (50 pts)
  - Content Length Similarity (30 pts)
  - Server Header Analysis (20 pts)
  - Favicon Hash Matching (80 pts)
  - Custom Keyword Search (100 pts)
- **Host Header Injection** - Handles virtual hosts correctly
- **Smart Protocol Detection** - HTTPS → HTTP fallback

### 🎨 Professional UI
- Beautiful Rich terminal interface
- Real-time progress tracking
- Color-coded results
- JSON export support

---

## 📦 Installation

```bash
# Clone repository
git clone https://github.com/Start-a-Town/CloudReaper.git
cd CloudReaper

# Install dependencies
pip install -r requirements.txt

# Verify installation
python cloudreaper.py --help
```

**Requirements:** Python 3.8+, pip

---

## 🖥️ Usage

### Basic Scan
```bash
python cloudreaper.py example.com
```

### Advanced Scan
```bash
python cloudreaper.py example.com --threads 50 --ports 80,443,8080,8443
```

### With Custom Wordlist
```bash
python cloudreaper.py example.com --wordlist subdomains.txt
```

### Keyword Confirmation
```bash
python cloudreaper.py example.com --keyword "Powered by WordPress"
```

### Export Results
```bash
python cloudreaper.py example.com --output results.json
```

### Full Professional Scan
```bash
python cloudreaper.py example.com \
  --threads 50 \
  --ports 80,443,81,8080,8443,8000,8880,2052,2053,2082,2083,2086,2087,2095,2096 \
  --wordlist custom_subs.txt \
  --keyword "unique-identifier" \
  --output report.json
```

---

## 🔧 Options

| Option | Description | Default |
|--------|-------------|---------|
| `target` | Target domain (required) | - |
| `--ports` | Comma-separated port list | `80,443,81,8080,8443,8000,8880` |
| `--threads` | Thread count for subdomain scanning | `20` |
| `--wordlist` | Path to custom subdomain wordlist | Built-in (45 subdomains) |
| `--output` | Save results to JSON file | None |
| `--keyword` | Body keyword for bypass confirmation | None |

---

## 🔍 How It Works

1. **Pre-Scan Detection** - Validates domain and checks if behind Cloudflare
2. **Baseline Fingerprinting** - Captures protected site signature
3. **OSINT Reconnaissance** - Parallel execution of DNS history, crt.sh, SPF, subdomain enumeration
4. **Active Scanning** - Port scanning on discovered IPs
5. **Verification** - Multi-factor similarity scoring with confidence levels

**Confidence Levels:**
- 🟢 **70%+** = Confirmed bypass
- 🟡 **40-70%** = Likely bypass
- ⚪ **<40%** = Unlikely

---

## 📤 Output

### Terminal
```
╭─────────────────────────────────────────────────────────╮
│                   Bypass Candidates                     │
├──────────────┬──────┬──────────────┬────────┬──────────┤
│ Source IP    │ Port │ Server       │ Score  │ Bypass?  │
├──────────────┼──────┼──────────────┼────────┼──────────┤
│ 203.0.113.42 │ 8080 │ nginx/1.18.0 │ 85%    │ YES!     │
│ 198.51.100.1 │ 443  │ Apache/2.4   │ 65%    │ Likely   │
╰──────────────┴──────┴──────────────┴────────┴──────────╯
```

### JSON Export
```json
[
  {
    "ip": "203.0.113.42",
    "port": 8080,
    "server": "nginx/1.18.0",
    "score": 85,
    "bypass_likely": true,
    "confirmed": true
  }
]
```

---

## 🏗️ Architecture

```
CloudReaper/
├── cloudreaper.py          # Main orchestrator
├── requirements.txt        # Dependencies
├── core/                   # Core modules
│   ├── dns_history.py      # ViewDNS scraper
│   ├── cert_search.py      # crt.sh transparency
│   ├── dns_records.py      # SPF/TXT parser
│   ├── scanner.py          # Subdomain/port scanning
│   └── verifier.py         # Verification engine
└── utils/                  # Utilities
    ├── displaying.py       # Rich UI components
    ├── ip_tools.py         # IP/DNS tools
    └── waf_detector.py     # Cloudflare detection
```

---

## 🛠️ Troubleshooting

**No candidate IPs found**
- Use custom wordlist: `--wordlist subs.txt`
- Increase threads: `--threads 50`

**Could not fetch baseline**
- Verify target is accessible
- Check internet connection

**Low match scores**
- Use `--keyword` with unique site content
- Manually verify: `curl -H "Host: example.com" http://IP`

**OSINT sources not responding**
- Wait and retry (rate limiting)
- Check services manually
- Use VPN to change IP

---

## 🤝 Contributing

Contributions welcome! Priority areas:

**High Priority:**
- Threaded port scanning
- Verbose logging mode
- Rate limiting protection
- MX record enumeration

**Medium Priority:**
- Shodan/Censys API integration
- Proxy support
- Configuration file (YAML)
- Resume capability

**How to Contribute:**
1. Fork the repository
2. Create feature branch: `git checkout -b feature/amazing-feature`
3. Commit changes: `git commit -m 'Add amazing feature'`
4. Push to branch: `git push origin feature/amazing-feature`
5. Open Pull Request

---

## 📚 Related Tools

- [CloudFail](https://github.com/m0rtem/CloudFail) - Original Cloudflare bypass tool
- [CloudFlair](https://github.com/christophetd/CloudFlair) - Censys-based finder
- [HatCloud](https://github.com/HatBashBR/HatCloud) - IP discovery tool

---

## ⚠️ Disclaimer

**FOR EDUCATIONAL AND AUTHORIZED TESTING ONLY.**

This tool is designed for:
- Security researchers with authorization
- Red teams with explicit permission
- Bug bounty hunters on in-scope targets
- System administrators auditing their infrastructure

**Unauthorized use is illegal.** The author assumes no liability for misuse. Always obtain proper authorization before testing.

By using CloudReaper, you agree to:
- Only test systems with explicit permission
- Comply with all applicable laws
- Use the tool responsibly and ethically

---

## 👨‍💻 Author

**HUNT3R**

- 📝 [Medium](https://medium.com/@imadouguahi)
- 💻 [Me](https://imadouguahi.me/)
- 💬 Telegram: @hunt3rxxxx

---

## 📄 License

MIT License - see [LICENSE](LICENSE) file for details.

---

## 🌟 Acknowledgments

- Security research community for bypass techniques
- ViewDNS.info for historical DNS data
- crt.sh for certificate transparency
- `rich` library team for the amazing UI framework

---

**⭐ Star this repository if you find CloudReaper useful!**

*Version 2.0 | Last Updated: February 2026*

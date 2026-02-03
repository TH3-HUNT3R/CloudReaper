import requests
from bs4 import BeautifulSoup
import urllib3
import hashlib

urllib3.disable_warnings(urllib3.exceptions.InsecureRequestWarning)

import mmh3
import codecs

def get_favicon_hash(url):
    """
    Fetch favicon and return its MurmurHash3.
    """
    icon_url = f"{url}/favicon.ico" if not url.endswith('/favicon.ico') else url
    headers = {
        "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/91.0.4472.124"
    }
    try:
        resp = requests.get(icon_url, headers=headers, verify=False, timeout=5)
        if resp.status_code == 200:
            favicon = codecs.encode(resp.content, "base64")
            return mmh3.hash(favicon)
    except Exception:
        pass
    return None

def get_page_signature(url, keyword=None, host_header=None):
    """Fetch page and return a signature dict (title, length, hash, etc)."""
    headers = {
        "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/91.0.4472.124"
    }
    if host_header:
        headers["Host"] = host_header

    try:
        resp = requests.get(url, headers=headers, verify=False, timeout=5, allow_redirects=True)
        soup = BeautifulSoup(resp.text, 'html.parser')
        title = soup.title.string.strip() if soup.title else "No Title"
        body = resp.text
        
        has_keyword = False
        if keyword and keyword in body:
            has_keyword = True
        
        return {
            "status": resp.status_code,
            "title": title,
            "len": len(body),
            "hash": hashlib.md5(body.encode('utf-8')).hexdigest(),
            "server": resp.headers.get("Server", "Unknown"),
            "url": resp.url,
            "has_keyword": has_keyword
        }
    except Exception:
        return None

def verify_bypass(target_url, candidate_ip, port, keyword=None):
    """
    Compare the main target (protected) with the candidate IP:Port.
    Returns a similarity score and details.
    """
    # Extract pure domain from target_url for Host header
    # e.g. https://example.com -> example.com
    target_domain = target_url.split("//")[1].split("/")[0].split(":")[0]

    # 1. Get Baseline (No special host header needed typically, verifies as usual)
    original_sig = get_page_signature(target_url)
    original_fav = get_favicon_hash(target_url)
    
    # 2. Get Candidate (Smart Protocol Detection)
    # Try HTTPS first, fallback to HTTP
    candidate_sig = None
    candidate_fav = None
    protocol = "https"
    
    try:
        # Probing HTTPS
        test_url = f"https://{candidate_ip}:{port}"
        # KEY FIX: Pass Host Header so vhosts resolve correctly!
        candidate_sig = get_page_signature(test_url, keyword=keyword, host_header=target_domain)
        # If this didn't crash but returned valid sig, stick with https
        if candidate_sig:
             candidate_fav = get_favicon_hash(test_url)
    except Exception:
        pass
        
    if not candidate_sig:
        # Fallback to HTTP
        protocol = "http"
        test_url = f"http://{candidate_ip}:{port}"
        # KEY FIX: Pass Host Header
        candidate_sig = get_page_signature(test_url, keyword=keyword, host_header=target_domain)
        if candidate_sig:
            candidate_fav = get_favicon_hash(test_url)
            
    if not original_sig or not candidate_sig:
        return 0, candidate_sig

    # 3. Compare
    score = 0
    
    # Title Match (Strong indicator)
    if original_sig['title'] == candidate_sig['title'] and original_sig['title'] != "No Title":
        score += 50
    
    # Content Length Similarity (within 10%)
    len_diff = abs(original_sig['len'] - candidate_sig['len'])
    if original_sig['len'] > 0:
        percent_diff = (len_diff / original_sig['len']) * 100
        if percent_diff < 10:
            score += 30
        elif percent_diff < 30:
            score += 10
            
    # Server Header (If not Cloudflare)
    if "cloudflare" not in candidate_sig['server'].lower():
        score += 20

    # Favicon Match (Very Strong indicator)
    if original_fav and candidate_fav and original_fav == candidate_fav:
        score += 80  # Almost certain match
    
    # Keyword Body Search (User override)
    if keyword and candidate_sig.get('has_keyword'):
        score += 100 # Confirmed
        
    return score, candidate_sig

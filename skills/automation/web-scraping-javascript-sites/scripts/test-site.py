#!/usr/bin/env python3
"""Test if a site is scrapeable with urllib or needs Playwright"""

import urllib.request
import re
import sys

def test_site(url):
    print(f"Fetching: {url}")
    req = urllib.request.Request(url, headers={
        'User-Agent': 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/537.36'
    })
    try:
        response = urllib.request.urlopen(req, timeout=10)
        html = response.read().decode('utf-8')
        print(f"SUCCESS: {len(html)} bytes received\n")
        
        # Check size
        if len(html) < 5000:
            print("⚠️  Very small HTML - likely needs JS rendering")
            return False
        
        # Strip tags and count text
        text = re.sub(r'<[^>]+>', ' ', html)
        text = re.sub(r'\s+', ' ', text).strip()
        word_count = len(text.split())
        print(f"Text content: {len(text)} chars, ~{word_count} words\n")
        
        if word_count < 50:
            print("⚠️  Very little text - likely JS-rendered SPA")
            print("→ Use Playwright for this site")
            return False
        
        # Show snippet
        print("--- First 500 chars of text ---")
        print(text[:500])
        print("---")
        
        return True
        
    except Exception as e:
        print(f"❌ ERROR: {e}")
        return None

if __name__ == "__main__":
    url = sys.argv[1] if len(sys.argv) > 1 else "https://example.com/app"
    can_scrape = test_site(url)
    
    print(f"\n{'✅ urllib works - use raw HTML fetch' if can_scrape else '❌ Use Playwright'}")

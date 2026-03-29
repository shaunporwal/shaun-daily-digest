#!/usr/bin/env python3
"""
Generate RSS feed from X feed entries with real tweet links
"""

import json
from datetime import datetime
from pathlib import Path

REPO_DIR = Path.home() / "Documents/GitHub/other/shaun-x-feed"
ENTRIES_DIR = REPO_DIR / "entries"
FEED_FILE = REPO_DIR / "feed.xml"

def generate_rss():
    """Generate RSS 2.0 feed from entries"""
    
    entries_dir = ENTRIES_DIR
    if not entries_dir.exists():
        entries_dir.mkdir(parents=True)
        return
    
    # Load all entries
    items = []
    for entry_file in sorted(entries_dir.glob("*.json"), reverse=True)[:30]:
        try:
            with open(entry_file) as f:
                data = json.load(f)
                items.append(data)
        except:
            pass
    
    # Build RSS
    rss = f"""<?xml version="1.0" encoding="UTF-8"?>
<rss version="2.0">
  <channel>
    <title>X Feed Digest - AI/Tech/Science</title>
    <link>https://github.com/shaunporwal/shaun-x-feed</link>
    <description>Real tweets curated from X about AI models, innovations, and global trends</description>
    <language>en-us</language>
    <lastBuildDate>{datetime.utcnow().strftime('%a, %d %b %Y %H:%M:%S +0000')}</lastBuildDate>
"""
    
    for item in items:
        title = item.get("title", "Daily Update")
        pub_date = item.get("date", datetime.now().isoformat())
        content = item.get("content", "")
        
        rss += f"""
    <item>
      <title>{title}</title>
      <pubDate>{pub_date}</pubDate>
      <description><![CDATA[{content}]]></description>
      <guid>{pub_date}</guid>
    </item>
"""
    
    rss += """
  </channel>
</rss>
"""
    
    with open(FEED_FILE, 'w') as f:
        f.write(rss)
    
    print(f"✅ RSS feed generated: {FEED_FILE}")

if __name__ == "__main__":
    generate_rss()

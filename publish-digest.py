#!/usr/bin/env python3
"""
Publish daily digest to GitHub Pages
Generates entries and commits to repo
"""

import json
import os
import subprocess
from datetime import datetime
from pathlib import Path

REPO_DIR = Path.home() / "Documents/GitHub/other/daily-digest"
ENTRIES_DIR = REPO_DIR / "entries"

def publish_digest(title, content):
    """Create entry and commit"""
    
    ENTRIES_DIR.mkdir(parents=True, exist_ok=True)
    
    # Create entry file
    timestamp = datetime.now().isoformat()
    filename = f"{datetime.now().strftime('%Y-%m-%d_%H-%M-%S')}.json"
    entry_file = ENTRIES_DIR / filename
    
    entry = {
        "title": title,
        "date": timestamp,
        "content": content
    }
    
    with open(entry_file, 'w') as f:
        json.dump(entry, f, indent=2)
    
    # Generate RSS feed
    subprocess.run([
        "python3",
        str(REPO_DIR / "generate-feed.py")
    ], cwd=str(REPO_DIR))
    
    # Commit and push
    os.chdir(REPO_DIR)
    subprocess.run(["git", "add", "-A"], check=True)
    subprocess.run([
        "git", "commit", 
        "-m", f"Daily digest: {title}"
    ], check=True)
    subprocess.run(["git", "push", "origin", "main"], check=True)
    
    print(f"✅ Published: {title}")
    return entry_file

if __name__ == "__main__":
    # Test
    test_content = """
    <h2>🤖 AI & Models</h2>
    <p>Latest developments in LLMs and agent frameworks</p>
    
    <h2>🧬 Science</h2>
    <p>Breakthroughs in biotech and research</p>
    
    <h2>🌍 Trends</h2>
    <p>Global technology and innovation news</p>
    """
    
    publish_digest(
        f"Daily Digest - {datetime.now().strftime('%B %d, %Y')}",
        test_content
    )

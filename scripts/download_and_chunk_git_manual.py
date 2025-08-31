import requests
from bs4 import BeautifulSoup
import os
import textwrap
import re
from urllib.parse import urlparse
import html2text

# Config
URL = "https://git-scm.com/docs/user-manual"
OUTPUT_DIR = "data/git_manual"

def format_filename_from_url(url: str) -> str:
    parsed = urlparse(url)
    filename = os.path.basename(parsed.path) or "index"
    # Chỉ giữ ký tự hợp lệ
    filename = re.sub(r'[^a-zA-Z0-9._-]', '_', filename)
    # Đặt phần mở rộng .md
    if not filename.endswith(".md"):
        filename += ".md"
    return filename

def save_markdown(html, url, output_dir):
    os.makedirs(output_dir, exist_ok=True)
    
    # Convert HTML -> Markdown
    h = html2text.HTML2Text()
    h.ignore_links = False
    h.body_width = 0
    markdown_text = h.handle(html)

    filename = format_filename_from_url(url)
    filepath = os.path.join(output_dir, filename)
    
    with open(filepath, "w", encoding="utf-8") as f:
        f.write(markdown_text)
    
    print(f"✅ Saved markdown: {filepath}")
    return filepath

def main():
    print("📥 Downloading Git User Manual...")
    response = requests.get(URL)
    if response.status_code != 200:
        raise Exception(f"Failed to fetch page: {response.status_code}")

    print("📝 Converting HTML -> Markdown...")
    save_markdown(response.text, URL, OUTPUT_DIR)

    print("🎉 Done.")

if __name__ == "__main__":
    main()
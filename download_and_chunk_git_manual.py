import requests
from bs4 import BeautifulSoup
import os
import textwrap

# Config
URL = "https://git-scm.com/docs/user-manual"
OUTPUT_DIR = "data/git_manual_chunks"
CHUNK_SIZE = 800  # words per chunk

def clean_text(html):
    soup = BeautifulSoup(html, "html.parser")
    content_div = soup.find("div", {"id": "content"})
    if not content_div:
        raise Exception("Không tìm thấy nội dung chính.")
    return content_div.get_text(separator="\n")

def chunk_text(text, chunk_size):
    words = text.split()
    chunks = [words[i:i+chunk_size] for i in range(0, len(words), chunk_size)]
    return [" ".join(chunk) for chunk in chunks]

def save_chunks(chunks, output_dir):
    os.makedirs(output_dir, exist_ok=True)
    for i, chunk in enumerate(chunks):
        file_path = os.path.join(output_dir, f"chunk_{i+1:03}.txt")
        with open(file_path, "w", encoding="utf-8") as f:
            f.write(chunk)
        print(f"✅ Saved: {file_path}")

def main():
    print("📥 Downloading Git User Manual...")
    response = requests.get(URL)
    if response.status_code != 200:
        raise Exception(f"Failed to fetch page: {response.status_code}")

    print("🔍 Parsing and extracting content...")
    full_text = clean_text(response.text)

    print("✂️ Chunking content...")
    chunks = chunk_text(full_text, CHUNK_SIZE)

    print(f"💾 Saving {len(chunks)} chunks to '{OUTPUT_DIR}'...")
    save_chunks(chunks, OUTPUT_DIR)

    print("🎉 Done.")

if __name__ == "__main__":
    main()

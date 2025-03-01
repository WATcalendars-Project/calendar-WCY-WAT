import os
import requests

BASE_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))  
DATA_DIR = os.path.join(BASE_DIR, "data/html")
os.makedirs(DATA_DIR, exist_ok=True)

def fetch_html(url, filename=None, save=True):

    headers = {"User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/119.0.0.0 Safari/537.36"}

    response = requests.get(url, headers=headers)
    if response.status_code != 200:
        raise Exception(f"Error downloading html: {response.status_code}")

    html_content = response.text

    if save and filename:
        filepath = os.path.join(DATA_DIR, filename)
        with open(filepath, "w", encoding="utf-8") as f:
            f.write(html_content)
        print(f"'{filename}' saved in {filepath}")

    return html_content
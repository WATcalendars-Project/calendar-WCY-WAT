import os
from bs4 import BeautifulSoup
from download_html import fetch_html 

GROUPS_URL = "https://planzajec.wcy.wat.edu.pl/pl/rozklad"
DATA_DIR = os.path.join(os.path.dirname(os.path.dirname(os.path.abspath(__file__))), "data")
OUTPUT_FILE = os.path.join(DATA_DIR, "groups.txt")

def parse_groups(html_content):
    soup = BeautifulSoup(html_content, "html.parser")

    groups = [option.text.strip() for option in soup.find_all("option") if option.text.strip()]
    
    groups = [group for group in groups if "- Wybierz grupę -" not in group]
    groups = [group.rstrip(".") for group in groups]

    return groups

if __name__ == "__main__":
    html_content = fetch_html(GROUPS_URL) 
    groups = parse_groups(html_content)

    os.makedirs(DATA_DIR, exist_ok=True)
    with open(OUTPUT_FILE, "w", encoding="utf-8") as f:
        f.write("\n".join(groups))

    print(f"Groups saved in: {OUTPUT_FILE}")

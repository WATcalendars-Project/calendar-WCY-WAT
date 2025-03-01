import os
from bs4 import BeautifulSoup
from download_html import fetch_html

GROUPS_URL = "https://planzajec.wcy.wat.edu.pl/pl/rozklad"

DATA_DIR = os.path.join(os.path.dirname(os.path.dirname(os.path.abspath(__file__))), "data")
HTML_DIR = os.path.join(DATA_DIR, "html")
FILENAME = os.path.join(HTML_DIR, "groups.html")
OUTPUT_FILE = os.path.join(DATA_DIR, "groups.txt")

def parse_groups(html_file, output_file):

    with open(html_file, "r", encoding="utf-8") as f:
        soup = BeautifulSoup(f, "html.parser")

    groups = [option.text.strip() for option in soup.find_all("option") if option.text.strip()]

    if groups and "- Wybierz grupę -" in groups[0]:
        groups.pop(0)

    groups = [group.rstrip(".") for group in groups]

    with open(output_file, "w", encoding="utf-8") as f:
        f.write("\n".join(groups))

    print(f"Groups saved in: '{output_file}")

if __name__ == "__main__":
    fetch_html(GROUPS_URL, FILENAME)
    parse_groups(FILENAME, OUTPUT_FILE)
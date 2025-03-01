import os
from download_html import fetch_html

GROUPS_URL = "https://planzajec.wcy.wat.edu.pl/pl/rozklad"

DATA_DIR = os.path.join(os.path.dirname(os.path.dirname(os.path.abspath(__file__))), "data", "html")
FILENAME = "groups.html"

if __name__ == "__main__":
    fetch_html(GROUPS_URL, FILENAME)
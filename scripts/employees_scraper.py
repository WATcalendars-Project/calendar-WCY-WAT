import requests
from bs4 import BeautifulSoup

BASE_URL = "https://usos.wat.edu.pl/kontroler.php?_action=katalog2/osoby/pracownicyJednostki&jed_org_kod=A000000&page="
OUTPUT_FILE = "data/employees.txt"

html_content = ""

for page in range(1, 54):
    url = BASE_URL + str(page)
    response = requests.get(url)
    
    if response.status_code == 200:
        html_content += response.text + f"\n\n<!-- Strona {page} -->\n\n"
    else:
        print(f"Error downloading page: {page}: {response.status_code}")

soup = BeautifulSoup(html_content, "html.parser")

employees = []

for entry in soup.find_all("td", class_="uwb-staffuser-panel"):
    name_tag = entry.find("b")  
    degree = entry.find("a", class_="no-badge uwb-photo-panel-title")  

    if name_tag and degree:
        full_name = name_tag.text.strip()
        degree_text = degree.text.replace(full_name, "").strip()
        employees.append(f"{degree_text} {full_name}")

with open(OUTPUT_FILE, "w", encoding="utf-8") as output_file:
    for employee in employees:
        output_file.write(employee + "\n")

print(f"Employees saved in: {OUTPUT_FILE}")

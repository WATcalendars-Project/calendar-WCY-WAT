import os
import re
import requests
from bs4 import BeautifulSoup
from datetime import datetime

# Definicje katalogów i plików
DATA_DIR = "data"
WEB_STATIC_DATA_DIR = "web/static/data"
GROUPS_FILE = os.path.join(DATA_DIR, "groups.txt")
SCHEDULES_DIR = os.path.join(WEB_STATIC_DATA_DIR, "schedules")
EMPLOYEES_FILE = os.path.join(DATA_DIR, "employees.txt")

BLOCK_TIMES = {
    "block1": ("08:00", "09:35"),
    "block2": ("09:50", "11:25"),
    "block3": ("11:40", "13:15"),
    "block4": ("13:30", "15:05"),
    "block5": ("16:00", "17:35"),
    "block6": ("17:50", "19:25"),
    "block7": ("19:40", "21:15"),
}

# Tworzenie katalogu jeśli nie istnieje
os.makedirs(SCHEDULES_DIR, exist_ok=True)

def load_groups():
    """Wczytuje listę grup z pliku `groups.txt`."""
    with open(GROUPS_FILE, "r", encoding="utf-8") as f:
        return [line.strip() for line in f.readlines()]

def load_lecturer_titles():
    """Wczytuje stopnie naukowe wykładowców z pliku `employees.txt`."""
    lecturer_dict = {}
    if not os.path.exists(EMPLOYEES_FILE):
        print(f"⚠️ Plik {EMPLOYEES_FILE} nie istnieje! Stopnie naukowe nie zostaną dodane.")
        return lecturer_dict

    with open(EMPLOYEES_FILE, "r", encoding="utf-8") as file:
        for line in file:
            match = re.match(r"(.+?)\s+([A-ZĄĆĘŁŃÓŚŹŻ][a-ząćęłńóśźż]+)\s+([A-ZĄĆĘŁŃÓŚŹŻ][a-ząćęłńóśźż]+)", line.strip())
            if match:
                title, name, surname = match.groups()
                lecturer_dict[f"{name} {surname}"] = title.strip()
    return lecturer_dict

def fetch_schedule(group_id):
    """Pobiera plan zajęć dla danej grupy."""
    url = f"https://planzajec.wcy.wat.edu.pl/pl/rozklad?grupa_id={group_id}"
    headers = {"User-Agent": "Mozilla/5.0"}
    response = requests.get(url, headers=headers)
    
    if response.status_code != 200:
        print(f"❌ Błąd pobierania planu dla {group_id}! Kod: {response.status_code}")
        return None
    
    return response.text

def parse_schedule(html, academic_titles):
    """Parsuje HTML z planem zajęć."""
    if not html:
        return []
    
    soup = BeautifulSoup(html, "html.parser")
    lessons = []

    for lesson in soup.find_all("div", class_="lesson"):
        try:
            date_str = lesson.find("span", class_="date").text.strip()
            block_id = lesson.find("span", class_="block_id").text.strip()
            subject_element = lesson.find("span", class_="name")
            subject_lines = [line.strip() for line in subject_element.stripped_strings]

            if len(subject_lines) < 4:
                continue

            subject_short = subject_lines[0]
            lesson_type = subject_lines[1]
            room = subject_lines[2].replace(",", "").strip()
            lesson_number_match = re.search(r"\[(\d+)\]", subject_lines[3])
            lesson_number = lesson_number_match.group(1) if lesson_number_match else "Brak"

            info_element = lesson.find("span", class_="info")
            full_subject_info = info_element.text.strip() if info_element else "Nieznana nazwa"
            full_subject_cleaned = re.sub(r" - \(.+\) - .*", "", full_subject_info).strip()

            lecturer_match = re.search(r"- \(.+\) - ((?:dr |prof\. |inż\. )?[A-ZĄĆĘŁŃÓŚŹŻ][a-ząćęłńóśźż]+) ([A-ZĄĆĘŁŃÓŚŹŻ][a-ząćęłńóśźż]+)", full_subject_info)
            lecturer_with_title = "-"
            if lecturer_match:
                lecturer_name = f"{lecturer_match.group(2)} {lecturer_match.group(1)}"
                lecturer_with_title = academic_titles.get(lecturer_name, "") + " " + lecturer_name

            lesson_type_full = {
                "(w)": "Wykład",
                "(L)": "Laboratorium",
                "(ć)": "Ćwiczenia",
                "(P)": "Projekt",
                "(inne)": "inne",
            }.get(lesson_type, "Nieznany")

            date_obj = datetime.strptime(date_str, "%Y_%m_%d")
            start_time, end_time = BLOCK_TIMES.get(block_id, ("00:00", "00:00"))
            start_datetime = datetime.strptime(start_time, "%H:%M").replace(year=date_obj.year, month=date_obj.month, day=date_obj.day)
            end_datetime = datetime.strptime(end_time, "%H:%M").replace(year=date_obj.year, month=date_obj.month, day=date_obj.day)

            lessons.append({
                "date": date_str,
                "start": start_datetime,
                "end": end_datetime,
                "subject": subject_short,
                "type": lesson_type,
                "type_full": lesson_type_full,
                "room": room,
                "lesson_number": lesson_number,
                "full_subject": full_subject_cleaned,
                "lecturer": lecturer_with_title,
            })
        except Exception as e:
            print(f"⚠️ Błąd parsowania zajęć: {e}")
    
    return lessons

def sanitize_filename(filename):
    """Usuwa niedozwolone znaki w NAZWIE PLIKU, ale nie w ścieżce."""
    return re.sub(r'[<>:"\\|?*]', "_", filename)  # Usuwa TYLKO niedozwolone znaki w nazwie pliku

def generate_ics(lessons, filename, group_id):
    """Tworzy plik ICS z planem zajęć."""
    if not lessons:
        print(f"⚠️ Brak danych do zapisania dla {group_id}")
        return

    ics_content = f"BEGIN:VCALENDAR\nVERSION:2.0\nPRODID:-//scheduleWCY//EN\nCALSCALE:GREGORIAN\nX-WR-CALNAME:{group_id}\n"
    
    for lesson in lessons:
        start = lesson['start'].strftime("%Y%m%dT%H%M%S")
        end = lesson['end'].strftime("%Y%m%dT%H%M%S")
        
        summary = f"{lesson['subject']} {lesson['type']}"
        location = lesson['room']
        description = f"{lesson['full_subject']}\\nRodzaj zajęć: {lesson['type_full']}\\nNr zajęć: {lesson['lesson_number']}\\nProwadzący: {lesson['lecturer']}"
        
        ics_content += f"""BEGIN:VEVENT\nDTSTART:{start}\nDTEND:{end}\nSUMMARY:{summary}\nLOCATION:{location}\nDESCRIPTION:{description}\nEND:VEVENT\n"""
    
    ics_content += "END:VCALENDAR\n"

    # **Poprawka**: TYLKO nazwa pliku jest sanitizowana, nie cała ścieżka!
    sanitized_filename = sanitize_filename(f"{group_id}.ics")
    full_path = os.path.join(SCHEDULES_DIR, sanitized_filename)

    with open(full_path, "w", encoding="utf-8") as f:
        f.write(ics_content)
    
    print(f"✅ Plik kalendarza zapisany: {full_path}")

def generate_all_schedules():
    """Generuje pliki ICS dla wszystkich grup."""
    groups = load_groups()
    academic_titles = load_lecturer_titles()

    for group in groups:
        print(f"📥 Pobieranie planu dla {group}...")
        html = fetch_schedule(group)
        lessons = parse_schedule(html, academic_titles)

        generate_ics(lessons, filename=f"{group}.ics", group_id=group)

if __name__ == "__main__":
    generate_all_schedules()

from flask import Flask, render_template
import os

app = Flask(__name__)

# Ścieżki do plików
DATA_DIR = os.path.join(os.path.dirname(__file__), "..", "data")
GROUPS_FILE = os.path.join(DATA_DIR, "groups.txt")
YEARS_FILE = os.path.join(DATA_DIR, "year.txt")

def load_file(file_path):
    """Wczytuje plik i zwraca listę linii, pomijając puste wiersze."""
    with open(file_path, "r", encoding="utf-8") as f:
        return [line.strip() for line in f.readlines() if line.strip()]

@app.route("/")
def index():
    groups = load_file(GROUPS_FILE)
    years = load_file(YEARS_FILE)
    return render_template("index.html", groups=groups, years=years)

if __name__ == "__main__":
    app.run(debug=True)

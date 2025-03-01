# WCY Schedule Calendar
A simple tool to fetch and generate ICS calendar files for students at the Faculty of Cybernetics, Military University of Technology (WCY WAT). This project scrapes the official schedule, processes the data, and provides downloadable calendar files for different student groups.


## Website:
https://dominikx2002.github.io/calendar-WCY-WAT/


### How it works:
1. Scraping Data: Python scripts collect information from:
    - WCY WAT Schedule (https://planzajec.wcy.wat.edu.pl/rozklad)
    - USOS WAT Employees (https://usos.wat.edu.pl/kontroler.php?_action=katalog2/osoby/index)
2. Generating Calendar Files: The schedule_scraper.py script converts schedule data into .ics files.
3. Hosting the Frontend: GitHub Pages provides an interactive UI for selecting and downloading calendar files.
4. Automatic Updates: GitHub Actions runs daily to keep schedules up-to-date.


## Setup & Usage:
1. Local Setup
    Clone the repository
        git clone https://github.com/dominikx2002/calendar-WCY-WAT.git
        cd calendar-WCY-WAT
    Install dependencies
        pip install -r requirements.txt
    Run scraping scripts
        python scripts/groups_scraper.py
        python scripts/employees_scraper.py
        python scripts/schedule_scraper.py
2. Run the Website (GitHub Pages)
    This project is hosted via GitHub Pages. Visit:
        https://dominikx2002.github.io/calendar-WCY-WAT/

      ![obraz](https://github.com/user-attachments/assets/bee25f89-dbff-4b74-9421-adfe8900c08d)

    Download the .ics file
    Import it into your favourite calendar app (Google Calendar, Outlook, etc.)


### GitHub Actions
This project uses GitHub Actions to update schedules daily. 
The workflow:
- Runs every day at midnight (cron: "0 0 * * *")
- Fetches the latest schedule
- Generates .ics files
- Commits and pushes the updates
- Workflow file: .github/workflows/update-data.yml 

### Contributing
Want to improve the project? Feel free to:
- Open an Issue
- Create a Pull Request
- Suggest improvments

### Contact:
For any questions, feel free to open an issue or reach out via GitHub!

## License
This project is licensed under [BSD-2-Clause License](LICENSE). See [LICENSE](LICENSE) for details.

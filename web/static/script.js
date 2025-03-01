document.addEventListener("DOMContentLoaded", function() {
    loadGroups();
    loadYears();
});

async function loadGroups() {
    const groupSelect = document.getElementById("group");
    try {
        const response = await fetch("data/groups.txt");
        const text = await response.text();
        const groups = text.split("\n").map(g => g.trim()).filter(g => g);

        groups.forEach(group => {
            const option = document.createElement("option");
            option.value = group;
            option.textContent = group;
            groupSelect.appendChild(option);
        });
    } catch (error) {
        console.error("Błąd ładowania grup:", error);
    }
}

async function loadYears() {
    const yearSelect = document.getElementById("year");
    try {
        const response = await fetch("data/year.txt");
        const text = await response.text();
        const years = text.split("\n").map(y => y.trim()).filter(y => y);

        years.forEach(year => {
            const option = document.createElement("option");
            option.value = year;
            option.textContent = `${year} Rok`;
            yearSelect.appendChild(option);
        });
    } catch (error) {
        console.error("Błąd ładowania lat:", error);
    }
}

function generateLink() {
    const group = document.getElementById("group").value;
    const year = document.getElementById("year").value;
    const link = `https://twoja-strona.pl/kalendarz/${year}/${group}.ics`;

    document.getElementById("generated-link").innerHTML = 
        `<a href="${link}" target="_blank">📅 Pobierz kalendarz</a>`;
}

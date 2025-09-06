const table = document.getElementById("trainingTable");
const selection = document.getElementById("trainingPlanSelection");
const trainingPlans = trainingPlansData; 
const daysOfWeek = ["monday", "tuesday", "wednesday", "thursday", "friday", "saturday", "sunday"];

function renderTable() {
    const currentSelection = selection.value;
    table.innerHTML = "";

    const filteredPlans = trainingPlans.filter(plan => {
        if (currentSelection === "All") return true;

        const [week, year] = plan.week.split("-").map(Number);
        const [currentWeek, currentYear] = currentWeekYear.split("-").map(Number);
        const yearDiff = year - currentYear;
        const weekDiff = week - currentWeek;
        const current = (yearDiff > 0 || (yearDiff === 0 && weekDiff >= 0));

        if (currentSelection === "Current" && current) return true;
        if (currentSelection === "Previous" && !current) return true;
        return false;
    });

    filteredPlans.forEach(plan => {
        const week = plan.week;
        let orderedPlan = {};
        for (const key of daysOfWeek) {
            orderedPlan[key] = plan[key];
        }

        let row = "<tr><th>" + week + "</th>";

        for (const [key, value] of Object.entries(orderedPlan)) {
            const day = key.charAt(0).toUpperCase() + key.slice(1);
            row += "<td>";
            row += "<div class='center-text'>" + day + "</div>";
            row += "Easy distance: " + value["easy_distance"] + "<br>";
            row += "Hard distance: " + value["hard_distance"] + "<br>";
            row += "Total distance: " + (parseFloat(value["hard_distance"]) + parseFloat(value["easy_distance"])) + "<br>";
            row += "</td>";
        }

        row += "</tr>";
        table.innerHTML += row;
    });
}

renderTable();
selection.addEventListener("change", renderTable);

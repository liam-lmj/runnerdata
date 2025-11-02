const daysOfWeek = ["Monday", "Tuesday", "Wednesday", "Thursday", "Friday", "Saturday", "Sunday"];

function updateCharts(barData, pieData) {
    Plotly.react('bar', barData.data, barData.layout || {});
    Plotly.react('pie', pieData.data, pieData.layout || {});
}

function renderTable(week, mileageData) {
    const table = document.getElementById("mileageTable");
    table.innerHTML = "";
    for (let weekly_mileage of mileageData) {
        if (weekly_mileage.week !== week) continue;
        let row = "<tr>";

        let orderedMileage = {};
        for (const key of daysOfWeek) {
            orderedMileage[key] = weekly_mileage[key];
        }
        console.log(orderedMileage);
        for (const [key, value] of Object.entries(orderedMileage)) {
            if (key === "week" || key === "Total" || value === undefined) continue;
            row += "<td>";
            row += "<div class='center-text'>" + key + "</div>";
            row += "Easy distance: " + Math.round(100 * (value["easy_distance"])) / 100 + "<br>";
            row += "Hard distance: " + Math.round(100 * (value["hard_distance"])) / 100 + "<br>";
            row += "Total distance: " + Math.round(100 * (value["total_distance"])) / 100 + "<br>";
            row += "</td>";
        }
        row += "</tr>";
        table.innerHTML += row;
    }
}

function initializeCharts(barData, pieData, week, mileageData) {
    updateCharts(barData, pieData);
    renderTable(week, mileageData);
    const weekSelector = document.getElementById("week");
    weekSelector.value = week;
    weekSelector.addEventListener('change', function() {
        const selectedWeek = this.value;
        fetch('/mileagechart', {
            method: 'POST',
            headers: { 'Content-Type': 'application/json' },
            body: JSON.stringify({ selectedWeek, 'type': 'charts' })
        })
        .then(response => response.json())
        .then(data => {
            const bar = JSON.parse(data.bar_json);
            const pie = JSON.parse(data.pie_json);
            updateCharts(bar, pie);
            renderTable(selectedWeek, mileageData);
        });
    });
}

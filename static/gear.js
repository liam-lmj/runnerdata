const table = document.getElementById("gearTable");
const selection = document.getElementById("gearSelection");
const gear = runningGearData;

function renderTable() {
    const currentSelection = selection.value;

    table.innerHTML = "";

    const filteredGear = gear.filter(key => {
        if (currentSelection === "All") return true; 

        if (currentSelection === "Active" && key.active === "Active"){
            return true
        } 
        if (currentSelection === "Retired" && key.active === "Retired"){
            return true
        } 
            return false;    
        });
 
        for (const key of filteredGear){
            const row = document.createElement("tr");
            const cell = document.createElement("td");

            cell.innerHTML = `
                                Trainer: ${key.name}<br>
                                Distance: ${key.distance}<br>
                                Active: ${key.active}<br>
                                Default Run Type: ${key.default_type}<br>
                            `;
            row.appendChild(cell);
            table.appendChild(row);
        }
}

renderTable();
selection.addEventListener("change", renderTable);
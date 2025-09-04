const table = document.getElementById("gearTable");
const selection = document.getElementById("gearSelection");
const popup = document.getElementById("popup");
const gear = runningGearData;

function openForm(gear_id) {
  popup.style.display = "block";
  popup.dataset.gear_id = gear_id
}

function closeForm() {
  popup.style.display = "none";
}

function updateAndClose(add, remove, gear_id) {
    const totalNewMiles = add - remove;
    fetch('/gear', {
        method: 'POST',
        headers: { 'Content-Type': 'application/json' },
        body: JSON.stringify({ totalNewMiles, gear_id })
    })
    .then(response => response.json())
    .then(data => {
        const index = runningGearData.findIndex(g => g.gear_id == gear_id);
        if (index !== -1) {
            runningGearData[index].distance += totalNewMiles;
        }
        renderTable();  
        closeForm();    
    })
}

function retiredAndClose() {
    closeForm();
}

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
            const button = document.createElement("button");
            cell.innerHTML = `
                                Trainer: ${key.name}<br>
                                Distance: ${key.distance}<br>
                                Active: ${key.active}<br>
                                Default Run Type: ${key.default_type}<br>
                            `;
            button.innerHTML = 'Update Trainer';

            button.addEventListener("click", function() {openForm(key.gear_id);});

            row.appendChild(cell);
            table.appendChild(row);
            table.appendChild(button)
        }
}

renderTable();
selection.addEventListener("change", renderTable);
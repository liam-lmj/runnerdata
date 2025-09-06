const table = document.getElementById("gearTable");
const selection = document.getElementById("gearSelection");
const activeSelection = document.getElementById("activeSelection");
const defaultTypeSelection = document.getElementById("default_type");
const popup = document.getElementById("popup");
const popupAdd = document.getElementById("popup_add");
const popupAddForm = document.getElementById("popup_add_form");
const gear = runningGearData;

function openAddForm() {
  popupAdd.style.display = "block";
}

function closeAddForm() {
  popupAdd.style.display = "none";
}

function validateAdd() {
  if (popupAddForm.checkValidity()) {
    addAndClose(
      document.getElementById("existingMiles").value,
      document.getElementById("default_type_add").value,
      document.getElementById("trainer").value
    );
    popupAddForm.reset();

  } else {
    popupAddForm.reportValidity(); 
  }
}

function addAndClose(miles, default_type, trainer, type = "Add") {
    fetch('/gear', {
        method: 'POST',
        headers: { 'Content-Type': 'application/json' },
        body: JSON.stringify({ miles, default_type, trainer, type })
    })
    .then(response => response.json())
    .then(data => {
        //const index = runningGearData.findIndex(g => g.gear_id == gear_id);
        //if (index !== -1) {
        //    runningGearData[index].distance += totalNewMiles;
        //    runningGearData[index].active = active;
        //    runningGearData[index].default_type = default_type;
        //}
        renderTable();  
        closeAddForm();    
    })
}

function openForm(gear_id, active, runType) {
  popup.style.display = "block";
  popup.dataset.gear_id = gear_id;
  activeSelection.value = active;
  defaultTypeSelection.value = runType;
}

function closeForm() {
  popup.style.display = "none";
}

function updateAndClose(add, remove, active, default_type, gear_id, type = "Update") {
    const totalNewMiles = Number(add) - Number(remove);
    fetch('/gear', {
        method: 'POST',
        headers: { 'Content-Type': 'application/json' },
        body: JSON.stringify({ totalNewMiles, gear_id, active, default_type, type })
    })
    .then(response => response.json())
    .then(data => {
        const index = runningGearData.findIndex(g => g.gear_id == gear_id);
        console.log(runningGearData)
        console.log(runningGearData[index])
        if (index !== -1) {
            runningGearData[index].distance += totalNewMiles;
            runningGearData[index].active = active;
            runningGearData[index].default_type = default_type;
        }
        renderTable();  
        closeForm();    
    })
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
            const runType = key.default_type === null ? "None" : key.default_type
             
            cell.innerHTML = `
                                Trainer: ${key.name}<br>
                                Distance: ${key.distance}<br>
                                Active: ${key.active}<br>
                                Default Run Type: ${runType}<br>
                            `;
            button.innerHTML = 'Update Trainer';

            button.addEventListener("click", function() {openForm(key.gear_id, key.active, runType);});

            cell.appendChild(button);
            row.appendChild(cell);
            table.appendChild(row);
        }
}

renderTable();
selection.addEventListener("change", renderTable);
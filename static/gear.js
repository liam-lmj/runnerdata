const table = document.getElementById("gearTable");
const selection = document.getElementById("gearSelection");
const activeSelection = document.getElementById("activeSelection");
const defaultTypeSelection = document.getElementById("default_type");
const popup = document.getElementById("popup");
const popupForm = document.getElementById("popup_form");
const popupAdd = document.getElementById("popup_add");
const popupAddForm = document.getElementById("popup_add_form");
const runTypes = ["Easy", "Hard"]

function openAddForm() {
  popupAdd.style.display = "block";
  popup.style.display = "none";
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
        new_trainer = {
            name: trainer,
            distance: miles,
            active: "Active",
            default_type: default_type,
            gear_id: data.gear_id
        }
        if (runTypes.includes(default_type)){
          var counter, item;
          for (counter in runningGearData) {
            item = runningGearData[counter];
            if (item.default_type === default_type) item.default_type = 'None'
          }
        }
        runningGearData.push(new_trainer)

        renderTable();  
        closeAddForm();    
    })
}

function openForm(gear_id, active, runType) {
  popup.style.display = "block";
  popupAdd.style.display = "none";
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
        const distance = Number(runningGearData[index].distance) + totalNewMiles;
        if (index !== -1) {
            runningGearData[index].distance = distance;
            runningGearData[index].active = active;
            runningGearData[index].default_type = default_type;
        }

        if (runTypes.includes(default_type)){
          var counter, item;
          for (counter in runningGearData) {
            item = runningGearData[counter];
            if (item.default_type === default_type && counter != index) item.default_type = 'None'
          }
        }

        renderTable();  
        closeForm();    
    })
}

function renderTable() {
    const currentSelection = selection.value;

    table.innerHTML = "";

    const filteredGear = runningGearData.filter(key => {
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
            const runType = key.default_type === null ? "None" : key.default_type;
            const roundedDistance = Math.round(key.distance);
            cell.innerHTML = `
                                Trainer: ${key.name}<br>
                                Distance: ${roundedDistance}<br> 
                                Active: ${key.active}<br>
                                Default Run Type: ${runType}<br>
                            `;

            cell.addEventListener("click", function() {openForm(key.gear_id, key.active, runType);});

            row.appendChild(cell);
            table.appendChild(row);
        }
}

renderTable();
selection.addEventListener("change", renderTable);
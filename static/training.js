const table = document.getElementById("trainingTable");
const selection = document.getElementById("trainingPlanSelection");
const trainingPlans = trainingPlansData; 
const nextWeeks = nextFiveWeeks;
const daysOfWeek = ["monday", "tuesday", "wednesday", "thursday", "friday", "saturday", "sunday"];
const popupAdd = document.getElementById("popup_add_plan");


const initalHtml = `<form class="training-form-container"id="popup_add_plan_form">
                        <h1 class="form-header">Add Plan</h1>

                        <div class="form-row" id="firstDay">
                            <label for="Monday"><b>Monday</b></label>
                            <input type="number" placeholder="input miles" id="monday_miles" name="monday_miles" required>
                        </div>

                        <div class="form-row">
                            <label for="Tuesday"><b>Tuesday</b></label>
                            <input type="number" placeholder="input miles" id="tuesday_miles" name="tuesday_miles" required>
                        </div>

                        <div class="form-row">
                            <label for="Wednesday"><b>Wednesday</b></label>
                            <input type="number" placeholder="input miles" id="wednesday_miles" name="wednesday_miles" required>
                        </div>

                        <div class="form-row">
                            <label for="Thursday"><b>Thursday</b></label>
                            <input type="number" placeholder="input miles" id="thursday_miles" name="thursday_miles" required>
                        </div>

                        <div class="form-row">
                            <label for="Friday"><b>Friday</b></label>
                            <input type="number" placeholder="input miles" id="friday_miles" name="friday_miles" required>
                        </div>

                        <div class="form-row">
                            <label for="Saturday"><b>Saturday</b></label>
                            <input type="number" placeholder="input miles" id="saturday_miles" name="saturday_miles" required>
                        </div>

                        <div class="form-row">
                            <label for="Sunday"><b>Sunday</b></label>
                            <input type="number" placeholder="input miles" id="sunday_miles" name="sunday_miles" required>
                        </div>

                        <div class="form-row">
                            <label for="Session"><b>Session</b></label>
                            <select id="sessionType" name="sessionType">
                                    <option value="None">None</option>
                                    <option value="Threshold">Threshold</option>
                                    <option value="AM Threshold">AM Threshold</option>  
                                    <option value="Hard Reps">Hard Reps</option>
                                    <option value="Race">Race</option>
                            </select>
                            <input type="text" placeholder="description" id="sessionDescription" name="sessionDescription" required>
                        </div>

                        <div class="form-row" id="sessionsContainer"></div>

                        <div class="button-group" id="buttons">
                            <button type="button" onclick="addAndClose()">Add</button>
                            <button type="reset" onclick="closeAddForm()">Cancel</button>
                        </div>
                    </form>`

function formatWeekDropdown() {
  const container = document.getElementById('popup_add_plan_form');
  const firstDay = document.getElementById('firstDay');

  let dropdownDiv = document.createElement('div');
  let dropdown = document.createElement('select');
  dropdownDiv.className = "form-row";
  dropdown.className = "drop-down-alt";
  dropdown.id = "week";

  let row =  "";

  dropdownDiv.appendChild(dropdown);
  for (let i = 0; i < nextFiveWeeks.length; i++) {
    row += `<option value="${nextFiveWeeks[i]}">${nextFiveWeeks[i]}</option>`;
  }
  dropdown.innerHTML = row;
  container.insertBefore(dropdownDiv, firstDay);
}

function addSessionRow(type, desc) {
  const container = document.getElementById('popup_add_plan_form');
  const buttons = document.getElementById('buttons');
  const html = `
    <div class="form-row" id="sessionRow${counter}">
      <label for="sessionType${counter}"><b>Session</b></label>
      <select id="sessionType${counter}" name="sessionType${counter}">
        <option value="None" ${type === 'None' ? 'selected' : ''}>None</option>
        <option value="Threshold" ${type === 'Threshold' ? 'selected' : ''}>Threshold</option>
        <option value="AM Threshold" ${type === 'AM Threshold' ? 'selected' : ''}>AM Threshold</option>
        <option value="Hard Reps" ${type === 'Hard Reps' ? 'selected' : ''}>Hard Reps</option>
        <option value="Race" ${type === 'Race' ? 'selected' : ''}>Race</option>
      </select>
      <input type="text" placeholder="description" id="sessionDescription${counter}" name="sessionDescription${counter}" value="${desc}">
    </div>
  `;
  let session = document.createElement('div');
  session.innerHTML = html;
  container.insertBefore(session, buttons);
  counter++;
}

function handleSessionInput() {
  let sessionTypeValue = document.getElementById('sessionType').value;
  let sessionDescValue = document.getElementById('sessionDescription').value;

  if (sessionDescValue.trim() !== '' && sessionTypeValue !== 'none' && sessionTypeValue !== '') {
    addSessionRow(sessionTypeValue, sessionDescValue);
    document.getElementById('sessionDescription').value = '';
    document.getElementById('sessionType').value = 'none';
  }
}

function openNewPlan() {
  popupAdd.style.display = "block";
  popupAdd.innerHTML = initalHtml;
  counter = 1;
  formatWeekDropdown()
  document.getElementById('sessionType').addEventListener('change', handleSessionInput);
  document.getElementById('sessionDescription').addEventListener('change', handleSessionInput);
}
 
function closeAddForm() {
  popupAdd.style.display = "none";
  popupAdd.innerHTML = initalHtml;
}

function addAndClose() {
  const week = document.getElementById("week").value;
  const monday = document.getElementById("monday_miles").value;
  const tuesday = document.getElementById("tuesday_miles").value;
  const wednesday = document.getElementById("wednesday_miles").value;
  const thursday = document.getElementById("thursday_miles").value;
  const friday = document.getElementById("friday_miles").value;
  const saturday = document.getElementById("saturday_miles").value;
  const sunday = document.getElementById("sunday_miles").value;
  const total = Number(monday) + Number(tuesday) + Number(wednesday) + 
                Number(thursday) + Number(friday) + Number(saturday) + Number(sunday);
  let sessions = [];

  for (let i = 1; i < counter; i++) {
    const sessionDescId = `sessionDescription${i}`;
    const sessionTypeId = `sessionType${i}`;
    const sessionDesc = document.getElementById(sessionDescId).value;
    const sessionType = document.getElementById(sessionTypeId).value;
    const sessionDict = {
                          "sessionDesc": sessionDesc,
                          "sessionType": sessionType
                        }
    sessions.push(sessionDict);
  }

  fetch('/training', {
      method: 'POST',
      headers: { 'Content-Type': 'application/json' },
      body: JSON.stringify({ week, monday, tuesday, wednesday, thursday, 
                             friday, saturday, sunday, total, sessions,
                             runner: "34892346", current: "true", achieved: "pending" })
  })

  popupAdd.style.display = "none";
  popupAdd.innerHTML = initalHtml;
}

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

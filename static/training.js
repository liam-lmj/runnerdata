const table = document.getElementById("trainingTable");
const selection = document.getElementById("trainingPlanSelection");
const trainingPlans = trainingPlansData; 
const daysOfWeek = ["monday", "tuesday", "wednesday", "thursday", "friday", "saturday", "sunday"];
const popupAdd = document.getElementById("popup_add_plan");


const initalHtml = `<form class="training-form-container"id="popup_add_plan_form">
                        <h1 class="form-header">Add Plan</h1>

                        <div class="form-row">
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
                                    <option value="none">None</option>
                                    <option value="thresh">Threshold</option>
                                    <option value="aThresh">AM Threshold</option>  
                                    <option value="hardRepos">Hard Reps</option>
                                    <option value="race">Race</option>
                            </select>
                            <input type="text" placeholder="description" id="sessionDescription" name="sessionDescription" required>
                        </div>

                        <div class="form-row" id="sessionsContainer"></div>

                        <div class="button-group" id="buttons">
                            <button type="reset" onclick="closeAddForm()">Add</button>
                            <button type="reset" onclick="closeAddForm()">Cancel</button>
                        </div>
                    </form>`

function addSessionRow(type, desc) {
  const container = document.getElementById('popup_add_plan_form');
  const buttons = document.getElementById('buttons');
  const html = `
    <div class="form-row" id="sessionRow${counter}">
      <label for="sessionType${counter}"><b>Session</b></label>
      <select id="sessionType${counter}" name="sessionType${counter}">
        <option value="none" ${type === 'none' ? 'selected' : ''}>None</option>
        <option value="thresh" ${type === 'thresh' ? 'selected' : ''}>Threshold</option>
        <option value="aThresh" ${type === 'aThresh' ? 'selected' : ''}>AM Threshold</option>
        <option value="hardRepos" ${type === 'hardRepos' ? 'selected' : ''}>Hard Reps</option>
        <option value="race" ${type === 'race' ? 'selected' : ''}>Race</option>
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
  document.getElementById('sessionType').addEventListener('change', handleSessionInput);
  document.getElementById('sessionDescription').addEventListener('change', handleSessionInput);
}
 
function closeAddForm() {
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

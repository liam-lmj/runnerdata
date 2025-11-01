const settings = document.getElementById("settings");

function formSubmission(event) {
    event.preventDefault();

    let form = document.getElementById('settings_form');     
    if (!form.checkValidity()) {
        form.reportValidity();
        return false;
    }

    const selectedUnit = document.getElementById('selected_unit').value;
    const selectedZoneMethod = document.getElementById('selected_zone_method').value;
    const lt2Threshold = parseFloat(document.getElementById('lt2_threshold').value);
    const lt1Threshold = parseFloat(document.getElementById('lt1_threshold').value);
    const hardThreshold = parseFloat(document.getElementById('hard_threshold').value);

    if (selectedZoneMethod === "Heartrate" && hardThreshold <= lt2Threshold)
    {
        alert("Hard heartrate must be higher than LT2 heartrate.");
        document.getElementById('lt2_threshold').focus();
        return false;
    }
    if (selectedZoneMethod === "Heartrate" && lt2Threshold <= lt1Threshold)
    {
        alert("LT2 heartrate must be higher than LT1 heartrate.");
        document.getElementById('lt2_threshold').focus();
        return false;
    }
    if (selectedZoneMethod === "Pace" && lt2Threshold <= hardThreshold)
    {
        alert("Hard pace must be faster than LT2 pace.");
        document.getElementById('lt2_threshold').focus();
        return false;
    }
    if (selectedZoneMethod === "Pace" && lt1Threshold <= lt2Threshold)
    {
        alert("LT2 pace must be faster than LT1 pace.");
        document.getElementById('lt2_threshold').focus();
        return false;
    }

    updateAndCloseSettingsForm(selectedUnit, selectedZoneMethod, lt2Threshold, lt1Threshold, hardThreshold);
}


function updateAndCloseSettingsForm(unit, method, lt2, lt1, hard) {
    const currentUrl = window.location.href;

    fetch(currentUrl, {
        method: 'POST',
        headers: { 'Content-Type': 'application/json' },
        body: JSON.stringify({ 'type': 'Settings', unit, method, lt2, lt1, hard })
    })
    .then(response => response.json())
    .then(data => {
        closeSettingsForm();
    })
}

function closeSettingsForm() {
    settings.style.display = "none";
}

function openSettings() {
    settings.style.display = "block";
    popupAdd.style.display = "none";
    popup.style.display = "none";
}


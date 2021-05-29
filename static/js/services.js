// Get states data ...
async function populateStates() {
    const statesData = await fetch('/api/states')
        .then(response => response.json());
    return statesData;
}

// Get districts data based on state_id ...
async function populateDistricts(state_id) {
    const districtData = await fetch(`/api/districts/${state_id}`)
        .then(response => response.json());
    return districtData;
}

async function sendPostReq(reqUrl, data, config) {
    const result = await fetch('/register', {
            method: 'POST',
            headers: {
                'Content-Type': 'application/json'
            },
            body: JSON.stringify(data)
        })
        .then(response => response.json());
    return result;
}
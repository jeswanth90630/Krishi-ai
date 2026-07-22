const BASE_URL = "http://127.0.0.1:8000";

async function postData(endpoint, data) {
    const response = await fetch(BASE_URL + endpoint, {
        method: "POST",
        body: data
    });
    return await response.json();
}

async function getData(endpoint) {
    const response = await fetch(BASE_URL + endpoint);
    return await response.json();
}
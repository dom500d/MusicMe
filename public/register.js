document.addEventListener("DOMContentLoaded", (event) => {
    
    function server_request(url, data = {}, verb, callback) {
        return fetch(url, {
            credentials: 'same-origin',
            method: verb,
            body: JSON.stringify(data),
            headers: { 'Content-Type': 'application/json' }
        })
            .then(response => response.json())
            .then(response => {
                if (callback)
                    callback(response);
            })
            .catch(error => console.error('Error:', error));
    }
    let form = document.getElementById("register-form");
    form.addEventListener("submit", (event) => {
        event.preventDefault();
        let username = form.querySelector("#username");
        let pswd = form.querySelector("#pswd");
        let data = {"username": username, "password": pswd};
        server_request("/createUsers", data, "POST");
    })
});
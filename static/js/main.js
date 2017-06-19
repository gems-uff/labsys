fetch("/collection_methods", {
    method: "get",
    credentials: "same-origin",
    headers: {
        "Accept": "application/json",
        "Content-Type": "application/json"
    },
}).then(function(response) {
    return response.json();
}).then(function(data) {
    console.log("Data is ok", data);
}).catch(function(ex) {
    console.log("parsing failed", ex);
});

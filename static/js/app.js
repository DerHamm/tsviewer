function kickFromServer(clientId) {
    $.ajax({
        type: "GET",
        url: "/kick_from_server/" + clientId + "/Go%20Away%21",
    })
    const container = document.querySelector('.alerts');
    const alert = container.querySelector('sl-alert');
    alert.toast();
}



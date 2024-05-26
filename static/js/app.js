function kickFromServer(clientId) {
    $.ajax({
        type: "GET",
        url: "/kick_from_server/" + clientId,
    })
    const container = document.querySelector('.alerts');
    const alert = container.querySelector('sl-alert');
    alert.toast();
}



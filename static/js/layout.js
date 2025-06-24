const MESSAGE_TIMEOUT = 5000;

window.setTimeout(function() {
    // we make the flash mesage disappear after 5 seconds
    hideAlerts();
}, MESSAGE_TIMEOUT);


/**
 * Make the alert boxes fade out
 */
function hideAlerts() {
    let alerts = document.getElementsByClassName('alert-box');
    for (let i = 0; i < alerts.length; i++) {
        alerts[i].style.opacity = 0;
    }
}
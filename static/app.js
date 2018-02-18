var notificationArray = [];

document.addEventListener("DOMContentLoaded", function(event) {
    console.log('Document fully loaded');

    const $notificationCheckbox = $(".notificationCheckbox");

    var socket = io.connect(location.protocol + '//' + document.domain + ':' + location.port + '/price');
    console.log(currentDate(new Date()) + ' Socket connected!');

     // Setting up the local storage

    // If notification storage value is not defined, set it by default to true
    if (storageAvailable('localStorage')) {

        // Setting up the application if it is the first time it was opened.
        if(localStorage.getItem("showNotifications") === null){
            localStorage.setItem("showNotifications", "false");
            $notificationCheckbox.prop("checked", false);
        }

    }
    else {

        // Creating a random ID for the new created entry in the list to identify the created entry later.
        var milliseconds = new Date().getMilliseconds();
        var randomNumber = Math.floor(Math.random() * 1000);
        var newIdName = currentDate(new Date()).replace(" ", "-") + "-" + milliseconds + randomNumber + "-notification";

        // Creating the notification
        var notification = document.createElement("div");

        // Content of the notification
        var errorNotificationTemplate =
            "        <div class='content'>" +
            "            <button id='close_notification' onclick='closeNotification(\"" + newIdName + "\")'>X</button>" +
            "            Cannot access the local storage in your browser!" +
            "        </div>";

        // Accessing the notification list (<ul>)
        var notificationList = document.getElementById("notification_list");

        // Creating the element
        var entry = document.createElement('li');

        // Append the new elements to the list
        notificationList.appendChild(entry);
        entry.appendChild(notification);

        // Setting new data
        entry.id = newIdName;
        notification.className = "notification error_notification";
        notification.innerHTML = errorNotificationTemplate;

        // Push the new ID name to the notification array
        notificationArray.push(newIdName);

        // Showing the amount of currently visible notifications
        var amountNotificationsElement = document.getElementById("deleteAllNotifications").getElementsByTagName("span")[0];
        amountNotificationsElement.innerText = notificationArray.length;

    }

    // Setting up application with the values given by the application first start or by the user by changing
    // the values in the settings window.
    if(localStorage.getItem("showNotifications") === "true"){
        $notificationCheckbox.prop("checked", true);
    }else{
        $notificationCheckbox.prop("checked", false);
    }

    // "Connect" socket event
    socket.on('connect', function() {
        // Emitting a message to the server that the client is connected.
        socket.emit("client_message", {data: currentDate(new Date()) + ' I´m connected with the server!'});

        if(localStorage.getItem("showNotifications") === "true") {
            // Creating a random ID for the new created entry in the list to identify the created entry later.
            var milliseconds = new Date().getMilliseconds();
            var randomNumber = Math.floor(Math.random() * 1000);
            var newIdName = currentDate(new Date()).replace(" ", "-") + "-" + milliseconds + randomNumber + "-notification";

            // Creating the notification
            var notification = document.createElement("div");

            // Content of the notification
            var infoNotificationTemplate =
                "        <div class='content'>" +
                "            Connected to the server!" +
                "            <button id='close_notification' onclick='closeNotification(\"" + newIdName + "\")'>X</button><br>" +
                "            <small>" + currentDate(new Date()) + "</small>" +
                "        </div>";

            // Accessing the notification list (<ul>)
            var notificationList = document.getElementById("notification_list");

            // Creating the element
            var entry = document.createElement('li');

            // Append the new elements to the list
            notificationList.appendChild(entry);
            entry.appendChild(notification);

            // Setting new data
            entry.id = newIdName;
            notification.className = "notification success_notification";
            notification.innerHTML = infoNotificationTemplate;

            // Push the new ID name to the notification array
            notificationArray.push(newIdName);

            // Showing the amount of currently visible notifications
            var amountNotificationsElement = document.getElementById("deleteAllNotifications").getElementsByTagName("span")[0];
            amountNotificationsElement.innerText = notificationArray.length;
        }

    });

    socket.on('server_message', function (message) {
        console.log(currentDate(new Date()) + " Message from the server: " + message.data);

        /*
        *
        * The code below is only for development purposes.
        *
        * */

        // var milliseconds = new Date().getMilliseconds();
        // var randomNumber = Math.floor(Math.random() * 1000);
        // var newIdName = currentDate(new Date()).replace(" ", "-") + "-" + milliseconds + randomNumber + "-notification";
        //
        // var notification = document.createElement("div");
        // var infoNotificationTemplate =
        //     "        <div class='content'>" +
        //     "            Got a message by the server!" +
        //     "            <button id='close_notification' onclick='closeNotification(\"" + newIdName + "\")'>X</button><br>" +
        //     "            <small>" + currentDate(new Date()) + "</small>" +
        //     "        </div>";
        //
        // var notificationList = document.getElementById("notification_list");
        // var entry = document.createElement('li');
        // notificationList.appendChild(entry);
        // entry.appendChild(notification);
        // entry.id = newIdName;
        // notification.className = "notification info_notification";
        // notification.innerHTML = infoNotificationTemplate;
        //
        // notificationArray.push(newIdName);
        // var amountNotificationsElement = document.getElementById("deleteAllNotifications").getElementsByTagName("span")[0];
        //
        // amountNotificationsElement.innerText = notificationArray.length;
    });

    socket.on('price_message', function (msg) {
        document.getElementById("bitcoinPrice").innerText = msg.price;
        console.log(currentDate(new Date()) + ' Socket: Got successfully a (price) response! -> ' + msg.price);
        socket.emit('client_message', {data: currentDate(new Date()) + ' Got successfully the price response!'});

        /* TODO: How to set the progress bar width when a client connects while the 60 sec loop is running on the server side. */

        // Accessing the element which contains the progress bar
        var progressBar = document.getElementById("progressBarInner");

        // Giving a new width to the bar every second and restarting the progress when the width reached 100% of the screen
        // https://www.w3schools.com/howto/howto_js_progressbar.asp
        var width = 1;
        var interval = setInterval(frame, 1000);
        function frame() {
            if ((width / 60) * 100 >= 100) {
                clearInterval(interval);
            } else {
                var finalWidth = (width++ / 60) * 100;
                progressBar.style.width = finalWidth + '%';
            }
        }

        if(localStorage.getItem("showNotifications") === "true") {
            // Creating a random ID for the new created entry in the list to identify the created entry later.
            var milliseconds = new Date().getMilliseconds();
            var randomNumber = Math.floor(Math.random() * 1000);
            var newIdName = currentDate(new Date()).replace(" ", "-") + "-" + milliseconds + randomNumber + "-notification";

            // Creating the notification
            var notification = document.createElement("div");

            // Content of the notification
            var infoNotificationTemplate =
                "        <div class='content'>" +
                "            Price updated to: <u>" + msg.price + "</u>" +
                "            <button id='close_notification' onclick='closeNotification(\"" + newIdName + "\")'>X</button><br>" +
                "            <small>" + currentDate(new Date()) + "</small>" +
                "        </div>";

            // Accessing the notification list (<ul>)
            var notificationList = document.getElementById("notification_list");

            // Creating the element
            var entry = document.createElement('li');
            notificationList.appendChild(entry);

            // Append the new elements to the list
            entry.appendChild(notification);

            // Setting new data
            entry.id = newIdName;
            notification.className = "notification info_notification";
            notification.innerHTML = infoNotificationTemplate;

            // Push the new ID name to the notification array
            notificationArray.push(newIdName);

            // Showing the amount of currently visible notifications
            var amountNotificationsElement = document.getElementById("deleteAllNotifications").getElementsByTagName("span")[0];
            amountNotificationsElement.innerText = notificationArray.length;
        }

    });

    // Error in very rare moments
    // The settings for the notifications won´t play a role here because this is a error. Period.
    socket.on('error', function (error) {

        // Creating a random ID for the new created entry in the list to identify the created entry later.
        var milliseconds = new Date().getMilliseconds();
        var randomNumber = Math.floor(Math.random() * 1000);
        var newIdName = currentDate(new Date()).replace(" ", "-") + "-" + milliseconds + randomNumber + "-notification";

        // Creating the notification
        var notification = document.createElement("div");

        // Content of the notification
        var errorNotificationTemplate =
            "        <div class='content'>" +
            "            <button id='close_notification' onclick='closeNotification(\"" + newIdName + "\")'>X</button>" +
            "            Error occurred when trying to connect to the server!" +
            "        </div>";

        // Accessing the notification list (<ul>)
        var notificationList = document.getElementById("notification_list");

        // Creating the element
        var entry = document.createElement('li');

        // Append the new elements to the list
        notificationList.appendChild(entry);
        entry.appendChild(notification);

        // Setting new data
        entry.id = newIdName;
        notification.className = "notification error_notification";
        notification.innerHTML = errorNotificationTemplate;

        // Push the new ID name to the notification array
        notificationArray.push(newIdName);

        // Showing the amount of currently visible notifications
        var amountNotificationsElement = document.getElementById("deleteAllNotifications").getElementsByTagName("span")[0];
        amountNotificationsElement.innerText = notificationArray.length;

    });

    // console.log(socket);

    // Check if the close button for the settings dialog window was pressed (event handler)
    var closeButton = document.getElementById('closeSettingsDialogWindow');
    closeButton.onclick = function () {
        var settingsDialogWindow = document.getElementById("settingsDialogWindow");
        settingsDialogWindow.style.display = "none";
    };

    $notificationCheckbox.click(function () {
        localStorage.setItem("showNotifications", this.checked.toString());
    });

});

// Adding a zero if the hour, minute or seconds number is below zero
function addZero(i) {
    if (i < 10) {
        i = "0" + i;
    }
    return i;
}

// Function which returns the current date in a more readable string
function currentDate(/** Date */date) {
    var day = date.getDate();
    var month = date.getMonth() + 1;
    var year = date.getFullYear();

    var hour = addZero(date.getHours());
    var minute = addZero(date.getMinutes());
    var seconds = addZero(date.getSeconds());

    return "<" + month + "/" + day + "/" + year + " " + hour + ":" + minute + ":" + seconds + ">";
}

// Closes a notification with the given id of the notification.
function closeNotification(id) {
    var notification = document.getElementById(id);

    var index = notificationArray.indexOf(id);
    if(index > -1){
        notificationArray.splice(index, 1);
    }

    var amountNotificationsElement = document.getElementById("deleteAllNotifications").getElementsByTagName("span")[0];
    amountNotificationsElement.innerText = notificationArray.length;

    notification.parentNode.removeChild(notification);
}

// Function for deleting all notifications
function deleteAllNotifications() {
    var notificationList = document.getElementById("notification_list");

    notificationArray = [];

    // Thanks to Gabriel McAdams & Denilson Sá Maia -> https://stackoverflow.com/questions/3955229/remove-all-child-elements-of-a-dom-node-in-javascript
    while (notificationList.firstChild) {
        notificationList.removeChild(notificationList.firstChild);
    }

    var amountNotificationsElement = document.getElementById("deleteAllNotifications").getElementsByTagName("span")[0];
    amountNotificationsElement.innerText = notificationArray.length;
}

// Function for opening the settings dialog window
function openSettingsDialog() {
    var settingsDialogWindow = document.getElementById("settingsDialogWindow");
    settingsDialogWindow.style.display = "block";
}

// Check if the a storage is available
function storageAvailable(type) {
    try {
        var storage = window[type],
            x = '__storage_test__';
        storage.setItem(x, x);
        storage.removeItem(x);
        return true;
    }
    catch(e) {
        return e instanceof DOMException && (
            // everything except Firefox
            e.code === 22 ||
            // Firefox
            e.code === 1014 ||
            // test name field too, because code might not be present
            // everything except Firefox
            e.name === 'QuotaExceededError' ||
            // Firefox
            e.name === 'NS_ERROR_DOM_QUOTA_REACHED') &&
            // acknowledge QuotaExceededError only if there's something already stored
            storage.length !== 0;
    }
}


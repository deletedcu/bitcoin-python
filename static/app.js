document.addEventListener("DOMContentLoaded", function(event) {
    console.log('Document fully loaded');

    var socket = io.connect(location.protocol + '//' + document.domain + ':' + location.port + '/price');
    console.log(currentDate(new Date()) + ' Socket connected!');

    socket.on('connect', function() {
        socket.emit("client_message", {data: currentDate(new Date()) + ' I´m connected with the server!'});
    });

    socket.on('server_message', function (message) {
        console.log(currentDate(new Date()) + " Message from the server: " + message.data);
    });

    socket.on('price_message', function (msg) {
        document.getElementById("bitcoinPrice").innerText = msg.price;
        console.log(currentDate(new Date()) + ' Socket: Got successfully a (price) response! -> ' + msg.price);
        socket.emit('client_message', {data: currentDate(new Date()) + ' Got successfully the price response!'});

        /* TODO: How to set the progress bar width when a client connects while the 60 sec loop is running on the server side. */

        var progressBar = document.getElementById("progressBarInner");

        var width = 1;
        var interval = setInterval(frame, 1000);
        function frame() {
            if ((width / 60) * 100 >= 100) {
                interval(id);
            } else {
                var finalWidth = (width++ / 60) * 100;
                progressBar.style.width = finalWidth + '%';
            }
        }
    });

    console.log(socket);

});

function addZero(i) {
    if (i < 10) {
        i = "0" + i;
    }
    return i;
}

function currentDate(/** Date */date) {
    var day = date.getDate();
    var month = date.getMonth();
    var year = date.getFullYear();

    var hour = addZero(date.getHours());
    var minute = addZero(date.getMinutes());
    var seconds = addZero(date.getSeconds());

    return "<" + month + "/" + day + "/" + year + " " + hour + ":" + minute + ":" + seconds + ">";
}




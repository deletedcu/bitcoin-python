document.addEventListener("DOMContentLoaded", function(event) {
    console.log('Document fully loaded');

    var socket = io.connect(location.protocol + '//' + document.domain + ':' + location.port + '/price');
    console.log('Socket connected!');

    socket.on('connect', function() {
        socket.emit('my_event', {data: 'I\'m connected!'});
    });

    socket.on('my_event', function (message) {
       console.log("Got new message: " + message.data);
    });

    socket.on('priceresponse', function (msg) {
        console.log("Got an socket response!");
        console.log('Socket response contains:');
        console.log(msg);
        document.getElementById("bitcoinPrice").innerText = msg.price;
    });

});




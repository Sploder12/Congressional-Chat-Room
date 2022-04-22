$(document).ready(function() {
    var domain = "localhost";
    var port = "5000";
    var socket = io.connect('http://'+domain+':'+port);
    socket.on('message', function(msg) {
        $("#messages").append('<p>'+msg+'</p>');
    })
    $('#sendbutton').on('click', function() {
        socket.send([$('#myMessage').val(), "botMessage"]);
        $('#myMessage').val('');
    })
    $('#myMessage').keypress(function(event) {
        if (event.keyCode == 13 || event.which == 13) {
            socket.send([$('#myMessage').val(), "botMessage"]);
            $('#myMessage').val('');
        }
    })
})
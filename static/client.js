$(document).ready(function() {
    var messageBox = document.getElementById('myMessage');
    var subButton = document.getElementById('sendbutton');
    subButton.style.display = 'none';
    messageBox.style.display = 'none';
    var domain = "localhost";
    var port = "5000";
    var socket = io.connect('http://'+domain+':'+port);
    socket.on('connect', function() {
        socket.send(["User connecting...", "message"]);
    })
    socket.on('message', function(msg) {
        $("#messages").append('<p>'+msg+'</p>');
    })
    $('#sendbutton').on('click', function() {
        socket.send(["&lt;"+$('#username').val()+"&gt; "+$('#myMessage').val(), "message"]);
        $('#myMessage').val('');
    })
    $('#userbutton').on('click', function() {
        socket.send([$("#username").val()+" has connected!", "message"]);
        socket.send([$('#username').val(), "username"]);
    })
})
function toggleMessagebox() {
        var messageBox = document.getElementById('myMessage');
        var subButton = document.getElementById('sendbutton');
        var userButton = document.getElementById('userbutton');
        var userName = document.getElementById('username'); 
        subButton.style.display = 'block';
        messageBox.style.display = 'block';
        userName.style.display = 'none';
        userButton.style.display = 'none';

    }
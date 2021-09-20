from flask import Flask, render_template, redirect, request, url_for
from flask_socketio import SocketIO, send

app = Flask(__name__)
app.config['SECRET_KEY'] = 'secret!'
socketio = SocketIO(app)

@app.route("/", methods=["GET", "POST"])
def home():
    print(request.method)
    if request.method == "POST":
        if request.form['button'] == "About":
            return redirect(url_for("about"))
        if request.form['button'] == "Enter Chat":
            return redirect(url_for("chat"))
    return render_template("home.html")

@app.route("/about", methods=["GET", "POST"])
def about():
    return render_template("about.html")

@app.route("/chat", methods=["GET", "POST"])
def chat():
    return render_template("chat.html")

@socketio.on('message')
def handle_message(data):
    print('received message: ' + data)
    send(data, broadcast=True)


if __name__ == '__main__':
    ip = "localhost" 
    port = 8000
    if "ip" not in locals():
        ip = input("Enter the IP: ")
    if "port" not in locals():
        port = int(input("Enter the Port: "))
    socketio.run(app, host=ip, port=port)
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

@socketio.on('message', namespace="/")
def handle_message(data2):
    if data2[0] != "":
        if data2[1] == "message":
            print(data2)
            print('received message: ' + data2[0])
            send(data2[0], broadcast=True)
        elif data2[1] == "username":
            print(data2[0]+" connected")
    print(data2)

if __name__ == '__main__':
    socketio.run(app) # Runs on localhost:5000
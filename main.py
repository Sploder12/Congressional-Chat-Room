from flask import Flask, render_template, redirect, request, url_for

app = Flask(__name__)

@app.route("/", methods=["GET", "POST"])
def home():
    if request.method == "POST":
        return redirect(url_for("irc"))
    return render_template("home.html")

@app.route("/irc", methods=["GET", "POST"])
def irc():
    return render_template("irc.html")

if __name__ == '__main__':
    ip = "localhost" 
    port = "80"
    if "ip" not in locals():
        ip = input("Enter the IP: ")
    if "port" not in locals():
        port = int(input("Enter the Port: "))
    while True:
        debug = input("Debug Mode (changes to local only)? (y/n): ")
        if debug == "y" or debug == "n":
            break
        else:
            print("Invalid Response")
    if debug == "y":
        debug = True
    elif debug == "n":
        debug == False
    app.run(host=ip, port=port, debug=debug, threaded=True, use_reloader=False)
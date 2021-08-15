from flask import Flask, render_template, redirect, request, url_for

app = Flask(__name__)

@app.route("/", methods=["GET", "POST"])
def home():
    # if request.method == "POST":
    return render_template("home.html")

if __name__ == '__main__':
    ip = "192.168.68.111" 
    port = "8000"
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
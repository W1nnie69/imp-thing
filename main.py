from flask import Flask, render_template, url_for, redirect, request

app = Flask(__name__)

@app.route("/")
def redirect():
    return redirect(url_for('login'))

@app.route("/login")
def login():
    return render_template("login.html")

@app.route("/home", methods=["POST"])
def home():
    username = request.form["username"]
    return render_template("home.html", user_name=username)



if __name__ == '__main__':
    app.run(debug=True)
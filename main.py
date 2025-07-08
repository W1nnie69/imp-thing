from flask import Flask, render_template, url_for, redirect, request, jsonify
import json
import os

app = Flask(__name__)

def load_notes():
    if os.path.exists("notes.json"):
        with open("notes.json", "r") as f:
            content = f.read().strip()
            if content:
                try:
                    data = json.loads(content)
                    if isinstance(data, list):
                        return data
                    else:
                        return []
                except json.JSONDecodeError:
                    return []
            else:
                return []
    else:
        return []
    

def write_notes_to_file(notes):
    with open("notes.json", "w") as f:
        json.dump(notes, f, indent=4)


@app.route("/api/notes", methods=["GET"])
def get_notes():
    notes = load_notes()
    return jsonify(notes)


@app.route("/")
def login_redirect():
    return redirect(url_for('login'))


@app.route("/login")
def login():
    return render_template("login.html")


@app.route("/home", methods=["POST"])
def home():
    username = request.form["username"]
    return render_template("home.html", user_name=username)


@app.route("/api/notes", methods=["POST"])
def save_notes():
    note = request.get_json()
    notes = load_notes()

    for n in notes:
        if n['id'] == note['id']:
            n.update(note)
            break

    else:
        notes.append(note)

    write_notes_to_file(notes)
    return jsonify({"status": "saved"})


if __name__ == '__main__':
    app.run(debug=True)
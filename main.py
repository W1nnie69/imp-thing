from flask import Flask, render_template, url_for, redirect, request, jsonify
import json
import os
import requests

app = Flask(__name__)

import os
print("Current working directory:", os.getcwd())

def load_workspaces():
    if os.path.exists("workspaces.json"):
        with open("workspaces.json", "r") as f:
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
    

def load_notes():
    print("Attempting to load notes...")  # <---- add this
    if os.path.exists("notes.json"):
        with open("notes.json", "r") as f:
            content = f.read().strip()
            print("Raw notes.json content:", content)  # <---- add this too
            if content:
                try:
                    data = json.loads(content)
                    print("Parsed data:", data)  # <---- and this
                    if isinstance(data, list):
                        return data
                    else:
                        return []
                except json.JSONDecodeError as e:
                    print("JSON Decode Error:", e)
                    return []
            else:
                print("notes.json is empty")
                return []
    else:
        print("notes.json file not found")
        return []


def write_workspaces_to_file(workspaces):
    with open("workspaces.json", "w") as f:
        json.dump(workspaces, f, indent=4)
    

def write_notes_to_file(notes):
    with open("notes.json", "w") as f:
        json.dump(notes, f, indent=4)


@app.route("/")
def login_redirect():
    return redirect(url_for('welcome'))


@app.route("/welcome")
def welcome():
    return render_template("welcome.html")


@app.route("/login")
def login():
    return render_template("login.html")


@app.route("/signup")
def signup():
    return render_template("signup.html")


@app.route("/dashboard", methods=["POST"])
def dashboard():
    username = request.form["username"]
    return render_template("dashboard.html", user_name=username)


@app.route("/workspace")
def workspace():
    return render_template("workspace.html")


@app.route("/api/notes", methods=["GET"])
def get_notes():
    notes = load_notes()
    return jsonify(notes)


@app.route("/api/notes", methods=["POST"])
def save_notes():
    note = request.get_json()

    # Validate required fields (optional)
    required_keys = {'id', 'content', 'top', 'left', 'width', 'height', 'color'}
    if not required_keys.issubset(note.keys()):
        return jsonify({"error": "Missing required note fields"}), 400

    notes = load_notes()

    # Remove any existing note with the same ID
    notes = [n for n in notes if n['id'] != note['id']]

    # Append the new/updated note
    notes.append(note)

    # Write back clean, valid JSON array
    write_notes_to_file(notes)

    return jsonify({"status": "saved"})


@app.route("/api/duckduckgo")
def proxy_duckduckgo():
    query = request.args.get("q")
    if not query:
        return jsonify({"error": "Missing query"}), 400
    
    url = f"https://api.duckduckgo.com/?q={query}&format=json&no_redirect=1&no_html=1"
    response = requests.get(url)
    
    return response.json()


if __name__ == '__main__':
    app.run(debug=True)
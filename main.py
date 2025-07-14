from flask import Flask, render_template, url_for, redirect, request, jsonify, session, flash
import json
import os
import requests
import deepseek as ds

app = Flask(__name__)
app.secret_key = 'super-secret-key-123'


print("Current working directory:", os.getcwd())


def load_users():
    with open('users.json', 'r') as f:
        return json.load(f)
    
    return []


def load_usr_data(username):
    filepath = f"./usr-data/{username}.json"
    if os.path.exists(filepath):
        with open(filepath, "r") as f:
            return json.load(f)
        
    else:
        # Create default workspace if none exists
        default_workspace = [{
            "workspace_id": 1,
            "workspace_name": "Default",
            "notes": []
        }]
        with open(filepath, "w") as f:
            json.dump(default_workspace, f, indent=4)
        return default_workspace
        

def write_user_data(username, data):
    filepath = f"./usr-data/{username}.json"
    with open(filepath, "w") as f:
        json.dump(data, f, indent=4)


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


@app.route("/login", methods=["GET", "POST"])
def login():
    if request.method == "POST":
        username = request.form["username"]
        # password = request.form["password"]
        users = load_users()

        for user in users:
            if user["username"] == username:
                session["username"] = username
                return redirect(url_for("dashboard"))
            
        flash("Invalid username or password")   
        return redirect(url_for("login"))

    return render_template("login.html")


@app.route("/signup")
def signup():
    return render_template("signup.html")


@app.route("/dashboard")
def dashboard():
    if "username" not in session:
        return redirect(url_for("login"))
    return render_template("dashboard.html", username=session["username"])


@app.route("/workspace")
def workspace():
    return render_template("workspace.html")


@app.route("/api/notes", methods=["GET"])
def get_notes():
    username = session.get("username")
    if not username:
        return jsonify([])
    
    data = load_usr_data(username)
    notes = []

    for ws in data:
        notes.extend(ws["notes"])

    return jsonify(notes)


@app.route("/api/notes", methods=["POST"])
def save_notes():
    note = request.get_json()
    username = session.get("username")
    if not username:
        return jsonify({"error": "Not logged in"}), 401
    
    data = load_usr_data(username)
    workspace_id = 1

    for ws in data:
        if ws["workspace_id"] == workspace_id:
            for n in ws["notes"]:
                if n["id"] == note["id"]:
                    n.update(note)
                    break

            else:
                ws["notes"].append(note)
            break

    write_user_data(username, data)
    return jsonify({"status": "saved"})


@app.route("/api/duckduckgo")
def proxy_duckduckgo():
    query = request.args.get("q")
    if not query:
        return jsonify({"error": "Missing query"}), 400
    
    url = f"https://api.duckduckgo.com/?q={query}&format=json&no_redirect=1&no_html=1"
    response = requests.get(url)
    
    return response.json()


@app.route("/api/askai", methods=["POST"])
def ask_deepseek():
    data = request.get_json()
    data = data['notes']
    data = str(data)
    print(data)
    response = ds.build_request(data)
    if not response:
        print("Something went wrong, no response from ai")
        return jsonify({"error": "No response from AI"}), 500


    else:
        print(response)
        return jsonify({"suggestions": response})

if __name__ == '__main__':
    app.run(debug=True)
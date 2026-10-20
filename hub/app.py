from pathlib import Path
import json
import os

from flask import Flask, redirect, render_template, request, send_from_directory, url_for
import data_reload

app = Flask(__name__)
BASE_DIR = Path(__file__).resolve().parent
RUNTIME_DIR = Path(os.environ.get("WSN_RUNTIME_DIR", BASE_DIR))
data_file_path = os.environ.get("WSN_DATA", str(RUNTIME_DIR / "data.json"))
config_file_path = os.environ.get("WSN_CONFIG", str(RUNTIME_DIR / "wsn_config.json"))
events_table_path = os.environ.get("WSN_EVENTS", str(RUNTIME_DIR / "events_table.csv"))

def load_data():
    data_reload.data_reload(data_file_path, events_table_path)
    with open(data_file_path, "r", encoding="utf-8") as file:
        return json.load(file)

@app.route("/images/<filename>")
def serve_image(filename):
    return send_from_directory(RUNTIME_DIR, filename)

@app.route("/")
def index():
    data = load_data()
    return render_template("index.html", rooms=data["rooms"])

@app.route("/edit")
def edit():
    with open(config_file_path, "r", encoding="utf-8") as file:
        config_data = json.load(file)
    return render_template("edit.html", config=json.dumps(config_data, indent=4))

@app.route("/save", methods=["POST"])
def save():
    new_content = request.form["config"]
    try:
        config_data = json.loads(new_content)
    except json.JSONDecodeError as error:
        return f"Invalid JSON configuration: {error}", 400
    with open(config_file_path, "w", encoding="utf-8") as file:
        json.dump(config_data, file, indent=4)
        file.write("\n")
    return redirect(url_for("index"))

@app.route("/room/<room_id>")
def room(room_id):
    data = load_data()
    room_data = data["rooms"].get(room_id, {})
    return render_template("room.html", room_id=room_id, room=room_data)

@app.route("/set_room_status/<room_id>", methods=["POST"])
def set_room_status(room_id):
    data = load_data()
    data["rooms"][room_id]["status"] = "OK"
    with open(data_file_path, "w", encoding="utf-8") as file:
        json.dump(data, file, indent=4)
        file.write("\n")
    return redirect(url_for("room", room_id=room_id))

@app.route("/set_cabinet_status/<room_id>/<cabinet_id>", methods=["POST"])
def set_cabinet_status(room_id, cabinet_id):
    data = load_data()
    data["rooms"][room_id]["cabinets"][cabinet_id]["status"] = "OK"
    with open(data_file_path, "w", encoding="utf-8") as file:
        json.dump(data, file, indent=4)
        file.write("\n")
    return redirect(url_for("room", room_id=room_id))

if __name__ == "__main__":
    app.run(debug=True)

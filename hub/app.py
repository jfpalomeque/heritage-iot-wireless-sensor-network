from flask import Flask, render_template, request, redirect, url_for, jsonify, send_from_directory
import json
import os
import data_reload

app = Flask(__name__)

data_file_path = 'data.json'
config_file_path = 'wsn_config.json'
events_table_path = 'events_table.csv'

def load_data():
    data_reload.data_reload(data_file_path, events_table_path)
    with open(data_file_path, 'r') as file:
        return json.load(file)

@app.route('/images/<filename>')
def serve_image(filename):
    return send_from_directory(os.path.dirname(__file__), filename)

@app.route('/')
def index():
    print("Index page accessed")
    data = load_data()
    return render_template('index.html', rooms=data['rooms'])

@app.route('/edit')
def edit():
    print("Edit page accessed")
    with open(config_file_path, 'r') as file:
        config_data = json.load(file)
    return render_template('edit.html', config=json.dumps(config_data, indent=4))

@app.route('/save', methods=['POST'])
def save():
    print("Save endpoint accessed")
    new_content = request.form['config']
    with open(data_file_path, 'w') as file:
        file.write(new_content)
    return redirect(url_for('index'))

@app.route('/room/<room_id>')
def room(room_id):
    print(f"Room page for {room_id} accessed")
    data = load_data()
    room_data = data['rooms'].get(room_id, {})
    return render_template('room.html', room_id=room_id, room=room_data)

@app.route('/set_room_status/<room_id>', methods=['POST'])
def set_room_status(room_id):
    print(f"Set room status to OK for {room_id}")
    data = load_data()
    data['rooms'][room_id]['status'] = 'OK'
    with open(data_file_path, 'w') as file:
        json.dump(data, file, indent=4)
    return redirect(url_for('room', room_id=room_id))

@app.route('/set_cabinet_status/<room_id>/<cabinet_id>', methods=['POST'])
def set_cabinet_status(room_id, cabinet_id):
    print(f"Set cabinet status to OK for {cabinet_id} in {room_id}")
    data = load_data()
    data['rooms'][room_id]['cabinets'][cabinet_id]['status'] = 'OK'
    with open(data_file_path, 'w') as file:
        json.dump(data, file, indent=4)
    return redirect(url_for('room', room_id=room_id))

if __name__ == '__main__':
    print("Starting Flask application")
    app.run(debug=True)

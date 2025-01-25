from flask import Flask, request, jsonify
import json
import os

app = Flask(__name__)
DATA_FILE = 'routine_data.json'

# Function to read data from the file
def read_data():
    if os.path.exists(DATA_FILE):
        with open(DATA_FILE, 'r') as file:
            return json.load(file)
    return {"routine": {"exercises": []}}

# Function to write data to the file
def write_data(data):
    with open(DATA_FILE, 'w') as file:
        json.dump(data, file, indent=4)

@app.route('/routine', methods=['POST'])
def add_routine():
    data = request.json
    # Validate incoming JSON structure
    if 'routine' not in data or 'exercises' not in data['routine']:
        return jsonify({"error": "Invalid data format"}), 400
    
    # Read existing data
    existing_data = read_data()
    
    # Append new exercises
    existing_data['routine']['exercises'].extend(data['routine']['exercises'])
    
    # Write updated data back to the file
    write_data(existing_data)
    
    return jsonify({"message": "Routine added successfully"}), 201

@app.route('/routine', methods=['GET'])
def get_routine():
    data = read_data()
    return jsonify(data), 200

if __name__ == '__main__':
    app.run(debug=True)

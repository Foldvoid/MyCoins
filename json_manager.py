import json
import os

# Read the entire JSON file
def read_json(file_path):
    if not os.path.exists(file_path):
        return []
    with open(file_path, "r") as f:
        return json.load(f)

# Write back to JSON file
def write_json(file_path, data):
    with open(file_path, "w") as f:
        json.dump(data, f, indent=2)

# CREATE: Add a new record
def create_entry(file_path, entry):
    data = read_json(file_path)
    data.append(entry)
    write_json(file_path, data)

# READ: Get all records or one by ID
def read_entry(file_path, entry_id=None):
    data = read_json(file_path)
    if entry_id is None:
        return data
    return next((item for item in data if item["id"] == entry_id), None)

# UPDATE: Update an existing record
def update_entry(file_path, entry_id, updates):
    data = read_json(file_path)
    for item in data:
        if item["id"] == entry_id:
            item.update(updates)
            break
    write_json(file_path, data)

# DELETE: Remove a record
def delete_entry(file_path, entry_id):
    data = read_json(file_path)
    data = [item for item in data if item["id"] != entry_id]
    write_json(file_path, data)
import os
import json

file_dir = os.environ.get('FILE_STORE_PATH') or os.getcwd()

def write(data, user_id):
    json_body = json.dumps(data or {})
    file_path = os.path.join(file_dir, f"{user_id}.json")
    with open(file_path, 'w') as f:
        f.write(json_body)
    return "ok", 200

def read(user_id):
    file_path = os.path.join(file_dir, f"{user_id}.json")
    if os.path.isfile(file_path):
        with open(file_path, 'r') as f:
            file_data = json.load(f)
        return file_data, 200
    else:
        return "File not found", 404

from flask import Flask, jsonify, request
from flask_jwt_extended import JWTManager, jwt_required, get_jwt_identity
from dotenv import load_dotenv
from file_store import read, write
import os

load_dotenv()

app = Flask(__name__)
app.config['JWT_SECRET_KEY'] = os.environ['JWT_SECRET']
app.config['JWT_IDENTITY_CLAIM'] = 'id'
jwt = JWTManager(app)

@app.route('/api/sync', methods=['GET', 'PUT'])
@jwt_required()
def sync():
    user_id = get_jwt_identity()
    users = os.environ['JWT_USERS'].split(',')
    if user_id not in users:
        return jsonify({'status': 'error', 'message': 'Unauthorized!'}), 401

    if request.method == 'GET':
        return read(user_id)

    if request.method == 'PUT':
        data = request.get_json()
        return write(data, user_id)

    return jsonify({'status': 'error', 'message': 'Unsupported method!'}), 405

@app.route('/test', methods=['GET'])
def test():
    return 'ok'


if __name__ == '__main__':
  port = os.environ['PORT']
  host = os.environ['HOST']
  app.run(
    host=host,
    port=port,
    debug=True,
    load_dotenv=True
  )
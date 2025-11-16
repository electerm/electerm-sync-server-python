from flask import Flask, jsonify, request
from flask_jwt_extended import JWTManager, jwt_required, get_jwt_identity
from dotenv import load_dotenv
import os
import logging
import sys

# Add src directory to Python path so imports work in both direct execution and module execution
if os.path.dirname(__file__) not in sys.path:
    sys.path.insert(0, os.path.dirname(__file__))

from data_store import read, write

# Configure logging
logging.basicConfig(level=logging.INFO, format='%(asctime)s - %(levelname)s - %(message)s')
logger = logging.getLogger(__name__)

load_dotenv()

app = Flask(__name__)
app.config['JWT_SECRET_KEY'] = os.environ['JWT_SECRET']
app.config['JWT_IDENTITY_CLAIM'] = 'id'
jwt = JWTManager(app)

@jwt.invalid_token_loader
def invalid_token_callback(error_string):
    logger.warning(f"Invalid token provided: {error_string}")
    return jsonify({'status': 'error', 'message': 'Invalid token'}), 422

@jwt.expired_token_loader
def expired_token_callback(jwt_header, jwt_payload):
    logger.warning("Expired token used")
    return jsonify({'status': 'error', 'message': 'Token expired'}), 422

@jwt.unauthorized_loader
def unauthorized_callback(error_string):
    logger.warning(f"Unauthorized access: {error_string}")
    return jsonify({'status': 'error', 'message': 'Missing or invalid token'}), 422

@app.route('/api/sync', methods=['GET', 'PUT', 'POST'])
@jwt_required()
def sync():
    user_id = get_jwt_identity()
    users = os.environ['JWT_USERS'].split(',')
    
    if user_id not in users:
        logger.warning(f"Unauthorized access attempt by user: {user_id}")
        return jsonify({'status': 'error', 'message': 'Unauthorized!'}), 401

    if request.method == 'GET':
        data, status = read(user_id)
        if status == 200:
            return jsonify(data), 200
        else:
            return jsonify({'status': 'error', 'message': data}), status

    if request.method == 'POST':
        logger.info(f"User {user_id} testing sync endpoint")
        return 'test ok'

    if request.method == 'PUT':
        logger.info(f"User {user_id} writing sync data")
        data = request.get_json()
        status_msg, status = write(data, user_id)
        if status == 200:
            return status_msg, 200
        else:
            return jsonify({'status': 'error', 'message': status_msg}), status

    return jsonify({'status': 'error', 'message': 'Unsupported method!'}), 405

@app.route('/test', methods=['GET'])
def test():
    logger.info("Test endpoint accessed")
    return 'ok'


if __name__ == '__main__':
  port = int(os.environ.get('PORT', 5000))
  host = os.environ.get('HOST', '127.0.0.1')

  logger.info("=== =========== ===")
  logger.info("=== Electerm Sync Server Starting ===")
  logger.info(f"Server will run at: http://{host}:{port}")
  logger.info(f"API endpoint: http://{host}:{port}/api/sync")
  logger.info(f"Test endpoint: http://{host}:{port}/test")
  
  # Show JWT configuration
  jwt_secret = os.environ.get('JWT_SECRET', '')
  jwt_users = os.environ.get('JWT_USERS', '')
  
  if jwt_secret:
    logger.info("JWT_SECRET configured (check your .env file)")
  else:
    logger.warning("JWT_SECRET not configured in environment variables")
  
  if jwt_users:
    users_list = jwt_users.split(',')
    logger.info(f"Authorized users: {', '.join(users_list)}")
    logger.info(f"Use one of these as JWT_USER_NAME in Electerm: {users_list[0]}")
  else:
    logger.warning("No JWT_USERS configured in environment variables")
  
  # Show data store location
  from data_store import db_path
  logger.info(f"Data store location: {db_path}")
  
  logger.info("=== Configuration for Electerm ===")
  logger.info(f"Server URL: http://{host}:{port}")
  logger.info("Set these values in Electerm sync settings:")
  logger.info("- Custom sync server URL: http://{host}:{port}")
  logger.info("- JWT_SECRET: check your .env file")
  logger.info("- JWT_USER_NAME: (see authorized users above)")
  logger.info("=== Server Ready ===")
  logger.info("=== =========== ===")
  
  app.run(
    host=host,
    port=port,
    debug=True,
    load_dotenv=True
  )
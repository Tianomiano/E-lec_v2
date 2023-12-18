from flask import jsonify, Blueprint, request
from models.engine.db_storage import db, Users
import bcrypt
from flask_bcrypt import generate_password_hash, check_password_hash
import jwt
import datetime
from datetime import datetime

users_bp = Blueprint('users', __name__)

@users_bp.route('/users', methods=['GET'])
def get_all_users():
    # an endpoint to access all users for the platform
    
    users = Users.query.all()
    users_data = [{
        'user_id': user.user_id,
        'username': user.username,
        'email': user.email
    } for user in users]
    return jsonify(users_data)

@users_bp.route('/getuser', methods=['GET'])
def get_user_details():
    # enable access to a specific logged in user profile

    token = request.headers.get('Authorization')
    if not token:
        return jsonify({'error': 'Authorization token missing'}), 401

    try:
        token_data = jwt.decode(token, 'miano123', algorithms=['HS256'])
        user_id = token_data['user_id']
    except jwt.ExpiredSignatureError:
        return jsonify({'error': 'Token expired'}), 401
    except jwt.InvalidTokenError:
        return jsonify({'error': 'Invalid token'}), 401

    user = Users.query.get(user_id)
    if not user:
        return jsonify({'error': 'User not found'}), 404
    user_data = {
        'user_id': user.user_id,
        'username': user.username,
        'email': user.email
    }
    return jsonify(user_data)

@users_bp.route('/users/passwd/update', methods=['PUT'])
def update_user_password():
    # enable users to change their password

    token = request.headers.get('Authorization')
    if not token:
        return jsonify({'error': 'Authorization token missing'}), 401

    try:
        token_data = jwt.decode(token, 'miano123', algorithms=['HS256'])
        user_id = token_data['user_id']
    except jwt.ExpiredSignatureError:
        return jsonify({'error': 'Token expired'}), 401
    except jwt.InvalidTokenError:
        return jsonify({'error': 'Invalid token'}), 401

    user = Users.query.get(user_id)
    if not user:
        return jsonify({'error': 'User not found'}), 404
    
    data = request.get_json()
    new_password = data.get('new_password')
    confirm_password = data.get('confirm_password')

    if new_password != confirm_password:
        return jsonify({'error': 'New password and confirm password do not match'}), 400

    if check_password_hash(user.passwd, new_password):
        return jsonify({'error': 'New password cannot be the same as the old password'}), 400

    hashed_password = generate_password_hash(new_password).decode('utf-8')
    user.passwd = hashed_password
    db.session.commit()

    return jsonify({'message': 'Password updated successfully'}), 200

@users_bp.route('/getuser/update', methods=['PUT'])
def update_user():
    # enable users to edit/update their profile

    token = request.headers.get('Authorization')
    if not token:
        return jsonify({'error': 'Authorization token missing'}), 401

    try:
        token_data = jwt.decode(token, 'miano123', algorithms=['HS256'])
        user_id = token_data['user_id']
    except jwt.ExpiredSignatureError:
        return jsonify({'error': 'Token expired'}), 401
    except jwt.InvalidTokenError:
        return jsonify({'error': 'Invalid token'}), 401
    
    user = Users.query.get(user_id)

    new_username = request.json.get('new_username')
    new_email = request.json.get('new_email')

    if not new_username and not new_email:
        return jsonify({'error': 'New username or email required'}), 400

    if new_username:
        user.username = new_username

    if new_email:
        user.email = new_email

    db.session.commit()

    return jsonify({'message': 'User details updated successfully'})

@users_bp.route('/users/close_account', methods=['DELETE'])
def close_account():
    # enable users to delete their account and associated details

    token = request.headers.get('Authorization')
    if not token:
        return jsonify({'error': 'Authorization token missing'}), 401

    try:
        token_data = jwt.decode(token, 'miano123', algorithms=['HS256'])
        user_id = token_data['user_id']
    except jwt.ExpiredSignatureError:
        return jsonify({'error': 'Token expired'}), 401
    except jwt.InvalidTokenError:
        return jsonify({'error': 'Invalid token'}), 401
    
    user = Users.query.get(user_id)

    # Confirm with password
    password = request.json.get('password')
    if not bcrypt.checkpw(password.encode('utf-8'), user.passwd.encode('utf-8')):
        return jsonify({'error': 'Invalid password'}), 401

    # Delete user's articles, questions, replies, and account
    articles = user.articles
    for article in articles:
        db.session.delete(article)

    # Delete user's questions
    questions = user.questions
    for question in questions:
        db.session.delete(question)

    # Delete user's replies
    replies = user.replies
    for reply in replies:
        db.session.delete(reply)

    # Delete user's account
    db.session.delete(user)
    db.session.commit()

    # Update deletion_requested timestamp
    user.deletion_requested = datetime.utcnow()
    db.session.commit()

    return jsonify({'message': 'Account and associated data marked for deletion', 'logged_in': False}), 200

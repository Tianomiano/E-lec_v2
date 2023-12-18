from flask import Blueprint, request, jsonify
from models.engine.db_storage import db, Users
import bcrypt
import jwt
from flask import session

login_bp = Blueprint('login', __name__)

@login_bp.route('/login', methods=['POST'])
def login():
    data = request.get_json()

    email = data.get('email')
    password = data.get('password')

    if not email or not password:
        return jsonify({'error': 'Missing email or password'}), 400

    user = Users.query.filter_by(email=email).first()

    if user and user.deletion_requested and user.reactivate_requested:
        if bcrypt.checkpw(password.encode('utf-8'), user.restored_password.encode('utf-8')):
            # Restore user's account and data
            user.deletion_requested = None
            user.reactivate_requested = False
            user.email = user.restored_email
            user.passwd = user.restored_password
            db.session.commit()

            # Generate a JWT with the user's ID as a claim
            token_payload = {'user_id': user.user_id}
            secret_key = 'miano123'
            token = jwt.encode(token_payload, secret_key, algorithm='HS256')

            return jsonify({'message': 'Account reactivated and logged in', 'token': token}), 200


    # Normal login check
    if not user or not bcrypt.checkpw(password.encode('utf-8'), user.passwd.encode('utf-8')):
        return jsonify({'error': 'Invalid email or password'}), 401

    # Generate a JWT with the user's ID as a claim
    token_payload = {'user_id': user.user_id}
    secret_key = 'miano123'
    token = jwt.encode(token_payload, secret_key, algorithm='HS256')

    session['user_token'] = token

    return jsonify({'message': 'Login successful', 'token': token, 'logged_in': True}), 200

@login_bp.route('/logout', methods=['POST'])
def logout():
    # Clear the user token from the session
    session.pop('user_token', None)

    return jsonify({'message': 'Logged out successfully', 'logged_in': False}), 200
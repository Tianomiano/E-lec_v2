from flask import Blueprint, request, jsonify
from models.engine.db_storage import db, Users
from werkzeug.security import generate_password_hash, check_password_hash
import bcrypt

register_bp = Blueprint('register', __name__)

@register_bp.route('/register', methods=['POST'])
def register():
    # receive registration details and handle registration
    
    data = request.get_json()

    username = data.get('username')
    email = data.get('email')
    password = data.get('password')
    confirm_password = data.get('confirm_password')

    if not username or not email or not password or not confirm_password:
        return jsonify({'error': 'Missing required fields'}), 400

    if password != confirm_password:
        return jsonify({'error': 'Passwords do not match'}), 400

    existing_user = Users.query.filter_by(email=email).first()
    if existing_user:
        return jsonify({'error': 'Email already registered'}), 400

    hashed_password = bcrypt.hashpw(password.encode('utf-8'), bcrypt.gensalt())
    new_user = Users(username=username, email=email, passwd=hashed_password)

    db.session.add(new_user)
    db.session.commit()

    return jsonify({'message': 'User registered successfully'}), 201
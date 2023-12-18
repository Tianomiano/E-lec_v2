# decorators.py

from functools import wraps
from flask import jsonify, request
import jwt

def require_token(func):
    @wraps(func)
    def wrapper(*args, **kwargs):
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

        kwargs['user_id'] = user_id
        return func(*args, **kwargs)

    return wrapper

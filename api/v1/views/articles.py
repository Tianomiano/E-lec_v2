from flask import Blueprint, request, jsonify
import jwt
from flask_jwt_extended import jwt_required, get_jwt_identity
from models.engine.db_storage import db, Users, Articles
from datetime import datetime

articles_bp = Blueprint('articles', __name__)

@articles_bp.route('/articles', methods=['GET'])
def get_all_articles():
    # gets a list of all posted articles
    articles = Articles.query.all()
    article_list = []
    for article in articles:
        article_list.append({
            'article_id': article.article_id,
            'title': article.title,
            'author_id': article.author_id,
            'content' : article.content,
            'date_posted': article.date_posted.strftime('%Y-%m-%d %H:%M:%S')
        })
    return jsonify({'articles': article_list})

@articles_bp.route('/articles/<int:article_id>', methods=['GET'])
def get_article_by_id(article_id):
    # displays a specific article based on it's article_id
    article = Articles.query.get(article_id)
    if not article:
        return jsonify({'error': 'Article not found'}), 404
    
    article_data = {
        'article_id': article.article_id,
        'title': article.title,
        'author_id': article.author_id,
        'content': article.content,
        'date_posted': article.date_posted.strftime('%Y-%m-%d %H:%M:%S')
    }
    return jsonify({'article': article_data})

@articles_bp.route('/users/<int:user_id>/articles', methods=['GET'])
def get_user_articles(user_id):
    # displays all articles posted by a specific user
    user = Users.query.get(user_id)
    if not user:
        return jsonify({'error': 'User not found'}), 404
    
    articles = Articles.query.filter_by(author_id=user_id).all()
    article_list = []
    for article in articles:
        article_list.append({
            'article_id': article.article_id,
            'title': article.title,
            'author_id': article.author_id,
            'date_posted': article.date_posted.strftime('%Y-%m-%d %H:%M:%S')
        })
    return jsonify({'articles': article_list})

@articles_bp.route('/articles', methods=['POST'])
def create_article():
    # allows a user to post an article
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
    
    data = request.get_json()
    title = data.get('title')
    content = data.get('content')

    article = Articles(title=title, content=content, author_id=user_id)
    db.session.add(article)
    db.session.commit()

    return jsonify({'message': 'Article created successfully'}), 201

@articles_bp.route('/articles/<int:article_id>', methods=['PUT'])
def update_article(article_id):
    #  use put method to edit an article
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
        
    article = Articles.query.get(article_id)
    if not article:
        return jsonify({'error': 'Article not found'}), 404

    if article.author_id != user_id:
        return jsonify({'error': 'You do not have permission to update this article'}), 403

    data = request.get_json()
    title = data.get('title')
    content = data.get('content')

    article.title = title
    article.content = content
    db.session.commit()

    return jsonify({'message': 'Article updated successfully'}), 200

@articles_bp.route('/articles/<int:article_id>', methods=['DELETE'])
def delete_article(article_id):
    #  uses delete method to delete an article
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

    article = Articles.query.get(article_id)
    if not article:
        return jsonify({'error': 'Article not found'}), 404

    if article.author_id != user_id:
        return jsonify({'error': 'You do not have permission to delete this article'}), 403

    db.session.delete(article)
    db.session.commit()

    return jsonify({'message': 'Article deleted successfully'}), 200

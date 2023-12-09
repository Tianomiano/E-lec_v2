from flask import Blueprint, request, jsonify
from models.engine.db_storage import db, Question, Users, Reply
from datetime import datetime
import jwt

questions_bp = Blueprint('questions', __name__)

@questions_bp.route('/questions', methods=['GET'])
def get_questions():
    # Pull every posted question

    subject = request.args.get('subject')
    search_query = request.args.get('q')
    page = int(request.args.get('page', 1))
    per_page = int(request.args.get('per_page', 10))

    query = Question.query

    if subject:
        query = query.filter_by(subject=subject)
    if search_query:
        query = query.filter(Question.question.ilike(f'%{search_query}%'))

    questions = query.order_by(Question.date_posted.desc()) \
                     .paginate(page=page, per_page=per_page, error_out=False)

    questions_data = []
    for question in questions.items:
        questions_data.append({
            'question_id': question.question_id,
            'subject': question.subject,
            'question': question.question,
            'date_posted': question.date_posted,
            'author_id' : question.author_id,
        })

    return jsonify({
        'questions': questions_data,
        'total_questions': questions.total,
        'current_page': questions.page,
        'per_page': questions.per_page,
    }), 200

@questions_bp.route('/questions/<int:question_id>', methods=['GET'])
def get_question_details(question_id):
    # pull the details of a specific question based on question_id

    question = Question.query.get_or_404(question_id)
    author = Users.query.get(question.author_id)

    replies = Reply.query.filter_by(question_id=question_id).all()
    replies_data = []
    for reply in replies:
        reply_data = {
            'reply_id': reply.reply_id,
            'content': reply.content,
            'date_posted': reply.date_posted,
            'author_id' : reply.author_id,
        }
        replies_data.append(reply_data)

    question_data = {
        'question_id': question.question_id,
        'subject': question.subject,
        'question': question.question,
        'date_posted': question.date_posted,
        'author': author.username,
        'replies': replies_data,
    }

    return jsonify(question_data), 200

@questions_bp.route('/users/<int:user_id>/questions', methods=['GET'])
def get_user_questions(user_id):
    # pull all the questions associated with a specific user id

    user = Users.query.get(user_id)
    if not user:
        return jsonify({'error': 'User not found'}), 404

    questions = Question.query.filter_by(author_id=user_id).all()
    questions_data = []
    for question in questions:
        question_data = {
            'question_id': question.question_id,
            'subject': question.subject,
            'question': question.question,
            'date_posted': question.date_posted,
        }
        questions_data.append(question_data)

    return jsonify({'questions': questions_data}), 200

@questions_bp.route('/users/<int:user_id>/replies', methods=['GET'])
def get_user_replies(user_id):
    # get all replies associated with a specific user id

    user = Users.query.get(user_id)
    if not user:
        return jsonify({'error': 'User not found'}), 404

    replies = Reply.query.filter_by(author_id=user_id).all()
    replies_data = []
    for reply in replies:
        reply_data = {
            'reply_id': reply.reply_id,
            'content': reply.content,
            'date_posted': reply.date_posted,
            'author_id' : reply.author_id,
        }
        replies_data.append(reply_data)

    return jsonify({'replies': replies_data}), 200

@questions_bp.route('/questions', methods=['POST'])
def post_question():
    # allow users to post questions

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

    subject = data.get('subject')
    content = data.get('content')

    if subject not in ['Architecture', 'Arts', 'Biology', 'Chemistry', 'Computer Science', 'Engineering', 'Food and Nutrition', 'Medicine', 'Mathematics', 'Other']:
        return jsonify({'error': 'Invalid subject'}), 400

    new_question = Question(
        subject=subject,
        question=content,
        author_id=user_id,
        date_posted=datetime.utcnow()
    )

    db.session.add(new_question)
    db.session.commit()

    return jsonify({'message': 'Question posted successfully'}), 201

@questions_bp.route('/questions/<int:question_id>', methods=['PUT'])
def update_question(question_id):
    # allow users to edit questions if they are the author

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

    question = Question.query.get(question_id)
    if not question:
        return jsonify({'error': 'Question not found'}), 404

    if question.author_id != user_id:
        return jsonify({'error': 'You do not have permission to update this question'}), 403

    data = request.get_json()
    content = data.get('content')

    question.question = content
    db.session.commit()

    return jsonify({'message': 'Question updated successfully'}), 200

@questions_bp.route('/questions/del/<int:question_id>', methods=['DELETE'])
def delete_question(question_id):
    # allow the question author to delete a specific question

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

    question = Question.query.get(question_id)
    if not question:
        return jsonify({'error': 'Question not found'}), 404

    if question.author_id != user_id:
        return jsonify({'error': 'You do not have permission to delete this question'}), 403

    db.session.delete(question)
    db.session.commit()

    return jsonify({'message': 'Question deleted successfully'}), 200



@questions_bp.route('/questions/<int:question_id>/reply', methods=['POST'])
def post_reply(question_id):
    # allow users to post replies to a specific question

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

    content = data.get('content')

    new_reply = Reply(
        content=content,
        date_posted=datetime.utcnow(),
        author_id=user_id,
        question_id=question_id
    )

    db.session.add(new_reply)
    db.session.commit()

    return jsonify({'message': 'Reply posted successfully'}), 201

@questions_bp.route('/replies/<int:reply_id>', methods=['PUT'])
def update_reply(reply_id):
    # allow reply author to edit their reply

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

    reply = Reply.query.get(reply_id)
    if not reply:
        return jsonify({'error': 'Reply not found'}), 404

    if reply.author_id != user_id:
        return jsonify({'error': 'You do not have permission to update this reply'}), 403

    data = request.get_json()
    content = data.get('content')

    reply.content = content
    db.session.commit()

    return jsonify({'message': 'Reply updated successfully'}), 200

@questions_bp.route('/replies/del/<int:reply_id>', methods=['DELETE'])
def delete_reply(reply_id):
    # allow reply author to delete their reply
    
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

    reply = Reply.query.get(reply_id)
    if not reply:
        return jsonify({'error': 'Reply not found'}), 404

    if reply.author_id != user_id:
        return jsonify({'error': 'You do not have permission to delete this reply'}), 403

    db.session.delete(reply)
    db.session.commit()

    return jsonify({'message': 'Reply deleted successfully'}), 200

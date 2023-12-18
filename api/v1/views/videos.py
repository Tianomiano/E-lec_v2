from flask import Blueprint, jsonify
from models.engine.db_storage import db, Video
from datetime import datetime
import jwt
from flask import request
from .decorators import require_token
import validators
from sqlalchemy.exc import IntegrityError

videos_bp = Blueprint('videos', __name__)


# API endpoint to get all videos
@videos_bp.route('/videos', methods=['GET'])
def get_all_videos():
    # Query the database to get all videos
    videos = Video.query.all()

    # Convert the videos to a list of dictionaries
    videos_list = [{'question_id': video.question_id, 'subject': video.subject, 'videos': video.videos} for video in videos]

    return jsonify({'videos': videos_list})

# Add this function to get the embed code based on the video URL
def get_embed_code(video_url):
    # Extract video ID from the shared link
    if 'loom.com' in video_url:
        video_id_start = video_url.find('/share/') + len('/share/')
        video_id_end = video_url.find('?', video_id_start)
        video_id = video_url[video_id_start:video_id_end]

        # Extract sid parameter from the shared link
        sid_start = video_url.find('?sid=') + len('?sid=')
        sid = video_url[sid_start:]

        # Construct the embed code
        embed_code = f'<iframe width="260" height="215" src="https://www.loom.com/embed/{video_id}?sid={sid}" frameborder="0" webkitallowfullscreen mozallowfullscreen allowfullscreen></iframe>'
    else:
        if "youtu.be" in video_url:
            video_id = video_url.split("/")[-1]
        elif "youtube.com" in video_url:
            video_id = video_url.split("v=")[-1].split("&")[0]
        else:
            # Invalid YouTube URL
            return None

        # Construct YouTube embed code
        embed_code = f'<iframe width="260" height="215" src="https://www.youtube.com/embed/{video_id}" ' \
                    'title="YouTube video player" frameborder="0" ' \
                    'allow="accelerometer; autoplay; clipboard-write; encrypted-media; gyroscope; ' \
                    'picture-in-picture; web-share" allowfullscreen></iframe>'
    return embed_code


@videos_bp.route('/videos/<subject>', methods=['GET'])
def get_videos_by_subject(subject):
    # Query the database to get videos for the specified subject
    videos = Video.query.filter_by(subject=subject).all()

    # Convert the videos to a list of dictionaries
    videos_list = [
        {
            'video_id': video.video_id,
            'subject': video.subject,
            'title': video.title,
            'embed_code': get_embed_code(video.url),
            'date_posted': video.date_posted
        } for video in videos
    ]

    return jsonify({'videos': videos_list})


# API endpoint to post a new video
@videos_bp.route('/videos', methods=['POST'])
@require_token
def post_video(user_id):
    data = request.get_json()

    subject = data.get('subject')
    title = data.get('title')
    video_url = data.get('video_url')

    if not subject or not video_url:
        return jsonify({'error': 'Subject and video_url are required'}), 400
    
    # Check if the provided subject is valid
    valid_subjects = ['Architecture', 'Arts', 'Biology', 'Chemistry', 'Computer Science', 'Engineering', 'Food and Nutrition', 'Medicine', 'Mathematics', 'Other']
    if subject not in valid_subjects:
        return jsonify({'error': 'Invalid subject'}), 400
    
    # Validate if the video_url is a valid URL
    if not validators.url(video_url):
        return jsonify({'error': 'Invalid URL format'}), 400
    
    # Additional safety checks
    allowed_domains = ['youtube.com', 'loom.com']

    if not any(domain in video_url for domain in allowed_domains):
        return jsonify({'error': 'Invalid video source'}), 400

    # Check for duplicate entry before adding the new video
    existing_video = Video.query.filter_by(url=video_url).first()

    if existing_video:
        return jsonify({'error': 'Video with the same URL already exists'}), 400

    try:
        new_video = Video(
            subject=subject,
            title=title,
            url=video_url,
            author_id=user_id,
            date_posted=datetime.utcnow()
        )

        db.session.add(new_video)
        db.session.commit()

        return jsonify({'message': 'Video posted successfully'}), 201

    except IntegrityError:
        db.session.rollback()
        return jsonify({'error': 'An error occurred while posting the video'}), 500

@videos_bp.route('/videos/del/<int:video_id>', methods=['DELETE'])
@require_token
def delete_video(user_id, video_id):
    # Check if the video with the given ID exists and belongs to the requesting user
    video = Video.query.filter_by(question_id=video_id, author_id=user_id).first()

    if not video:
        return jsonify({'error': 'Video not found or unauthorized to delete'}), 404

    # Delete the video
    db.session.delete(video)
    db.session.commit()

    return jsonify({'message': 'Video deleted successfully'}), 200

@videos_bp.route('/videos/user/<int:user_id>', methods=['GET'])
@require_token
def get_videos_by_user(user_id):
    videos = Video.query.filter_by(author_id=user_id).all()
    videos_list = [{'video_id': video.video_id, 'subject': video.subject, 'url': video.url, 'date_posted': video.date_posted} for video in videos]
    return jsonify({'videos': videos_list})


@videos_bp.route('/videos/<int:video_id>', methods=['PUT'])
@require_token
def update_video_url(user_id, video_id):
    video = Video.query.filter_by(video_id=video_id, author_id=user_id).first()

    if not video:
        return jsonify({'error': 'Video not found or unauthorized to update'}), 404

    data = request.get_json()
    new_url = data.get('new_url')
    new_title = data.get('new_title')

    if not new_url:
        return jsonify({'error': 'New video_url is required'}), 400

    video.url = new_url
    if new_title:
        video.title = new_title

    db.session.commit()

    return jsonify({'message': 'Video URL updated successfully'}), 200

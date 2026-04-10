from datetime import datetime
from flask import Blueprint, request, jsonify, session as flask_session
from app import db
from app.models.reading_session import ReadingSession
from app.models.book import Book

sessions_bp = Blueprint('sessions', __name__)


def current_user_id():
    return flask_session.get('user_id')


@sessions_bp.route('/', methods=['GET'])
def get_sessions():
    uid = current_user_id()
    if not uid:
        return jsonify({'error': 'Not authenticated'}), 401
    sessions = (ReadingSession.query
                .filter_by(user_id=uid)
                .order_by(ReadingSession.session_date.desc(), ReadingSession.created_at.desc())
                .all())
    return jsonify({'sessions': [s.to_dict() for s in sessions]}), 200


@sessions_bp.route('/', methods=['POST'])
def log_session():
    uid = current_user_id()
    if not uid:
        return jsonify({'error': 'Not authenticated'}), 401

    data = request.get_json()
    for field in ('book_id', 'duration_minutes', 'session_date'):
        if not data.get(field):
            return jsonify({'error': f'{field} is required'}), 400

    book = Book.query.filter_by(id=data['book_id'], user_id=uid).first()
    if not book:
        return jsonify({'error': 'Book not found'}), 404

    reading_session = ReadingSession(
        user_id=uid,
        book_id=data['book_id'],
        session_date=datetime.strptime(data['session_date'], '%Y-%m-%d').date(),
        start_time=datetime.strptime(data['start_time'], '%H:%M').time() if data.get('start_time') else None,
        end_time=datetime.strptime(data['end_time'],   '%H:%M').time() if data.get('end_time')   else None,
        duration_minutes=int(data['duration_minutes']),
        pages_read=data.get('pages_read', 0),
        mood=data.get('mood', 'focused'),
        notes=data.get('notes'),
    )

    if book.status == 'to_read':
        book.status = 'reading'

    db.session.add(reading_session)
    db.session.commit()
    return jsonify({'message': 'Session logged', 'session': reading_session.to_dict()}), 201


@sessions_bp.route('/<int:session_id>', methods=['DELETE'])
def delete_session(session_id):
    uid = current_user_id()
    if not uid:
        return jsonify({'error': 'Not authenticated'}), 401
    s = ReadingSession.query.filter_by(id=session_id, user_id=uid).first_or_404()
    db.session.delete(s)
    db.session.commit()
    return jsonify({'message': 'Session deleted'}), 200

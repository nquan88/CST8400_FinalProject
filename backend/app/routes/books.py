from flask import Blueprint, request, jsonify, session
from app import db
from app.models.book import Book

books_bp = Blueprint('books', __name__)


def current_user_id():
    return session.get('user_id')


@books_bp.route('/', methods=['GET'])
def get_books():
    uid = current_user_id()
    if not uid:
        return jsonify({'error': 'Not authenticated'}), 401
    books = Book.query.filter_by(user_id=uid).order_by(Book.created_at.desc()).all()
    return jsonify({'books': [b.to_dict() for b in books]}), 200


@books_bp.route('/', methods=['POST'])
def add_book():
    uid = current_user_id()
    if not uid:
        return jsonify({'error': 'Not authenticated'}), 401
    data = request.get_json()
    if not data or not data.get('title'):
        return jsonify({'error': 'Title is required'}), 400

    book = Book(
        user_id=uid,
        title=data['title'],
        author=data.get('author'),
        genre=data.get('genre'),
        difficulty_level=data.get('difficulty_level', 'medium'),
        total_pages=data.get('total_pages'),
        status=data.get('status', 'to_read'),
    )
    db.session.add(book)
    db.session.commit()
    return jsonify({'message': 'Book added', 'book': book.to_dict()}), 201


@books_bp.route('/<int:book_id>', methods=['PUT'])
def update_book(book_id):
    uid = current_user_id()
    if not uid:
        return jsonify({'error': 'Not authenticated'}), 401
    book = Book.query.filter_by(id=book_id, user_id=uid).first_or_404()
    data = request.get_json()
    for field in ('title', 'author', 'genre', 'difficulty_level', 'total_pages', 'status'):
        if field in data:
            setattr(book, field, data[field])
    db.session.commit()
    return jsonify({'message': 'Book updated', 'book': book.to_dict()}), 200


@books_bp.route('/<int:book_id>', methods=['DELETE'])
def delete_book(book_id):
    uid = current_user_id()
    if not uid:
        return jsonify({'error': 'Not authenticated'}), 401
    book = Book.query.filter_by(id=book_id, user_id=uid).first_or_404()
    db.session.delete(book)
    db.session.commit()
    return jsonify({'message': 'Book deleted'}), 200

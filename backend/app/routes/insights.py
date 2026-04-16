from flask import Blueprint, jsonify, session
from app.services.analytics import compute_analytics
from app.services.insights_engine import generate_insights

insights_bp = Blueprint('insights', __name__)


def current_user_id():
    return session.get('user_id')


@insights_bp.route('/', methods=['GET'])
def get_insights():
    uid = current_user_id()
    if not uid:
        return jsonify({'error': 'Not authenticated'}), 401

    return jsonify({
        'insights': generate_insights(uid)
    }), 200


@insights_bp.route('/analytics', methods=['GET'])
def get_analytics():
    uid = current_user_id()
    if not uid:
        return jsonify({'error': 'Not authenticated'}), 401

    return jsonify({
        'analytics': compute_analytics(uid)
    }), 200
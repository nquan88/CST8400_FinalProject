from flask import Blueprint, render_template, redirect, url_for, session
<<<<<<< HEAD
=======
from app.services.analytics import compute_analytics
from app import db 
from app.models.goal import Goal
from flask import request, redirect, url_for, session
>>>>>>> 47582d5b5ef8a842817fcb1679ea1afc4b5818a0

views_bp = Blueprint('views', __name__)


def logged_in():
    return 'user_id' in session


@views_bp.route('/')
def dashboard():
    if not logged_in():
        return redirect(url_for('views.login'))
<<<<<<< HEAD
    return render_template('dashboard.html')

=======

    user_id = session['user_id']
    data = compute_analytics(user_id)
    print("DATA:", data)

    goal = Goal.query.filter_by(user_id=user_id).first()
    goal_minutes = goal.daily_minutes if goal else 30

    return render_template('dashboard.html', data=data, goal_minutes=goal_minutes)
>>>>>>> 47582d5b5ef8a842817fcb1679ea1afc4b5818a0

@views_bp.route('/login')
def login():
    if logged_in():
        return redirect(url_for('views.dashboard'))
    return render_template('login.html')


@views_bp.route('/register')
def register():
    if logged_in():
        return redirect(url_for('views.dashboard'))
    return render_template('register.html')


<<<<<<< HEAD
=======


@views_bp.route('/set-goal', methods=['POST'])
def set_goal():
    user_id = session['user_id']
    minutes = int(request.form['minutes'])

    goal = Goal.query.filter_by(user_id=user_id).first()

    if goal:
        goal.daily_minutes = minutes
    else:
        goal = Goal(user_id=user_id, daily_minutes=minutes)
        db.session.add(goal)

    db.session.commit()
    return redirect(url_for('views.dashboard'))

>>>>>>> 47582d5b5ef8a842817fcb1679ea1afc4b5818a0
@views_bp.route('/books')
def books():
    if not logged_in():
        return redirect(url_for('views.login'))
    return render_template('books.html')


@views_bp.route('/log-session')
def log_session():
    if not logged_in():
        return redirect(url_for('views.login'))
    return render_template('log_session.html')


@views_bp.route('/insights')
def insights():
    if not logged_in():
        return redirect(url_for('views.login'))
    return render_template('insights.html')

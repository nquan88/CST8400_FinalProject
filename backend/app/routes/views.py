from flask import Blueprint, render_template, redirect, url_for, session

views_bp = Blueprint('views', __name__)


def logged_in():
    return 'user_id' in session


@views_bp.route('/')
def dashboard():
    if not logged_in():
        return redirect(url_for('views.login'))
    return render_template('dashboard.html')


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

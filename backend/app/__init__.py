from flask import Flask
from flask_sqlalchemy import SQLAlchemy

db = SQLAlchemy()


def create_app():
    app = Flask(__name__)
    app.config.from_object('app.config.Config')

    db.init_app(app)

    from app.routes.auth import auth_bp
    from app.routes.books import books_bp
    from app.routes.sessions import sessions_bp
    from app.routes.insights import insights_bp
    from app.routes.views import views_bp

    app.register_blueprint(auth_bp,     url_prefix='/api/auth')
    app.register_blueprint(books_bp,    url_prefix='/api/books')
    app.register_blueprint(sessions_bp, url_prefix='/api/sessions')
    app.register_blueprint(insights_bp, url_prefix='/api/insights')
    app.register_blueprint(views_bp)

    @app.cli.command('init-db')
    def init_db():
        db.create_all()
        print('Database tables created.')

    return app

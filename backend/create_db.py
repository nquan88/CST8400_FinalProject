from app import create_app, db
from app.models.user import User
from app.models.book import Book
from app.models.reading_session import ReadingSession
from app.models.goal import Goal

app = create_app()

with app.app_context():
    db.create_all()
    print("DB created")
from app import db


class Book(db.Model):
    __tablename__ = 'books'

    id               = db.Column(db.Integer, primary_key=True)
    user_id          = db.Column(db.Integer, db.ForeignKey('users.id'), nullable=False)
    title            = db.Column(db.String(200), nullable=False)
    author           = db.Column(db.String(150))
    genre            = db.Column(db.String(100))
    difficulty_level = db.Column(db.Enum('easy', 'medium', 'hard'), default='medium')
    total_pages      = db.Column(db.Integer)
    status           = db.Column(db.Enum('to_read', 'reading', 'completed', 'abandoned'), default='to_read')
    created_at       = db.Column(db.DateTime, server_default=db.func.now())

    sessions = db.relationship('ReadingSession', backref='book', lazy=True, cascade='all, delete-orphan')

    def to_dict(self):
        return {
            'id':               self.id,
            'user_id':          self.user_id,
            'title':            self.title,
            'author':           self.author,
            'genre':            self.genre,
            'difficulty_level': self.difficulty_level,
            'total_pages':      self.total_pages,
            'status':           self.status,
            'created_at':       self.created_at.isoformat() if self.created_at else None,
        }

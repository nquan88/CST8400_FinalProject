from app import db


class ReadingSession(db.Model):
    __tablename__ = 'reading_sessions'

    id               = db.Column(db.Integer, primary_key=True)
    user_id          = db.Column(db.Integer, db.ForeignKey('users.id'), nullable=False)
    book_id          = db.Column(db.Integer, db.ForeignKey('books.id'), nullable=False)
    session_date     = db.Column(db.Date,    nullable=False)
    start_time       = db.Column(db.Time)
    end_time         = db.Column(db.Time)
    duration_minutes = db.Column(db.Integer, nullable=False)
    pages_read       = db.Column(db.Integer, default=0)
    mood             = db.Column(db.Enum('focused', 'distracted', 'tired', 'energized'), default='focused')
    notes            = db.Column(db.Text)
    created_at       = db.Column(db.DateTime, server_default=db.func.now())

    def to_dict(self):
        return {
            'id':               self.id,
            'user_id':          self.user_id,
            'book_id':          self.book_id,
            'book_title':       self.book.title if self.book else None,
            'session_date':     self.session_date.isoformat() if self.session_date else None,
            'start_time':       self.start_time.strftime('%H:%M') if self.start_time else None,
            'end_time':         self.end_time.strftime('%H:%M')   if self.end_time   else None,
            'duration_minutes': self.duration_minutes,
            'pages_read':       self.pages_read,
            'mood':             self.mood,
            'notes':            self.notes,
            'created_at':       self.created_at.isoformat() if self.created_at else None,
        }

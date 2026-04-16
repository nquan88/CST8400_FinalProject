from app import create_app, db
<<<<<<< HEAD
=======
from app.models.goal import Goal
>>>>>>> 47582d5b5ef8a842817fcb1679ea1afc4b5818a0

app = create_app()
with app.app_context():
    db.create_all()
    print('DB created')

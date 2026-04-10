# Smart Reading Habit Tracker
CST8400 Final Project — AI & Data Analytics

**Team:** Le Vy Pham · Minh Quan Ngo · Adama Adamou Allagouma

---

## Setup

### 1. Database

```bash
mysql -u root -p < database/schema.sql
```

### 2. Backend

```bash
cd backend
python -m venv venv
# Windows:
venv\Scripts\activate
# macOS/Linux:
source venv/bin/activate

pip install -r requirements.txt
```

Copy `.env.example` to `.env` and fill in your MySQL credentials:

```
SECRET_KEY=any-random-string
DATABASE_URL=mysql+pymysql://root:YOUR_PASSWORD@localhost/reading_tracker
```

### 3. Run

```bash
python run.py
```

Open **http://localhost:5000** — register an account and start tracking.

---

## Project Structure

```
CST8400_FinalProject/
├── database/
│   └── schema.sql              # MySQL schema (users, books, reading_sessions)
├── backend/
│   ├── run.py                  # Entry point
│   ├── requirements.txt
│   ├── .env.example
│   └── app/
│       ├── __init__.py         # Flask app factory
│       ├── config.py
│       ├── models/             # SQLAlchemy models
│       │   ├── user.py
│       │   ├── book.py
│       │   └── reading_session.py
│       ├── routes/             # Blueprints
│       │   ├── auth.py         # /api/auth/*
│       │   ├── books.py        # /api/books/*
│       │   ├── sessions.py     # /api/sessions/*
│       │   ├── insights.py     # /api/insights/*
│       │   └── views.py        # Page routes
│       ├── services/
│       │   ├── analytics.py    # Pandas-based analytics
│       │   └── insights_engine.py  # Rule-based AI insights
│       ├── static/
│       │   ├── css/style.css
│       │   └── js/             # dashboard, books, log-session, insights
│       └── templates/          # Jinja2 HTML pages
└── README.md
```

## API Endpoints

| Method | Endpoint | Description |
|--------|----------|-------------|
| POST | `/api/auth/register` | Register a new user |
| POST | `/api/auth/login` | Login |
| POST | `/api/auth/logout` | Logout |
| GET  | `/api/books/` | List books |
| POST | `/api/books/` | Add book |
| PUT  | `/api/books/<id>` | Update book |
| DELETE | `/api/books/<id>` | Delete book |
| GET  | `/api/sessions/` | List sessions |
| POST | `/api/sessions/` | Log session |
| DELETE | `/api/sessions/<id>` | Delete session |
| GET  | `/api/insights/` | Get AI insights |
| GET  | `/api/insights/analytics` | Get analytics data |

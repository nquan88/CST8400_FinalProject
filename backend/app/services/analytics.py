from collections import Counter
import pandas as pd
from app.models.reading_session import ReadingSession
from app.models.book import Book


def time_of_day(hour):
    if 5 <= hour < 12:
        return 'Morning'
    elif 12 <= hour < 17:
        return 'Afternoon'
    elif 17 <= hour < 21:
        return 'Evening'
    return 'Night'


def compute_analytics(user_id):
    sessions = ReadingSession.query.filter_by(user_id=user_id).all()

    empty = {
        'total_sessions': 0, 'total_minutes': 0, 'total_pages': 0,
        'avg_duration_minutes': 0, 'preferred_reading_time': 'N/A',
        'reading_frequency_per_week': 0, 'consistency_score': 0,
        'mood_distribution': {}, 'genre_distribution': {},
        'sessions_by_day_of_week': {d: 0 for d in
            ['Monday','Tuesday','Wednesday','Thursday','Friday','Saturday','Sunday']},
        'sessions_last_30_days': [], 'reading_streak': 0,
    }

    if not sessions:
        return empty

    rows = [{
        'id':               s.id,
        'session_date':     s.session_date,
        'duration_minutes': s.duration_minutes,
        'pages_read':       s.pages_read or 0,
        'mood':             s.mood,
        'start_time':       s.start_time,
        'book_id':          s.book_id,
    } for s in sessions]

    df = pd.DataFrame(rows)
    df['session_date'] = pd.to_datetime(df['session_date'])

    total_sessions = len(df)
    total_minutes  = int(df['duration_minutes'].sum())
    total_pages    = int(df['pages_read'].sum())
    avg_duration   = round(float(df['duration_minutes'].mean()), 1)

    # Preferred reading time of day
    tod_counter = Counter()
    for s in sessions:
        if s.start_time:
            tod_counter[time_of_day(s.start_time.hour)] += 1
    preferred_time = tod_counter.most_common(1)[0][0] if tod_counter else 'N/A'

    # Sessions per week
    date_range_days = (df['session_date'].max() - df['session_date'].min()).days + 1
    weeks = max(date_range_days / 7, 1)
    freq_per_week = round(total_sessions / weeks, 1)

    # Consistency score: % of last 30 days with at least one session
    today   = pd.Timestamp.today().normalize()
    day_30  = today - pd.Timedelta(days=29)
    recent  = df[df['session_date'] >= day_30]
    active_days      = recent['session_date'].dt.normalize().nunique()
    consistency_score = round((active_days / 30) * 100, 1)

    # Mood distribution
    mood_dist = df['mood'].value_counts().to_dict()

    # Genre distribution
    books = {b.id: b for b in Book.query.filter_by(user_id=user_id).all()}
    genre_counter = Counter()
    for s in sessions:
        b = books.get(s.book_id)
        if b and b.genre:
            genre_counter[b.genre] += 1
    genre_dist = dict(genre_counter)

    # Sessions by day of week
    days_order = ['Monday','Tuesday','Wednesday','Thursday','Friday','Saturday','Sunday']
    df['dow'] = df['session_date'].dt.day_name()
    sessions_by_dow = {d: 0 for d in days_order}
    sessions_by_dow.update(df['dow'].value_counts().to_dict())

    # Daily totals for last 30 days (line chart data)
    recent_grp = (recent
                  .groupby(recent['session_date'].dt.strftime('%Y-%m-%d'))['duration_minutes']
                  .sum()
                  .reset_index())
    recent_grp.columns = ['date', 'duration_minutes']
    sessions_last_30 = recent_grp.to_dict('records')

    # Reading streak (consecutive days up to today)
    all_dates = sorted(df['session_date'].dt.normalize().unique(), reverse=True)
    streak = 0
    cursor = today
    for d in all_dates:
        if d == cursor or d == cursor - pd.Timedelta(days=1):
            streak += 1
            cursor = d
        else:
            break

    return {
        'total_sessions':            total_sessions,
        'total_minutes':             total_minutes,
        'total_pages':               total_pages,
        'avg_duration_minutes':      avg_duration,
        'preferred_reading_time':    preferred_time,
        'reading_frequency_per_week': freq_per_week,
        'consistency_score':         consistency_score,
        'mood_distribution':         mood_dist,
        'genre_distribution':        genre_dist,
        'sessions_by_day_of_week':   sessions_by_dow,
        'sessions_last_30_days':     sessions_last_30,
        'reading_streak':            streak,
    }

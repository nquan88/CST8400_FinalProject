from app.services.analytics import compute_analytics
from app.services.llm_client import generate_insights_via_hf


def generate_insights(user_id):
    a = compute_analytics(user_id)

<<<<<<< HEAD
    # Optional Hugging Face / LLM-generated insights
    try:
        llm_out = generate_insights_via_hf(a)
        if isinstance(llm_out, list) and all(isinstance(i, dict) for i in llm_out):
            for item in llm_out:
=======
    # Try LLM-generated insights (Hugging Face). If the API key isn't set
    # or the LLM call fails, fall back to the built-in rule-based insights.
    try:
        llm_out = generate_insights_via_hf(a)
        # validate structure: list of dicts with required keys
        if isinstance(llm_out, list) and all(isinstance(i, dict) for i in llm_out):
            for item in llm_out:
                # ensure required keys exist and provide safe defaults
>>>>>>> 47582d5b5ef8a842817fcb1679ea1afc4b5818a0
                item.setdefault('type', 'info')
                item.setdefault('icon', 'lightbulb')
                item.setdefault('title', '')
                item.setdefault('message', '')
            return llm_out
    except Exception:
<<<<<<< HEAD
=======
        # silently fall back to rule-based insights
>>>>>>> 47582d5b5ef8a842817fcb1679ea1afc4b5818a0
        pass

    if a['total_sessions'] == 0:
        return [{
<<<<<<< HEAD
            'type': 'welcome',
            'title': 'Welcome to your Reading Tracker!',
            'message': 'Log your first reading session to start receiving personalized insights.',
            'icon': 'book',
=======
            'type':    'welcome',
            'title':   'Welcome to your Reading Tracker!',
            'message': 'Log your first reading session to start receiving personalized insights.',
            'icon':    'book',
>>>>>>> 47582d5b5ef8a842817fcb1679ea1afc4b5818a0
        }]

    insights = []

<<<<<<< HEAD
    # Preferred reading time
    pref = a['preferred_reading_time']
    if pref != 'N/A':
        time_messages = {
            'Morning': 'You read most often in the morning. This appears to be your most natural and productive reading window.',
            'Afternoon': 'You tend to read most in the afternoon. That seems to be your preferred reading period.',
            'Evening': 'You usually read in the evening. This may be the best time for your routine and focus.',
            'Night': 'Most of your reading happens at night. You appear to prefer late-day reading sessions.',
        }
        insights.append({
            'type': 'info',
            'icon': 'clock',
            'title': 'Preferred Reading Time',
            'message': time_messages.get(pref, f'Your preferred reading time is {pref}.'),
        })

    # Reading consistency
    score = a['consistency_score']
    if score >= 70:
        consistency_message = f'You read on {score}% of the last 30 days. Your reading habit is very consistent.'
        consistency_type = 'success'
    elif score >= 40:
        consistency_message = f'You read on {score}% of the last 30 days. Your reading habit is developing steadily.'
        consistency_type = 'info'
    else:
        consistency_message = f'You read on only {score}% of the last 30 days. Try shorter daily sessions to improve consistency.'
        consistency_type = 'warning'

    insights.append({
        'type': consistency_type,
        'icon': 'calendar-check',
        'title': 'Reading Consistency',
        'message': consistency_message,
    })

    # Session duration patterns
    patterns = a['session_duration_patterns']
    short_count = patterns.get('Short', 0)
    medium_count = patterns.get('Medium', 0)
    long_count = patterns.get('Long', 0)

    if long_count >= medium_count and long_count >= short_count:
        pattern_message = 'Most of your sessions are long. You seem comfortable with deep, extended reading sessions.'
    elif medium_count >= short_count and medium_count >= long_count:
        pattern_message = 'Most of your sessions are medium-length. This suggests a balanced and sustainable reading habit.'
    else:
        pattern_message = 'Most of your sessions are short. Short sessions can still be effective, especially when done consistently.'

    insights.append({
        'type': 'info',
        'icon': 'chart-bar',
        'title': 'Session Duration Patterns',
        'message': pattern_message,
    })

    # Average duration bonus insight
    avg = a['avg_duration_minutes']
    insights.append({
        'type': 'tip',
        'icon': 'hourglass-half',
        'title': 'Average Session Length',
        'message': f'Your average reading session is {avg} minutes.',
    })

    # Reading streak bonus insight
    streak = a['reading_streak']
    if streak >= 3:
        insights.append({
            'type': 'success',
            'icon': 'fire',
            'title': 'Reading Streak',
            'message': f'You are currently on a {streak}-day reading streak.',
        })

    return insights
=======
    # ── Consistency ──────────────────────────────────────────────────────────
    score = a['consistency_score']
    if score >= 70:
        insights.append({
            'type': 'success', 'icon': 'fire',
            'title': 'Great Consistency!',
            'message': f'You read on {score}% of days this month. Keep up the momentum!',
        })
    elif score >= 40:
        insights.append({
            'type': 'info', 'icon': 'chart-line',
            'title': 'Building Your Habit',
            'message': f'You read on {score}% of days this month. Aim for daily sessions to strengthen the habit.',
        })
    else:
        insights.append({
            'type': 'warning', 'icon': 'exclamation-triangle',
            'title': 'Consistency Needs Work',
            'message': f'You only read on {score}% of days this month. Even 10 minutes a day makes a big difference!',
        })

    # ── Average session duration ──────────────────────────────────────────────
    avg = a['avg_duration_minutes']
    if avg >= 60:
        insights.append({
            'type': 'success', 'icon': 'bullseye',
            'title': 'Deep Focus Sessions',
            'message': f'Your average session is {avg} minutes — excellent sustained concentration!',
        })
    elif avg >= 20:
        insights.append({
            'type': 'info', 'icon': 'clock',
            'title': 'Steady Sessions',
            'message': f'Your average session is {avg} min. Research suggests 30–45 min is optimal for retention.',
        })
    else:
        insights.append({
            'type': 'tip', 'icon': 'lightbulb',
            'title': 'Short Sessions',
            'message': f'Your average session is only {avg} min. Try extending to 20+ minutes to reach a reading flow.',
        })

    # ── Preferred reading time ────────────────────────────────────────────────
    pref = a['preferred_reading_time']
    if pref != 'N/A':
        time_tips = {
            'Morning':   'Morning reading is ideal — your brain is fresh and retention is high.',
            'Afternoon': 'Afternoon reading works well. Watch out for the post-lunch energy dip (2–3 PM).',
            'Evening':   'Evening reading is great for winding down. Try to keep a consistent start time.',
            'Night':     'Late-night reading can be cozy, but fatigue may reduce retention. Consider shifting earlier.',
        }
        icon_map = {'Morning': 'sun', 'Afternoon': 'cloud-sun', 'Evening': 'moon', 'Night': 'star'}
        insights.append({
            'type': 'info', 'icon': icon_map.get(pref, 'clock'),
            'title': f'You Are a {pref} Reader',
            'message': time_tips.get(pref, ''),
        })

    # ── Streak ────────────────────────────────────────────────────────────────
    streak = a['reading_streak']
    if streak >= 7:
        insights.append({
            'type': 'success', 'icon': 'trophy',
            'title': f'{streak}-Day Streak!',
            'message': 'Incredible dedication — you have been reading every day this week!',
        })
    elif streak >= 3:
        insights.append({
            'type': 'info', 'icon': 'bolt',
            'title': f'{streak}-Day Streak',
            'message': 'You are on a streak! Read today to keep it going.',
        })

    # ── Mood ──────────────────────────────────────────────────────────────────
    mood_dist = a['mood_distribution']
    if mood_dist:
        top_mood = max(mood_dist, key=mood_dist.get)
        mood_advice = {
            'focused':    None,
            'energized':  None,
            'distracted': 'You often feel distracted while reading. Try a quieter space or shorter, focused sprints.',
            'tired':      'You often read when tired. Shifting your sessions to a higher-energy time of day could improve focus.',
        }
        advice = mood_advice.get(top_mood)
        if advice:
            insights.append({
                'type': 'tip', 'icon': 'lightbulb',
                'title': 'Reading Environment Tip',
                'message': advice,
            })

    # ── Genre variety ─────────────────────────────────────────────────────────
    genre_count = len(a['genre_distribution'])
    if genre_count >= 3:
        insights.append({
            'type': 'info', 'icon': 'layer-group',
            'title': 'Diverse Reader',
            'message': f'You read across {genre_count} genres — variety builds broader knowledge and keeps reading fresh!',
        })
    elif genre_count == 1:
        genre = list(a['genre_distribution'].keys())[0]
        insights.append({
            'type': 'tip', 'icon': 'compass',
            'title': 'Explore More Genres',
            'message': f'You mainly read {genre}. Branching into other genres can spark new interests.',
        })

    # ── Frequency ─────────────────────────────────────────────────────────────
    freq = a['reading_frequency_per_week']
    if freq < 3:
        insights.append({
            'type': 'tip', 'icon': 'calendar-alt',
            'title': 'Read More Frequently',
            'message': f'You average {freq} sessions/week. Aim for 4–5 to build a strong reading habit.',
        })

    return insights
>>>>>>> 47582d5b5ef8a842817fcb1679ea1afc4b5818a0

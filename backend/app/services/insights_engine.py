from app.services.analytics import compute_analytics
from app.services.llm_client import generate_insights_via_gemini


def generate_insights(user_id):
    a = compute_analytics(user_id)

    try:
        llm_out = generate_insights_via_gemini(a)
        if isinstance(llm_out, list) and all(isinstance(i, dict) for i in llm_out):
            for item in llm_out:
                item.setdefault('type', 'info')
                item.setdefault('icon', 'lightbulb')
                item.setdefault('title', '')
                item.setdefault('message', '')
            return llm_out
    except Exception:
        pass

    if a['total_sessions'] == 0:
        return [{
            'type':    'welcome',
            'title':   'Welcome to your Reading Tracker!',
            'message': 'Log your first reading session to start receiving personalized insights.',
            'icon':    'book',
        }]

    insights = []

    score = a['consistency_score']
    if score >= 70:
        insights.append({'type': 'success', 'icon': 'fire', 'title': 'Great Consistency!',
            'message': f'You read on {score}% of days this month. Keep up the momentum!'})
    elif score >= 40:
        insights.append({'type': 'info', 'icon': 'chart-line', 'title': 'Building Your Habit',
            'message': f'You read on {score}% of days this month. Aim for daily sessions to strengthen the habit.'})
    else:
        insights.append({'type': 'warning', 'icon': 'exclamation-triangle', 'title': 'Consistency Needs Work',
            'message': f'You only read on {score}% of days this month. Even 10 minutes a day makes a big difference!'})

    avg = a['avg_duration_minutes']
    if avg >= 60:
        insights.append({'type': 'success', 'icon': 'bullseye', 'title': 'Deep Focus Sessions',
            'message': f'Your average session is {avg} minutes — excellent sustained concentration!'})
    elif avg >= 20:
        insights.append({'type': 'info', 'icon': 'clock', 'title': 'Steady Sessions',
            'message': f'Your average session is {avg} min. Research suggests 30–45 min is optimal for retention.'})
    else:
        insights.append({'type': 'tip', 'icon': 'lightbulb', 'title': 'Short Sessions',
            'message': f'Your average session is only {avg} min. Try extending to 20+ minutes to reach a reading flow.'})

    pref = a['preferred_reading_time']
    if pref != 'N/A':
        time_tips = {
            'Morning':   'Morning reading is ideal — your brain is fresh and retention is high.',
            'Afternoon': 'Afternoon reading works well. Watch out for the post-lunch energy dip (2–3 PM).',
            'Evening':   'Evening reading is great for winding down. Try to keep a consistent start time.',
            'Night':     'Late-night reading can be cozy, but fatigue may reduce retention. Consider shifting earlier.',
        }
        icon_map = {'Morning': 'sun', 'Afternoon': 'cloud-sun', 'Evening': 'moon', 'Night': 'star'}
        insights.append({'type': 'info', 'icon': icon_map.get(pref, 'clock'),
            'title': f'You Are a {pref} Reader', 'message': time_tips.get(pref, '')})

    streak = a['reading_streak']
    if streak >= 7:
        insights.append({'type': 'success', 'icon': 'trophy', 'title': f'{streak}-Day Streak!',
            'message': 'Incredible dedication — you have been reading every day this week!'})
    elif streak >= 3:
        insights.append({'type': 'info', 'icon': 'bolt', 'title': f'{streak}-Day Streak',
            'message': 'You are on a streak! Read today to keep it going.'})

    freq = a['reading_frequency_per_week']
    if freq < 3:
        insights.append({'type': 'tip', 'icon': 'calendar-alt', 'title': 'Read More Frequently',
            'message': f'You average {freq} sessions/week. Aim for 4–5 to build a strong reading habit.'})

    return insights

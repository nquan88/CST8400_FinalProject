from app.services.analytics import compute_analytics
from app.services.llm_client import generate_insights_via_hf


def generate_insights(user_id):
    a = compute_analytics(user_id)

    # Optional Hugging Face / LLM-generated insights
    try:
        llm_out = generate_insights_via_hf(a)
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
            'type': 'welcome',
            'title': 'Welcome to your Reading Tracker!',
            'message': 'Log your first reading session to start receiving personalized insights.',
            'icon': 'book',
        }]

    insights = []

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
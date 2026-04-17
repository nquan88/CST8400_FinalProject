function escHtml(str) {
  const d = document.createElement('div');
  d.textContent = str ?? '';
  return d.innerHTML;
}

async function askAI() {
  const btn = document.getElementById('ask-ai-btn');
  const resultSection = document.getElementById('ai-result');
  const container = document.getElementById('insights-container');

  btn.disabled = true;
  btn.textContent = '⏳ Asking Gemini…';

  resultSection.style.display = 'block';
  container.innerHTML = '<div class="ai-loading"><div class="spinner"></div><p>Gemini is analysing your reading data…</p></div>';

  try {
    const result = await api.get('/api/insights/');
    if (!result) throw new Error('No response');

    const insights = result.insights || [];

    if (!insights.length) {
      container.innerHTML = `
        <div class="empty-state">
          <div class="empty-icon">🔍</div>
          <p>No insights yet. Log some reading sessions first!</p>
        </div>`;
    } else {
      container.innerHTML = `
        <div class="insights-grid">
          ${insights.map(i => `
            <div class="insight-card ${escHtml(i.type)}">
              <div class="insight-icon">${insightIcon(i.icon)}</div>
              <div class="insight-body">
                <h4>${escHtml(i.title)}</h4>
                <p>${escHtml(i.message)}</p>
              </div>
            </div>`).join('')}
        </div>`;
    }

    btn.textContent = '🔄 Regenerate Insights';
  } catch (err) {
    container.innerHTML = `
      <div class="empty-state">
        <div class="empty-icon">⚠️</div>
        <p>Failed to get AI insights. Check your API key and try again.</p>
      </div>`;
    btn.textContent = '✨ Generate AI Insights';
  } finally {
    btn.disabled = false;
  }
}

async function loadAnalytics() {
  const container = document.getElementById('analytics-container');

  try {
    const result = await api.get('/api/insights/analytics');
    if (!result || !result.analytics) throw new Error('No data');

    const a = result.analytics;
    container.innerHTML = `
      <div class="insights-grid">
        <div class="insight-card info"><div class="insight-body"><h4>Total Sessions</h4><p>${a.total_sessions ?? 0}</p></div></div>
        <div class="insight-card info"><div class="insight-body"><h4>Preferred Reading Time</h4><p>${escHtml(a.preferred_reading_time ?? 'N/A')}</p></div></div>
        <div class="insight-card info"><div class="insight-body"><h4>Consistency Score</h4><p>${a.consistency_score ?? 0}%</p></div></div>
        <div class="insight-card info"><div class="insight-body"><h4>Avg Session Duration</h4><p>${a.avg_duration_minutes ?? 0} minutes</p></div></div>
        <div class="insight-card info"><div class="insight-body"><h4>Reading Streak</h4><p>${a.reading_streak ?? 0} day(s)</p></div></div>
        <div class="insight-card info"><div class="insight-body"><h4>Sessions / Week</h4><p>${a.reading_frequency_per_week ?? 0}</p></div></div>
      </div>`;
  } catch (e) {
    container.innerHTML = `<div class="empty-state"><div class="empty-icon">⚠️</div><p>Could not load analytics.</p></div>`;
  }
}

document.addEventListener('DOMContentLoaded', loadAnalytics);

async function loadInsights() {
  const container = document.getElementById('insights-container');
  container.innerHTML = '<div class="spinner"></div>';

  const result = await api.get('/api/insights/');
  if (!result) return;

  const insights = result.insights || [];

  if (!insights.length) {
    container.innerHTML = `
      <div class="empty-state">
        <div class="empty-icon">🔍</div>
        <p>No insights yet. Log some reading sessions first!</p>
      </div>`;
    return;
  }

  container.innerHTML = `
    <div class="insights-grid">
      ${insights.map(i => `
        <div class="insight-card ${i.type}">
          <div class="insight-icon">${insightIcon(i.icon)}</div>
          <div class="insight-body">
            <h4>${escHtml(i.title)}</h4>
            <p>${escHtml(i.message)}</p>
          </div>
        </div>
      `).join('')}
    </div>
  `;
}

async function loadAnalytics() {
  const container = document.getElementById('analytics-container');
  container.innerHTML = '<div class="spinner"></div>';

  const result = await api.get('/api/insights/analytics');
  if (!result) return;

  const a = result.analytics;

  container.innerHTML = `
    <div class="insights-grid">
      <div class="insight-card info">
        <div class="insight-body">
          <h4>Total Sessions</h4>
          <p>${a.total_sessions}</p>
        </div>
      </div>

      <div class="insight-card info">
        <div class="insight-body">
          <h4>Preferred Reading Time</h4>
          <p>${escHtml(a.preferred_reading_time)}</p>
        </div>
      </div>

      <div class="insight-card info">
        <div class="insight-body">
          <h4>Consistency Score</h4>
          <p>${a.consistency_score}%</p>
        </div>
      </div>

      <div class="insight-card info">
        <div class="insight-body">
          <h4>Average Session Duration</h4>
          <p>${a.avg_duration_minutes} minutes</p>
        </div>
      </div>

      <div class="insight-card info">
        <div class="insight-body">
          <h4>Session Duration Patterns</h4>
          <p>
            Short: ${a.session_duration_patterns.Short}<br>
            Medium: ${a.session_duration_patterns.Medium}<br>
            Long: ${a.session_duration_patterns.Long}
          </p>
        </div>
      </div>

      <div class="insight-card info">
        <div class="insight-body">
          <h4>Reading Streak</h4>
          <p>${a.reading_streak} day(s)</p>
        </div>
      </div>
    </div>
  `;
}

function escHtml(str) {
  const d = document.createElement('div');
  d.textContent = str;
  return d.innerHTML;
}

document.addEventListener('DOMContentLoaded', async () => {
  await loadInsights();
  await loadAnalytics();
});

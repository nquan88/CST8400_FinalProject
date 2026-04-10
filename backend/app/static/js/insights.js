async function loadInsights() {
  const container = document.getElementById('insights-container');
  container.innerHTML = '<div class="spinner"></div>';

  const result = await api.get('/api/insights/');
  if (!result) return;

  const insights = result.insights;

  if (!insights.length) {
    container.innerHTML = `
      <div class="empty-state">
        <div class="empty-icon">🔍</div>
        <p>No insights yet. Log some reading sessions first!</p>
      </div>`;
    return;
  }

  container.innerHTML = `<div class="insights-grid">
    ${insights.map(i => `
      <div class="insight-card ${i.type}">
        <div class="insight-icon">${insightIcon(i.icon)}</div>
        <div class="insight-body">
          <h4>${escHtml(i.title)}</h4>
          <p>${escHtml(i.message)}</p>
        </div>
      </div>`).join('')}
  </div>`;
}

function escHtml(str) {
  const d = document.createElement('div');
  d.textContent = str;
  return d.innerHTML;
}

document.addEventListener('DOMContentLoaded', loadInsights);

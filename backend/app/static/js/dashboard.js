let charts = {};

async function loadDashboard() {
  const result = await api.get('/api/insights/analytics');
  if (!result) return;

  const a = result.analytics;

  // ── Stat cards ──────────────────────────────────────────────────────────
  document.getElementById('stat-sessions').textContent  = a.total_sessions;
  document.getElementById('stat-pages').textContent     = a.total_pages;
  document.getElementById('stat-hours').textContent     = Math.round(a.total_minutes / 60);
  document.getElementById('stat-avg').textContent       = a.avg_duration_minutes + ' min';
  document.getElementById('stat-streak').textContent    = a.reading_streak + ' day' + (a.reading_streak !== 1 ? 's' : '');
  document.getElementById('stat-consist').textContent   = a.consistency_score + '%';
  document.getElementById('stat-pref').textContent      = a.preferred_reading_time;
  document.getElementById('stat-freq').textContent      = a.reading_frequency_per_week + '/wk';

  // ── Charts ───────────────────────────────────────────────────────────────
  renderActivityChart(a.sessions_last_30_days);
  renderDowChart(a.sessions_by_day_of_week);
  renderMoodChart(a.mood_distribution);
  renderGenreChart(a.genre_distribution);
}

function renderActivityChart(data) {
  const labels = data.map(d => d.date);
  const values = data.map(d => d.duration_minutes);

  const ctx = document.getElementById('chart-activity').getContext('2d');
  if (charts.activity) charts.activity.destroy();

  charts.activity = new Chart(ctx, {
    type: 'line',
    data: {
      labels,
      datasets: [{
        label: 'Minutes Read',
        data: values,
        borderColor: '#2563eb',
        backgroundColor: 'rgba(37,99,235,.1)',
        borderWidth: 2,
        fill: true,
        tension: 0.3,
        pointRadius: 3,
      }],
    },
    options: {
      responsive: true,
      plugins: { legend: { display: false } },
      scales: {
        x: { ticks: { maxTicksLimit: 10, font: { size: 11 } } },
        y: { beginAtZero: true, ticks: { font: { size: 11 } } },
      },
    },
  });
}

function renderDowChart(data) {
  const days   = Object.keys(data);
  const counts = Object.values(data);

  const ctx = document.getElementById('chart-dow').getContext('2d');
  if (charts.dow) charts.dow.destroy();

  charts.dow = new Chart(ctx, {
    type: 'bar',
    data: {
      labels: days.map(d => d.slice(0, 3)),
      datasets: [{
        label: 'Sessions',
        data: counts,
        backgroundColor: '#2563eb',
        borderRadius: 5,
      }],
    },
    options: {
      responsive: true,
      plugins: { legend: { display: false } },
      scales: {
        y: { beginAtZero: true, ticks: { stepSize: 1, font: { size: 11 } } },
        x: { ticks: { font: { size: 11 } } },
      },
    },
  });
}

function renderMoodChart(data) {
  if (!Object.keys(data).length) return;

  const ctx = document.getElementById('chart-mood').getContext('2d');
  if (charts.mood) charts.mood.destroy();

  charts.mood = new Chart(ctx, {
    type: 'doughnut',
    data: {
      labels: Object.keys(data),
      datasets: [{
        data: Object.values(data),
        backgroundColor: ['#2563eb','#16a34a','#f59e0b','#dc2626'],
        borderWidth: 2,
      }],
    },
    options: {
      responsive: true,
      plugins: { legend: { position: 'bottom', labels: { font: { size: 12 }, padding: 12 } } },
    },
  });
}

function renderGenreChart(data) {
  if (!Object.keys(data).length) return;

  const ctx = document.getElementById('chart-genre').getContext('2d');
  if (charts.genre) charts.genre.destroy();

  const palette = ['#2563eb','#16a34a','#f59e0b','#dc2626','#7c3aed','#0284c7','#d97706'];

  charts.genre = new Chart(ctx, {
    type: 'doughnut',
    data: {
      labels: Object.keys(data),
      datasets: [{
        data: Object.values(data),
        backgroundColor: palette,
        borderWidth: 2,
      }],
    },
    options: {
      responsive: true,
      plugins: { legend: { position: 'bottom', labels: { font: { size: 12 }, padding: 12 } } },
    },
  });
}
<<<<<<< HEAD

=======
document.addEventListener('DOMContentLoaded', function () {

    const labels = goalData.map(d => d.date);
    const actual = goalData.map(d => d.actual);
    const goal = goalData.map(d => d.goal);

    new Chart(document.getElementById('chart-goal'), {
        type: 'bar',
        data: {
            labels: labels,
            datasets: [
                {
                    label: 'Actual Reading',
                    data: actual,
                },
                {
                    label: 'Goal',
                    data: goal,
                }
            ]
        }
    });

});
>>>>>>> 47582d5b5ef8a842817fcb1679ea1afc4b5818a0
document.addEventListener('DOMContentLoaded', loadDashboard);

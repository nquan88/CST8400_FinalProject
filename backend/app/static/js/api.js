/**
 * Lightweight API client.
 * All requests are same-origin (Flask serves both frontend and API).
 */
const api = {
  async request(method, url, body = null) {
    const opts = {
      method,
      headers: { 'Content-Type': 'application/json' },
      credentials: 'same-origin',
    };
    if (body) opts.body = JSON.stringify(body);

    const res = await fetch(url, opts);

    if (res.status === 401) {
      window.location.href = '/login';
      return null;
    }

    return res.json();
  },

  get(url)          { return this.request('GET',    url);       },
  post(url, data)   { return this.request('POST',   url, data); },
  put(url, data)    { return this.request('PUT',    url, data); },
  delete(url)       { return this.request('DELETE', url);       },
};

/** Show an alert element with a message. type: 'error' | 'success' */
function showAlert(elId, message, type = 'error') {
  const el = document.getElementById(elId);
  if (!el) return;
  el.textContent = message;
  el.className = `alert alert-${type} show`;
}

function hideAlert(elId) {
  const el = document.getElementById(elId);
  if (el) el.className = 'alert';
}

/** Map insight type to emoji */
function insightIcon(type) {
  const icons = {
    fire: '🔥', trophy: '🏆', bolt: '⚡', bullseye: '🎯',
    clock: '⏱️', lightbulb: '💡', 'chart-line': '📈',
    'exclamation-triangle': '⚠️', sun: '🌅', 'cloud-sun': '☀️',
    moon: '🌙', star: '🌃', 'layer-group': '📚', compass: '🗺️',
    'calendar-alt': '📅', book: '📖',
  };
  return icons[type] || '📌';
}

/** Format minutes as "Xh Ym" */
function fmtDuration(mins) {
  if (mins < 60) return `${mins}m`;
  const h = Math.floor(mins / 60);
  const m = mins % 60;
  return m ? `${h}h ${m}m` : `${h}h`;
}

/** Status badge HTML */
function statusBadge(status) {
  const map = {
    to_read:   ['badge-gray',   'To Read'],
    reading:   ['badge-blue',   'Reading'],
    completed: ['badge-green',  'Completed'],
    abandoned: ['badge-red',    'Abandoned'],
  };
  const [cls, label] = map[status] || ['badge-gray', status];
  return `<span class="badge ${cls}">${label}</span>`;
}

/** Difficulty badge HTML */
function diffBadge(level) {
  const map = {
    easy:   ['badge-green',  'Easy'],
    medium: ['badge-yellow', 'Medium'],
    hard:   ['badge-red',    'Hard'],
  };
  const [cls, label] = map[level] || ['badge-gray', level];
  return `<span class="badge ${cls}">${label}</span>`;
}

/** Mood badge HTML */
function moodBadge(mood) {
  const map = {
    focused:    ['badge-blue',   '🎯 Focused'],
    energized:  ['badge-green',  '⚡ Energized'],
    distracted: ['badge-yellow', '😵 Distracted'],
    tired:      ['badge-gray',   '😴 Tired'],
  };
  const [cls, label] = map[mood] || ['badge-gray', mood];
  return `<span class="badge ${cls}">${label}</span>`;
}

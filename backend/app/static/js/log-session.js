// ── Populate book select ──────────────────────────────────────────────────────
async function loadBooks() {
  const result = await api.get('/api/books/');
  if (!result) return;

  const sel = document.getElementById('f-book');
  const books = result.books.filter(b => b.status !== 'completed' && b.status !== 'abandoned');

  if (!books.length) {
    sel.innerHTML = '<option value="">No books available — add a book first</option>';
    return;
  }

  sel.innerHTML = '<option value="">Select a book…</option>' +
    books.map(b => `<option value="${b.id}">${escHtml(b.title)}</option>`).join('');
}

function escHtml(str) {
  const d = document.createElement('div');
  d.textContent = str;
  return d.innerHTML;
}

// ── Set today's date as default ───────────────────────────────────────────────
function setDefaults() {
  const today = new Date().toISOString().split('T')[0];
  document.getElementById('f-date').value = today;
}

// ── Auto-calculate duration from start/end time ───────────────────────────────
function calcDuration() {
  const start = document.getElementById('f-start').value;
  const end   = document.getElementById('f-end').value;
  if (!start || !end) return;

  const [sh, sm] = start.split(':').map(Number);
  const [eh, em] = end.split(':').map(Number);
  const mins = (eh * 60 + em) - (sh * 60 + sm);

  if (mins > 0) {
    document.getElementById('f-duration').value = mins;
  }
}

document.getElementById('f-start').addEventListener('change', calcDuration);
document.getElementById('f-end').addEventListener('change', calcDuration);

// ── Recent sessions ───────────────────────────────────────────────────────────
async function loadRecentSessions() {
  const result = await api.get('/api/sessions/');
  if (!result) return;

  const sessions = result.sessions.slice(0, 10);
  const tbody    = document.getElementById('sessions-tbody');

  if (!sessions.length) {
    tbody.innerHTML = `<tr><td colspan="6" style="text-align:center;color:var(--text-muted);padding:20px">No sessions logged yet.</td></tr>`;
    return;
  }

  tbody.innerHTML = sessions.map(s => `
    <tr>
      <td>${s.session_date}</td>
      <td>${escHtml(s.book_title || '—')}</td>
      <td>${fmtDuration(s.duration_minutes)}</td>
      <td>${s.pages_read || 0} pages</td>
      <td>${moodBadge(s.mood)}</td>
      <td>
        <button class="btn btn-ghost" style="color:var(--danger);font-size:13px" onclick="deleteSession(${s.id})">Delete</button>
      </td>
    </tr>`).join('');
}

async function deleteSession(id) {
  if (!confirm('Delete this session?')) return;
  const res = await api.delete(`/api/sessions/${id}`);
  if (res && !res.error) loadRecentSessions();
}

// ── Submit ────────────────────────────────────────────────────────────────────
document.getElementById('session-form').addEventListener('submit', async (e) => {
  e.preventDefault();
  hideAlert('session-alert');

  const data = {
    book_id:          parseInt(document.getElementById('f-book').value),
    session_date:     document.getElementById('f-date').value,
    start_time:       document.getElementById('f-start').value || null,
    end_time:         document.getElementById('f-end').value   || null,
    duration_minutes: parseInt(document.getElementById('f-duration').value),
    pages_read:       parseInt(document.getElementById('f-pages').value) || 0,
    mood:             document.getElementById('f-mood').value,
    notes:            document.getElementById('f-notes').value.trim() || null,
  };

  if (!data.book_id) { showAlert('session-alert', 'Please select a book.'); return; }
  if (!data.duration_minutes || data.duration_minutes <= 0) {
    showAlert('session-alert', 'Duration must be greater than 0.');
    return;
  }

  const res = await api.post('/api/sessions/', data);
  if (!res) return;
  if (res.error) { showAlert('session-alert', res.error); return; }

  showAlert('session-alert', 'Session logged successfully!', 'success');
  document.getElementById('session-form').reset();
  setDefaults();
  loadRecentSessions();
});

document.addEventListener('DOMContentLoaded', () => {
  setDefaults();
  loadBooks();
  loadRecentSessions();
});

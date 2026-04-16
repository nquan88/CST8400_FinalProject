let allBooks = [];
let editingId = null;

// ── Load & render ────────────────────────────────────────────────────────────
async function loadBooks() {
  const result = await api.get('/api/books/');
  if (!result) return;

  allBooks = result.books;
  renderBooks(allBooks);
}

function renderBooks(books) {
  const tbody = document.getElementById('books-tbody');

  if (!books.length) {
    tbody.innerHTML = `
      <tr><td colspan="6">
        <div class="empty-state">
          <div class="empty-icon">📚</div>
          <p>No books yet. Add your first book to get started!</p>
        </div>
      </td></tr>`;
    return;
  }

  tbody.innerHTML = books.map(b => `
    <tr>
      <td><strong>${escHtml(b.title)}</strong></td>
      <td>${escHtml(b.author || '—')}</td>
      <td>${escHtml(b.genre  || '—')}</td>
      <td>${diffBadge(b.difficulty_level)}</td>
      <td>${statusBadge(b.status)}</td>
      <td>
        <button class="btn btn-ghost" onclick="openEdit(${b.id})">Edit</button>
        <button class="btn btn-ghost" style="color:var(--danger)" onclick="deleteBook(${b.id})">Delete</button>
      </td>
    </tr>`).join('');
}

function escHtml(str) {
  const d = document.createElement('div');
  d.textContent = str;
  return d.innerHTML;
}

// ── Modal ────────────────────────────────────────────────────────────────────
function openAdd() {
  editingId = null;
  document.getElementById('modal-title').textContent = 'Add Book';
  document.getElementById('book-form').reset();
  hideAlert('book-alert');
  document.getElementById('book-modal').classList.add('open');
}

function openEdit(id) {
  editingId = id;
  const b = allBooks.find(x => x.id === id);
  if (!b) return;

  document.getElementById('modal-title').textContent = 'Edit Book';
  document.getElementById('f-title').value      = b.title  || '';
  document.getElementById('f-author').value     = b.author || '';
  document.getElementById('f-genre').value      = b.genre  || '';
  document.getElementById('f-difficulty').value = b.difficulty_level || 'medium';
  document.getElementById('f-pages').value      = b.total_pages || '';
  document.getElementById('f-status').value     = b.status || 'to_read';
  hideAlert('book-alert');
  document.getElementById('book-modal').classList.add('open');
}

function closeModal() {
  document.getElementById('book-modal').classList.remove('open');
}

// ── Save ─────────────────────────────────────────────────────────────────────
document.getElementById('book-form').addEventListener('submit', async (e) => {
  e.preventDefault();
  hideAlert('book-alert');

  const data = {
    title:            document.getElementById('f-title').value.trim(),
    author:           document.getElementById('f-author').value.trim(),
    genre:            document.getElementById('f-genre').value.trim(),
    difficulty_level: document.getElementById('f-difficulty').value,
    total_pages:      parseInt(document.getElementById('f-pages').value) || null,
    status:           document.getElementById('f-status').value,
  };

  if (!data.title) {
    showAlert('book-alert', 'Title is required.');
    return;
  }

  const res = editingId
    ? await api.put(`/api/books/${editingId}`, data)
    : await api.post('/api/books/', data);

  if (!res) return;
  if (res.error) { showAlert('book-alert', res.error); return; }

  closeModal();
  loadBooks();
});

// ── Delete ────────────────────────────────────────────────────────────────────
async function deleteBook(id) {
  if (!confirm('Delete this book and all its reading sessions?')) return;
  const res = await api.delete(`/api/books/${id}`);
  if (res && !res.error) loadBooks();
}

// ── Filter ────────────────────────────────────────────────────────────────────
document.getElementById('filter-status').addEventListener('change', function () {
  const val = this.value;
  renderBooks(val ? allBooks.filter(b => b.status === val) : allBooks);
});

document.getElementById('search-input').addEventListener('input', function () {
  const q = this.value.toLowerCase();
  renderBooks(allBooks.filter(b =>
    b.title.toLowerCase().includes(q) ||
    (b.author || '').toLowerCase().includes(q)
  ));
});

document.addEventListener('DOMContentLoaded', loadBooks);

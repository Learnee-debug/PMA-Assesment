import { useEffect, useState } from 'react';
import { api } from '../api';

const EMPTY_FORM = { location: '', startDate: '', endDate: '' };

export default function RecordsManager() {
  const [records, setRecords] = useState([]);
  const [form, setForm] = useState(EMPTY_FORM);
  const [editingId, setEditingId] = useState(null);
  const [error, setError] = useState('');
  const [busy, setBusy] = useState(false);

  async function refresh() {
    try {
      const { records } = await api.listRecords();
      setRecords(records);
    } catch (err) {
      setError(err.message);
    }
  }

  useEffect(() => {
    refresh();
  }, []);

  async function handleSubmit(e) {
    e.preventDefault();
    setError('');
    setBusy(true);
    try {
      if (editingId) {
        await api.updateRecord(editingId, form);
      } else {
        await api.createRecord(form);
      }
      setForm(EMPTY_FORM);
      setEditingId(null);
      await refresh();
    } catch (err) {
      setError(err.message);
    } finally {
      setBusy(false);
    }
  }

  function startEdit(record) {
    setEditingId(record.id);
    setForm({
      location: record.location_query,
      startDate: record.start_date,
      endDate: record.end_date,
    });
  }

  function cancelEdit() {
    setEditingId(null);
    setForm(EMPTY_FORM);
  }

  async function handleDelete(id) {
    setError('');
    try {
      await api.deleteRecord(id);
      await refresh();
    } catch (err) {
      setError(err.message);
    }
  }

  return (
    <section className="records-manager">
      <h2>Saved Weather Records</h2>
      <p className="muted">
        Save a location + date range, then read, update, delete, or export what's stored in the database.
      </p>

      <form className="record-form" onSubmit={handleSubmit}>
        <input
          type="text"
          placeholder="Location"
          value={form.location}
          onChange={(e) => setForm({ ...form, location: e.target.value })}
          required
        />
        <input
          type="date"
          value={form.startDate}
          onChange={(e) => setForm({ ...form, startDate: e.target.value })}
          required
        />
        <input
          type="date"
          value={form.endDate}
          onChange={(e) => setForm({ ...form, endDate: e.target.value })}
          required
        />
        <button type="submit" disabled={busy}>
          {editingId ? 'Update Record' : 'Save Record'}
        </button>
        {editingId && (
          <button type="button" className="secondary" onClick={cancelEdit}>
            Cancel
          </button>
        )}
      </form>

      {error && <p className="error-text">⚠️ {error}</p>}

      <div className="export-bar">
        Export all records:
        {['json', 'csv', 'xml', 'md', 'pdf'].map((fmt) => (
          <a key={fmt} href={api.exportUrl(fmt)} target="_blank" rel="noreferrer">
            {fmt.toUpperCase()}
          </a>
        ))}
      </div>

      <div className="records-table-wrap">
        <table className="records-table">
          <thead>
            <tr>
              <th>Location</th>
              <th>Resolved</th>
              <th>Start</th>
              <th>End</th>
              <th>Updated</th>
              <th></th>
            </tr>
          </thead>
          <tbody>
            {records.length === 0 && (
              <tr><td colSpan={6} className="muted">No records yet.</td></tr>
            )}
            {records.map((r) => (
              <tr key={r.id}>
                <td>{r.location_query}</td>
                <td>{r.resolved_name}</td>
                <td>{r.start_date}</td>
                <td>{r.end_date}</td>
                <td>{r.updated_at}</td>
                <td className="record-actions">
                  <button onClick={() => startEdit(r)}>Edit</button>
                  <button className="danger" onClick={() => handleDelete(r.id)}>Delete</button>
                </td>
              </tr>
            ))}
          </tbody>
        </table>
      </div>
    </section>
  );
}

import React, { useEffect, useState } from "react";


function EmailList({ filter = {}, refreshTrigger = 0 }) {
  const [emails, setEmails] = useState([]);
  const [offset, setOffset] = useState(0);
  const limit = 10;
  const [loading, setLoading] = useState(false);
  const [error, setError] = useState("");

  const handleDelete = (id) => {
    fetch(`/api/email/delete/${id}`, { method: "DELETE" })
      .then(() => setEmails(emails.filter(e => e.id !== id)))
      .catch(err => console.error("Delete failed:", err));
  };

  useEffect(() => {
    let url = `/api/email/list?offset=${offset}&limit=${limit}`;
    // Map filter object to backend query params
    if (filter) {
      if (filter.unread) url += `&unread=true`;
      if (filter.spam) url += `&spam=true`;
      if (filter.older_than) url += `&older_than=${filter.older_than}`;
      if (filter.search) url += `&search=${encodeURIComponent(filter.search)}`;
    }
    setLoading(true);
    setError("");
    fetch(url)
      .then((res) => res.json())
      .then((data) => setEmails(data.emails))
      .catch((err) => setError("Failed to load emails"))
      .finally(() => setLoading(false));
  }, [offset, filter, refreshTrigger]);


  const handleDeleteSpam = () => {
  fetch("/api/email/delete-spam", { method: "DELETE" })
      .then(res => res.json())
      .then(data => {
        console.log("Deleted:", data.deleted_spam_count);
        // Optionally refresh the list or show a message
      });
  };

  const handleDeleteOlderThan = () => {
    const days = prompt("Delete emails older than how many days?");
    if (!days || isNaN(days) || days <= 0) return;
  fetch(`/api/email/delete-older-than/${days}`, { method: "DELETE" })
      .then(res => res.json())
      .then(data => {
        console.log("Deleted:", data.deleted_count);
        // Optionally refresh the list or show a message
      });
  };

  return (
    <div className="email-list-container">
      <div className="email-list-header">
        <h2>📬 Stored Emails</h2>
        <div className="email-list-actions">
          <button onClick={handleDeleteSpam}>🧹 Spam 7d</button>
          <button onClick={handleDeleteOlderThan}>🧹 Older Than...</button>
        </div>
      </div>
      {loading && <p>Loading...</p>}
      {error && <p className="error-msg">{error}</p>}
      <ul className="email-list">
        {emails.map(email => (
          <li key={email.id} className="email-list-item">
            <div className="email-list-row">
              <span className="email-list-label">From:</span>
              <span className="email-list-value">{email.sender || email.from_ || email.from}</span>
            </div>
            <div className="email-list-row">
              <span className="email-list-label">Email:</span>
              <span className="email-list-value">{email.email}</span>
            </div>
            <div className="email-list-row">
              <span className="email-list-label">Subject:</span>
              <span className="email-list-value">{email.subject}</span>
            </div>
            <div className="email-list-row">
              <span className="email-list-label">Status:</span>
              <span className="email-list-value">
                {email.is_spam ? <span className="email-status-spam">Spam</span> : <span className="email-status-ok">Inbox</span>}
              </span>
            </div>
            <button className="email-list-delete" onClick={() => handleDelete(email.id)}>🗑️</button>
          </li>
        ))}
      </ul>
      <div className="email-list-pagination">
        <button onClick={() => setOffset(Math.max(offset - limit, 0))} disabled={offset === 0}>⬅ Prev</button>
        <button onClick={() => setOffset(offset + limit)} disabled={emails.length < limit}>Next ➡</button>
      </div>
    </div>
  );
}

export default EmailList;

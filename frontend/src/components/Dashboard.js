// Dashboard component for displaying inbox stats and recent emails
export default function Dashboard({ stats, emails }) {
  return (
    <div>
      <h1>Inbox Stats</h1>
      <ul>
        <li>Total: {stats?.total ?? "-"}</li>
        <li>Spam: {stats?.spam ?? "-"}</li>
        <li>Unread: {stats?.unread ?? "-"}</li>
        {stats?.recent !== undefined && <li>Recent (24h): {stats.recent}</li>}
      </ul>

      <h2>Recent Emails</h2>
      <ul>
        {emails && emails.length > 0 ? (
          emails.map((email, idx) => (
            <li key={email.id || idx}>
              <strong>{email.sender}</strong> — {email.subject}
              <br />
              Received: {email.received_at} | Spam: {email.is_spam ? "Yes" : "No"} | Read: {email.is_read ? "Yes" : "No"}
            </li>
          ))
        ) : (
          <li>No recent emails.</li>
        )}
      </ul>
    </div>
  );
}

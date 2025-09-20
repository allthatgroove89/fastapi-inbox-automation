import React, { useState, useEffect } from "react";
import './App.css';
import EmailReader from './components/EmailReader';
import EmailList from "./components/EmailList";
import EmailFilter from "./components/EmailFilter";
import EmailConnectForm from "./components/EmailConnectForm";
import DashboardStats from "./components/DashboardStats";



function App() {
  const [filter, setFilter] = useState({});
  const [refreshTrigger, setRefreshTrigger] = useState(0);
  const [isConnecting, setIsConnecting] = useState(false);
  const [connectionMessage, setConnectionMessage] = useState(null);
  const [dashboardStats, setDashboardStats] = useState(null);
  // Fetch dashboard stats
  useEffect(() => {
    fetch("/api/dashboard")
      .then(res => res.json())
      .then(data => setDashboardStats(data))
      .catch(() => setDashboardStats(null));
  }, [refreshTrigger]);

  const handleConnect = ({ email, mode }) => {
    setIsConnecting(true);
    setConnectionMessage(null);
    fetch("/api/connect-email/", {
      method: "POST",
      headers: { "Content-Type": "application/json" },
      body: JSON.stringify({ email, mode })
    })
      .then(res => res.json())
      .then(data => {
        setIsConnecting(false);
        setConnectionMessage(data.message || "Connected");
        console.log("Connection response:", data);
        if (data.status === "redirect" && data.oauth_url) {
          window.open(data.oauth_url, "_blank");
        }
      })
      .catch(err => {
        setIsConnecting(false);
        setConnectionMessage("Failed to connect. Please try again.");
        console.error("Connection error:", err);
      });
  };

  // Accepts a filter object, merges with previous filter (for search input)
  const handleFilter = (newFilter) => {
    setFilter(prev => ({ ...prev, ...newFilter }));
  };

  const handleEmailRead = () => {
    fetch("/email/read", { method: "POST" })
      .then(() => setRefreshTrigger(prev => prev + 1));
  };

  return (
    <div className="dashboard-container">
      <header className="dashboard-header">
        <h1>📬 Inbox Automation Dashboard</h1>
      </header>
      <div className="dashboard-main">
        <section className="dashboard-panel dashboard-panel--left">
          <DashboardStats stats={dashboardStats} />
          {connectionMessage === "Connected" ? (
            <button
              className="logout-button"
              style={{ width: '100%', margin: '1em 0', padding: '0.75em', background: '#e74c3c', color: 'white', border: 'none', borderRadius: '4px', fontWeight: 'bold', fontSize: '1em', cursor: 'pointer' }}
              onClick={() => {
                fetch('/auth/logout', { method: 'POST' })
                  .then(() => window.location.reload());
              }}
            >
              Log out
            </button>
          ) : (
            <EmailConnectForm onSubmit={handleConnect} />
          )}
          {isConnecting && <p>Connecting...</p>}
          {connectionMessage && <p>{connectionMessage}</p>}
          <EmailFilter onFilter={handleFilter} activeSpam={filter.spam} />
          <EmailReader onRead={handleEmailRead} />
        </section>
        <section className="dashboard-panel dashboard-panel--right">
          <EmailList filter={filter} refreshTrigger={refreshTrigger} />
        </section>
      </div>
    </div>
  );
}


export default App;

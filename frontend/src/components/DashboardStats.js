import React from 'react';
import './DashboardStats.css';

function DashboardStats({ stats }) {
  if (!stats) return null;
  return (
    <div className="dashboard-stats">
      <h3>📊 Stats</h3>
      <ul>
        <li><strong>Total:</strong> {stats.total}</li>
        <li><strong>Spam:</strong> {stats.spam}</li>
        <li><strong>Unread:</strong> {stats.unread}</li>
        <li><strong>Recent (24h):</strong> {stats.recent}</li>
      </ul>
    </div>
  );
}

export default DashboardStats;

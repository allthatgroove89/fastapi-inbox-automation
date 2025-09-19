import React, { useState } from 'react';
import './EmailFilter.css';

function EmailFilter({ onFilter }) {
  const [searchTerm, setSearchTerm] = useState('');
  const [olderThan, setOlderThan] = useState('');

  const handleFilterClick = (type) => {
    onFilter({ category: type });
  };

  const handleOlderChange = (e) => {
    const days = e.target.value;
    setOlderThan(days);
    if (days) onFilter({ older_than: parseInt(days) });
  };

  const handleSearchChange = (e) => {
    const value = e.target.value;
    setSearchTerm(value);
    onFilter({ search: value });
  };

  const handleReset = () => {
    setSearchTerm('');
    setOlderThan('');
    onFilter({});
  };

  return (
    <div className="email-filter">
      <h2 className="email-filter__title">📂 Filter Emails</h2>
      <p className="email-filter__hint">Filters apply instantly to stored emails.</p>

      <div className="email-filter__labels">
        <button onClick={() => onFilter({ spam: false })}>📥 Inbox</button>
        <button onClick={() => onFilter({ spam: true })}>🧹 Spam</button>
      </div>

      <div className="email-filter__controls">
  <button onClick={() => onFilter({ spam: true })}>🧹 Spam (7d)</button>

        <label className="email-filter__dropdown">
          ⏳ Older Than:
          <select value={olderThan} onChange={handleOlderChange}>
            <option value="">Select</option>
            <option value="7">7 days</option>
            <option value="14">14 days</option>
            <option value="30">30 days</option>
          </select>
        </label>

        <input
          type="text"
          placeholder="🔍 Search..."
          value={searchTerm}
          onChange={handleSearchChange}
          className="email-filter__search"
        />

        <button onClick={handleReset} className="email-filter__reset">🔄 Reset</button>
      </div>
    </div>
  );
}

export default EmailFilter;

import React from "react";

function EmailReader() {
  const handleReadEmails = async () => {
    try {
  const response = await fetch("/api/email/read", {
        method: "POST",
        headers: { "Content-Type": "application/json" },
      });
      const data = await response.json();
      console.log("Fetched emails:", data);
      alert(`Fetched ${data.length || 0} emails`);
    } catch (error) {
      console.error("Error reading emails:", error);
      alert("Failed to fetch emails");
    }
  };

  return (
    <div>
      <button onClick={handleReadEmails}>📥 Trigger Email Read Task</button>
    </div>
  );
}

export default EmailReader;

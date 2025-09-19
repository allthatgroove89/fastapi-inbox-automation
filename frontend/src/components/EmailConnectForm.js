import React, { useState } from "react";

function EmailConnectForm(props) {
  const [email, setEmail] = useState("");
  const [mode, setMode] = useState("mock"); // "mock" or "gmail"

  const handleSubmit = function (e) {
    e.preventDefault();
    props.onSubmit({ email, mode });
  };

  return (
    React.createElement("div", { className: "connect-inbox-block" },
      React.createElement("form", { onSubmit: handleSubmit, style: styles.form },
        React.createElement("h2", null, "Connect Your Inbox"),

        React.createElement("input", {
          type: "email",
          id: "connect-email",
          name: "connect-email",
          placeholder: "Enter your email",
          value: email,
          onChange: function (e) { setEmail(e.target.value); },
          required: true,
          style: styles.input
        }),

        React.createElement("select", {
          id: "connect-mode",
          name: "connect-mode",
          value: mode,
          onChange: function (e) { setMode(e.target.value); },
          style: styles.select
        },
          React.createElement("option", { value: "mock" }, "Mock Mode"),
          React.createElement("option", { value: "gmail" }, "Gmail OAuth")
        ),

        React.createElement("button", {
          type: "submit",
          style: styles.button
        }, "Connect")
      )
    )
  );
}

const styles = {
  form: {
    display: "flex",
    flexDirection: "column",
    gap: "1rem",
    maxWidth: "400px",
    margin: "2rem auto",
    padding: "1rem",
    border: "1px solid #ccc",
    borderRadius: "8px",
    backgroundColor: "#f9f9f9"
  },
  input: {
    padding: "0.5rem",
    fontSize: "1rem"
  },
  select: {
    padding: "0.5rem",
    fontSize: "1rem"
  },
  button: {
    padding: "0.75rem",
    fontSize: "1rem",
    backgroundColor: "#007bff",
    color: "#fff",
    border: "none",
    borderRadius: "4px",
    cursor: "pointer"
  }
};

export default EmailConnectForm;

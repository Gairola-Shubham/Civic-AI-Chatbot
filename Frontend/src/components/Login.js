import { useState } from "react";

function Login({ onLogin }) {

  const [username, setUsername] = useState("");
  const [password, setPassword] = useState("");
  const [message, setMessage] = useState("");

  /* ================= SIGN UP ================= */
  function handleSignUp() {

    if (!username || !password) {
      setMessage("Please enter username and password");
      return;
    }

    localStorage.setItem(username, password);

    const users = JSON.parse(localStorage.getItem("users")) || [];

    if (!users.includes(username)) {
      users.push(username);
      localStorage.setItem("users", JSON.stringify(users));
    }

    setMessage("Account created! You can now log in.");
  }

  /* ================= LOGIN ================= */
  function handleLogin() {

    const storedPassword = localStorage.getItem(username);

    if (storedPassword === password) {
      setMessage("");
      onLogin(username);
    } else {
      setMessage("Invalid username or password");
    }
  }

  return (

    <div className="login-container">

      <div className="login-box">

        <h1 className="login-title">CIVIC AI</h1>
        <p className="login-subtitle">Your Civic Assistant</p>

        <input
          className="login-input"
          placeholder="Username"
          value={username}
          onChange={(e) => setUsername(e.target.value)}
        />

        <input
          className="login-input"
          type="password"
          placeholder="Password"
          value={password}
          onChange={(e) => setPassword(e.target.value)}
        />

        <div className="button-group">
          <button className="login-btn" onClick={handleLogin}>
            Login
          </button>

          <button className="signup-btn" onClick={handleSignUp}>
            Sign Up
          </button>
        </div>

        <button
          className="guest-btn"
          onClick={() => onLogin("Guest")}
        >
          Continue as Guest
        </button>

        {message && <p className="login-message">{message}</p>}

      </div>

    </div>
  );
}

export default Login;
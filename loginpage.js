import React from "react";
import LoginForm from "../components/LoginForm";

const LoginPage = ({ onLogin }) => (
  <div className="login-container">
    <div className="login-header">
      <h1>नेपाली मतदान प्रणाली</h1>
      <p>Nepali Global Voting System</p>
    </div>
    <LoginForm onLogin={onLogin} />
  </div>
);

export default LoginPage;

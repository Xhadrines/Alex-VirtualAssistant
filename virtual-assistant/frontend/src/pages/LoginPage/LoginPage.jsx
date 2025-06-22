import React, { useState } from "react";
import axios from "axios";
import { useNavigate } from "react-router-dom";
import "./LoginPage.css";

const API_URL = import.meta.env.VITE_CHAT_API;

const LoginPage = () => {
  const [username, setUsername] = useState("");
  const [password, setPassword] = useState("");
  const [feedback, setFeedback] = useState("");
  const [feedbackColor, setFeedbackColor] = useState("");

  const navigate = useNavigate();

  const handleLogin = async () => {
    if (!username || !password) {
      setFeedback("Completeaza toate campurile!");
      setFeedbackColor("red");
      return;
    }

    try {
      const response = await axios.post(`${API_URL}/api/login/`, {
        identifier: username,
        password: password,
      });

      if (response.data.token) {
        localStorage.setItem("token", response.data.token);
        localStorage.setItem("user_id", response.data.user_id);
        localStorage.setItem("username", username);
        localStorage.setItem("first_name", response.data.first_name);
        localStorage.setItem("last_name", response.data.last_name);

        localStorage.setItem(
          "is_superuser",
          response.data.is_superuser ? "true" : "false"
        );
        localStorage.setItem(
          "is_staff",
          response.data.is_staff ? "true" : "false"
        );

        setFeedback("Te-ai logat cu succes!");
        setFeedbackColor("green");

        navigate("/chat");
      } else {
        setFeedback(response.data.message || "Autentificare esuata.");
        setFeedbackColor("red");
      }
    } catch (error) {
      setFeedback("A aparut o eroare. Verifica datele introduse.");
      setFeedbackColor("red");
    }
  };

  const navigateToHome = () => {
    navigate("/");
  };

  const handleKeyDown = (e) => {
    if (e.key === "Enter") {
      handleLogin();
    }
  };

  return (
    <div className="login-container">
      <div className="header">
        <button className="back-btn" onClick={navigateToHome}>
          <img src="/back.png" alt="Inapoi" className="button-icon" />
        </button>
        <h1>Autentificare</h1>
      </div>
      <div className="login-form-container">
        <div className="input-group">
          <label htmlFor="username">Utilizator sau Email</label>
          <input
            type="text"
            id="username"
            placeholder="Introdu username-ul sau email-ul"
            value={username}
            onChange={(e) => setUsername(e.target.value)}
            onKeyDown={handleKeyDown}
          />
        </div>
        <div className="input-group">
          <label htmlFor="password">Parolă</label>
          <input
            type="password"
            id="password"
            placeholder="Introduceti parola"
            value={password}
            onChange={(e) => setPassword(e.target.value)}
            onKeyDown={handleKeyDown}
          />
        </div>
        <button className="login-btn" onClick={handleLogin}>
          Conectare
        </button>
        <div className="register-redirect">
          <button
            type="button"
            className="register-link"
            onClick={() => navigate("/register")}
          >
            {" "}
            Nu ai cont? Creează unul!
          </button>
          <button
            type="button"
            className="reset-link"
            onClick={() => navigate("/reset-password")}
          >
            Ai uitat parola? Resetează-o!
          </button>
        </div>
      </div>
      {feedback && (
        <div className="feedback" style={{ color: feedbackColor }}>
          {feedback}
        </div>
      )}
    </div>
  );
};

export default LoginPage;

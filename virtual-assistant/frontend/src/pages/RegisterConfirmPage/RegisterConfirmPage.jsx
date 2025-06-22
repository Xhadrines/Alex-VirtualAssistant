import React, { useState } from "react";
import axios from "axios";
import { useNavigate, useLocation } from "react-router-dom";
import "./RegisterConfirmPage.css";

const API_URL = import.meta.env.VITE_CHAT_API;

const RegisterConfirmPage = () => {
  const location = useLocation();
  const emailFromState =
    location.state?.email || localStorage.getItem("registerEmail") || "";

  const [email] = useState(emailFromState);
  const [username, setUsername] = useState("");
  const [password, setPassword] = useState("");
  const [confirmPassword, setConfirmPassword] = useState("");
  const [feedback, setFeedback] = useState("");
  const navigate = useNavigate();

  const validatePassword = (pass) => {
    const regex = /^(?=.*[A-Z])(?=.*\d)(?=.*[^A-Za-z0-9]).{5,}$/;
    return regex.test(pass);
  };

  const handleCreateAccount = async () => {
    if (!username || !password || !confirmPassword) {
      setFeedback("Completeaza toate campurile!");
      return;
    }

    if (password !== confirmPassword) {
      setFeedback("Parolele nu coincid!");
      return;
    }

    if (!validatePassword(password)) {
      setFeedback(
        "Parola trebuie sa contina minim 5 caractere, o litera mare, un caracter special si o cifra."
      );
      return;
    }

    try {
      const response = await axios.post(`${API_URL}/api/user/active/`, {
        email,
        username,
        password,
      });

      if (response.data.success) {
        setFeedback("Cont creat cu succes! Redirectare...");
        setTimeout(() => {
          navigate("/login");
        }, 2000);
      } else {
        setFeedback(response.data.error || "A aparut o eroare la creare.");
      }
    } catch (error) {
      setFeedback(error.response?.data?.error || "Eroare de retea sau server.");
    }
  };

  return (
    <div className="login-container">
      <header className="header">
        <button className="back-btn" onClick={() => navigate("/login")}>
          <img src="/back.png" alt="Inapoi" className="button-icon" />
        </button>
        <h1>Confirmare Creare Cont</h1>
      </header>

      <form
        className="login-form-container"
        onSubmit={(e) => e.preventDefault()}
      >
        <div className="input-group">
          <label>Nume utilizator</label>
          <input
            type="text"
            placeholder="Alege un username"
            value={username}
            onChange={(e) => setUsername(e.target.value)}
          />
        </div>

        <div className="input-group">
          <label>Parola</label>
          <input
            type="password"
            placeholder="Introdu parola"
            value={password}
            onChange={(e) => setPassword(e.target.value)}
          />
        </div>

        <div className="input-group">
          <label>Confirma Parola</label>
          <input
            type="password"
            placeholder="Reintrodu parola"
            value={confirmPassword}
            onChange={(e) => setConfirmPassword(e.target.value)}
          />
        </div>

        <button className="login-btn" onClick={handleCreateAccount}>
          Creeaza contul
        </button>

        {feedback && <div className="feedback">{feedback}</div>}
      </form>
    </div>
  );
};

export default RegisterConfirmPage;

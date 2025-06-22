import React, { useState } from "react";
import axios from "axios";
import { useNavigate, useLocation } from "react-router-dom";
import "./ResetPasswordConfirmPage.css";

const API_URL = import.meta.env.VITE_CHAT_API;

const ResetPasswordConfirmPage = () => {
  const location = useLocation();
  const navigate = useNavigate();

  // Extrage tokenul din query params
  const queryParams = new URLSearchParams(location.search);
  const token = queryParams.get("token");

  // Ia email-ul din localStorage (sau îl poți cere din input dacă vrei)
  const email = localStorage.getItem("resetEmail") || "";

  const [password, setPassword] = useState("");
  const [confirmPassword, setConfirmPassword] = useState("");
  const [feedback, setFeedback] = useState("");

  const validatePassword = (pass) => {
    const regex = /^(?=.*[A-Z])(?=.*\d)(?=.*[^A-Za-z0-9]).{5,}$/;
    return regex.test(pass);
  };

  const handleResetPassword = async () => {
    if (!email || !token) {
      setFeedback("Email și token sunt obligatorii.");
      return;
    }

    if (!password || !confirmPassword) {
      setFeedback("Completează toate câmpurile!");
      return;
    }

    if (password !== confirmPassword) {
      setFeedback("Parolele nu coincid!");
      return;
    }

    if (!validatePassword(password)) {
      setFeedback(
        "Parola trebuie să conțină minim 5 caractere, o literă mare, un caracter special și o cifră."
      );
      return;
    }

    try {
      const response = await axios.post(`${API_URL}/api/user/reset/password/`, {
        email,
        token,
        password,
      });

      if (response.data.message) {
        setFeedback("Parola a fost resetată cu succes! Redirectare...");
        setTimeout(() => {
          navigate("/login");
        }, 2000);
      } else {
        setFeedback(response.data.error || "A apărut o eroare la resetare.");
      }
    } catch (error) {
      setFeedback(error.response?.data?.error || "Eroare de rețea sau server.");
    }
  };

  return (
    <div className="reset-password-container">
      <header className="header">
        <button className="back-btn" onClick={() => navigate("/login")}>
          <img src="/back.png" alt="Înapoi" className="button-icon" />
        </button>
        <h1>Resetare Parolă</h1>
      </header>

      <form
        className="login-form-container"
        onSubmit={(e) => e.preventDefault()}
      >
        <div className="input-group">
          <label>Parolă Nouă</label>
          <input
            type="password"
            placeholder="Introdu parola nouă"
            value={password}
            onChange={(e) => setPassword(e.target.value)}
          />
        </div>

        <div className="input-group">
          <label>Confirmă Parola</label>
          <input
            type="password"
            placeholder="Reintrodu parola"
            value={confirmPassword}
            onChange={(e) => setConfirmPassword(e.target.value)}
          />
        </div>

        <button className="login-btn" onClick={handleResetPassword}>
          Resetează Parola
        </button>

        {feedback && <div className="feedback">{feedback}</div>}
      </form>
    </div>
  );
};

export default ResetPasswordConfirmPage;

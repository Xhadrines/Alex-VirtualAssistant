import React, { useState } from "react";
import axios from "axios";
import { useNavigate } from "react-router-dom";
import "./ResetPasswordPage.css"; // îi poți da același CSS sau unul separat

const API_URL = import.meta.env.VITE_CHAT_API;

const ResetPasswordPage = () => {
  const [email, setEmail] = useState("");
  const [feedback, setFeedback] = useState("");
  const [emailSent, setEmailSent] = useState(false);
  const navigate = useNavigate();

  const handleBack = () => {
    navigate("/login");
  };

  const handleCheckEmail = async () => {
    if (email.trim() === "") {
      setFeedback("Introdu un email valid!");
      return;
    }

    try {
      // schimbă endpoint-ul în funcție de API-ul tău pentru reset parola
      const response = await axios.get(`${API_URL}/api/user/email/`, {
        params: { email },
      });

      if (response.data.email_exists) {
        setEmailSent(true);
        setFeedback("");
        localStorage.setItem("resetEmail", email);
      } else {
        setFeedback("Emailul NU exista in sistem!");
      }
    } catch (error) {
      setFeedback("A aparut o eroare la verificarea emailului.");
    }
  };

  return (
    <>
      <header className="register-header">
        <button className="back-btn" onClick={handleBack}>
          <img src="/back.png" alt="Inapoi" className="button-icon" />
        </button>
        <h1>Resetare Parolă</h1>
      </header>

      <main className="register-main">
        {!emailSent ? (
          <div className="register-box">
            <input
              type="email"
              placeholder="Introdu adresa ta de email"
              value={email}
              onChange={(e) => setEmail(e.target.value)}
              className="email-input"
            />
            <button onClick={handleCheckEmail} className="action-btn">
              Continua
            </button>
            {feedback && <div className="feedback">{feedback}</div>}
          </div>
        ) : (
          <div className="register-box">
            <h2>Email-ul a fost trimis</h2>
            <p className="email-sent-text">{email}</p>
            <button className="action-btn" onClick={() => navigate("/login")}>
              Inapoi la Login
            </button>
          </div>
        )}
      </main>
    </>
  );
};

export default ResetPasswordPage;

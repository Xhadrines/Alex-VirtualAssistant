import React, { useState } from 'react';
import axios from 'axios';
import { useNavigate } from 'react-router-dom';
import './RegisterPage.css';

const API_URL = import.meta.env.VITE_CHAT_API;

const RegisterPage = () => {
  const [email, setEmail] = useState('');
  const [emailValid, setEmailValid] = useState(false);
  const [username, setUsername] = useState('');
  const [password, setPassword] = useState('');
  const [confirmPassword, setConfirmPassword] = useState('');
  const [feedback, setFeedback] = useState('');
  const navigate = useNavigate();

  const validatePassword = (pass) => {
    const regex = /^(?=.*[A-Z])(?=.*\d)(?=.*[^A-Za-z0-9]).{5,}$/;
    return regex.test(pass);
  };

  const handleCheckEmail = async () => {
    if (email.trim() === '') {
      setFeedback('Introdu un email valid!');
      return;
    }

    try {
      const response = await axios.get(`${API_URL}/api/user/email/`, {
        params: { email }
      });

      if (response.data.email_exists) {
        setEmailValid(true);
        setFeedback('');
      } else {
        setFeedback('Emailul NU există în sistem!');
        setEmailValid(false);
      }
    } catch (error) {
      setFeedback('A apărut o eroare la verificarea emailului.');
    }
  };

  const handleCreateAccount = async () => {
    if (!username || !password || !confirmPassword) {
      setFeedback('Completează toate câmpurile!');
      return;
    }

    if (password !== confirmPassword) {
      setFeedback('Parolele nu coincid!');
      return;
    }

    if (!validatePassword(password)) {
      setFeedback('Parola trebuie să conțină minim 5 caractere, o literă mare, un caracter special și o cifră.');
      return;
    }

    try {
      const response = await axios.post(`${API_URL}/api/user/active/`, {
        email,
        username,
        password
      });

      if (response.data.success) {
        setFeedback('Cont creat cu succes! Redirectare...');
        navigate('/login');
      } else {
        setFeedback(response.data.error || 'A apărut o eroare la creare.');
      }
    } catch (error) {
      setFeedback(error.response?.data?.error || 'Eroare de rețea sau server.');
    }
  };

  return (
    <div className="register-container">
      <div className="header">
        <button className="back-btn" onClick={() => navigate(-1)}>
          <img src="/back.png" alt="Inapoi" className="button-icon" />
        </button>
        <h1>Creare Cont</h1>
      </div>

      <div className="register-form-container">
        {!emailValid ? (
          <>
            <div className="input-group">
              <label>Email</label>
              <input
                type="email"
                placeholder="Introdu adresa de email a facultății"
                value={email}
                onChange={(e) => setEmail(e.target.value)}
              />
            </div>
            <button className="action-btn" onClick={handleCheckEmail}>Continuă</button>
          </>
        ) : (
          <>
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
              <label>Parolă</label>
              <input
                type="password"
                placeholder="Introdu parola"
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
            <button className="action-btn" onClick={handleCreateAccount}>Creează contul</button>
          </>
        )}
        {feedback && <div className="feedback">{feedback}</div>}
      </div>
    </div>
  );
};

export default RegisterPage;

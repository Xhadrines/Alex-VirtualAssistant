import React, { useState, useEffect, useRef } from 'react';
import { useNavigate } from 'react-router-dom';
import axios from 'axios';
import './ChatPage.css';

const API_URL = import.meta.env.VITE_CHAT_API;  // URL-ul API-ului pentru chat

const ChatPage = () => {
  const [messages, setMessages] = useState([]);  // Mesajele chat-ului
  const [inputMessage, setInputMessage] = useState('');  // Mesajul de la utilizator
  const [loading, setLoading] = useState(false);  // Starea de incarcare
  const [error, setError] = useState(null);  // Erori

  const messagesEndRef = useRef(null);  // Ref pentru a face scroll la ultimul mesaj
  const navigate = useNavigate();  // Hook pentru navigare

  // Functia pentru a trimite un mesaj
  const handleSendMessage = async () => {
    if (!inputMessage.trim() || loading) return;  // Verificam daca input-ul este gol sau se incarca deja un mesaj

    setMessages((prevMessages) => [...prevMessages, { text: inputMessage, sender: 'user' }]);
    setInputMessage('');
    setLoading(true);

    try {
      const response = await axios.post(`${API_URL}`, { message: inputMessage });  // Trimitem mesajul la API

      // Verificam daca am primit un raspuns valid
      if (response.data && response.data.answer) {
        setMessages((prevMessages) => [
          ...prevMessages,
          { text: response.data.answer, sender: 'bot' },
        ]);
      } else {
        setError("Raspuns invalid de la server. Te rog incearca din nou.");
      }
    } catch (error) {
      setError("Ceva a mers prost. Te rog incearca din nou.");
    } finally {
      setLoading(false);  // Incheiem incarcarea
    }
  };

  // Functia pentru a trimite mesaj la apasarea tastei Enter
  const handleKeyDown = (event) => {
    if (event.key === "Enter") {
      event.preventDefault();
      handleSendMessage();  // Trimite mesajul
    }
  };

  useEffect(() => {
    messagesEndRef.current?.scrollIntoView({ behavior: "smooth" });  // Scroll la ultimul mesaj
  }, [messages]);

  // Navigheaza catre pagina de acasa
  const navigateToHome = () => {
    navigate('/');  
  };

  return (
    <div className="chatpage-container">
      <div className="header">
        <button className="back-btn" onClick={navigateToHome}>
          <img src="/back.png" alt="Inapoi" className="button-icon" />
        </button>
        <h1>Alex - Asistent Virtual</h1>
        <button className="settings-btn" onClick={navigateToHome}>
          <img src="/settings.png" alt="Setari" className="button-icon" />
        </button>
      </div>

      <div className="chat-window">
        <div className="message-container">
          {/* Afisam toate mesajele */}
          {messages.map((message, index) => (
            <div
              key={index}
              className={`message ${message.sender === 'user' ? 'user-message' : 'bot-message'}`}
            >
              {message.text}
            </div>
          ))}

          {/* Mesaj de incarcare */}
          {loading && <div className="loading-message">Se genereaza raspunsul...</div>}
          {/* Mesaj de eroare */}
          {error && <div className="error-message">{error}</div>}

          {/* Ref pentru a face scroll la ultimul mesaj */}
          <div ref={messagesEndRef} />
        </div>
      </div>

      <div className="input-area">
        <input
          type="text"
          className="message-input"
          value={inputMessage}
          onChange={(e) => setInputMessage(e.target.value)}  // Actualizeaza mesajul de la utilizator
          onKeyDown={handleKeyDown}  // Trimite mesajul cu Enter
          placeholder="Scrie un mesaj..."
          disabled={loading}  // Dezactiveaza input-ul cand se incarca
        />

        <button className="send-btn" onClick={handleSendMessage} disabled={loading}>
          <img src="/send.png" alt="Trimite" className="send-icon" />
        </button>
      </div>
    </div>
  );
};

export default ChatPage;

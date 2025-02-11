import React, { useState, useEffect, useRef } from "react";
import axios from "axios";
import { useNavigate } from "react-router-dom";
import "./ChatWindow.css";

// URL-ul API-ului
const API_URL = import.meta.env.VITE_CHAT_API;

const ChatWindow = () => {
  // Starile componentelor pentru gestionarea deschiderii chat-ului, mesajelor, etc.
  const [isOpen, setIsOpen] = useState(false); // Chat-ul este deschis sau nu
  const [message, setMessage] = useState(""); // Mesajul introdus de utilizator
  const [chatMessages, setChatMessages] = useState([]); // Lista mesajelor
  const [loading, setLoading] = useState(false); // Starea de incarcare
  const [error, setError] = useState(null); // Erori, daca exista
  const [welcomeSent, setWelcomeSent] = useState(false); // Verifica daca mesajul de bun venit a fost trimis
  const messagesEndRef = useRef(null); // Referinta pentru a derula la ultimul mesaj
  const navigate = useNavigate(); // Pentru navigarea intre pagini

  // Functia care deschide si inchide chat-ul, si trimite mesajul de bun venit
  const toggleChat = async () => {
    setIsOpen(!isOpen); // Schimba starea chat-ului (deschis/inchis)

    if (!isOpen && !welcomeSent) {
      setLoading(true); // Activeaza incarcarea pentru mesajul de bun venit
      try {
        // Trimite cererea pentru a obtine mesajul de bun venit
        const response = await axios.post(`${API_URL}`, {
          message:
            "Generaza un mesaj scurt (maxim 50 de cuvinte) pentru student/viitor student/utilizator, dupa urmatorul template: mesajul de bun venit, cum te cheama, din ce facultate faci parte, si cu ce il poti ajuta.",
        });

        if (response.data?.answer) {
          setChatMessages([{ sender: "bot", text: response.data.answer }]); // Adauga mesajul de bun venit
          setWelcomeSent(true); // Marcheaza ca mesajul de bun venit a fost trimis
        } else {
          setError("Raspuns invalid de la server. Te rog incearca din nou."); // Mesaj de eroare daca nu exista raspuns
        }
      } catch {
        setError("Ceva a mers prost. Te rog incearca din nou."); // Mesaj de eroare la esecul cererii
      } finally {
        setLoading(false); // Inchide starea de incarcare
      }
    }
  };

  // Functia care trimite mesajul introdus de utilizator
  const sendMessage = async () => {
    if (!message.trim()) return; // Nu trimite mesaje goale

    setChatMessages([...chatMessages, { sender: "user", text: message }]); // Adauga mesajul utilizatorului
    setLoading(true); // Activeaza incarcarea
    setMessage(""); // Reseteaza campul de input

    try {
      const response = await axios.post(`${API_URL}`, { message }); // Trimite mesajul la API

      if (response.data?.answer) {
        // Adauga raspunsul bot-ului la mesaje
        setChatMessages((prevMessages) => [
          ...prevMessages,
          { sender: "bot", text: response.data.answer },
        ]);
      } else {
        setError("Raspuns invalid de la server. Te rog incearca din nou."); // Mesaj de eroare in caz de raspuns invalid
      }
    } catch {
      setError("Ceva a mers prost. Te rog incearca din nou."); // Mesaj de eroare in caz de esec
    } finally {
      setLoading(false); // Inchide incarcarea
    }
  };

  // Functie pentru a trimite mesajul cand se apasa tasta Enter
  const handleKeyDown = (e) => {
    if (e.key === "Enter") {
      e.preventDefault(); // Previne trimiterea formularului
      sendMessage(); // Trimite mesajul
    }
  };

  // Efect pentru a derula la ultimul mesaj din chat
  useEffect(() => {
    messagesEndRef.current?.scrollIntoView({ behavior: "smooth" });
  }, [chatMessages]); // Se executa de fiecare data cand lista de mesaje se modifica

  // Functie pentru a naviga spre o alta pagina (ex: chat complet)
  const navigateToChat = () => {
    navigate("/chat");
  };

  return (
    <div>
      {/* Butonul de deschidere a chat-ului */}
      {!isOpen && (
        <button className="chat-toggle-btn" onClick={toggleChat}>
          Alex - Asistent Virtual
        </button>
      )}

      {/* Chat-ul deschis */}
      {isOpen && (
        <div className={`chat-container ${isOpen ? "open" : ""}`}>
          <div className="chat-header">
            {/* Butonul pentru deschiderea unui chat mare */}
            <button className="chat-open" onClick={navigateToChat}>
              <img src="/new.png" alt="Deschide chat-ul mare" />
            </button>
            {/* Titlul chat-ului */}
            <span className="chat-title">Alex - Asistent Virtual</span>
            {/* Butonul pentru inchiderea chat-ului */}
            <button className="chat-close" onClick={toggleChat}>
              <img src="/close.png" alt="Inchide chat-ul" />
            </button>
          </div>
          <div className="chat-messages">
            {/* Mesajele din chat */}
            {chatMessages.map((msg, index) => (
              <div
                key={index}
                className={`chat-message ${msg.sender === "bot" ? "bot" : "user"}`}
              >
                {msg.text}
              </div>
            ))}
            {/* Mesajul de incarcare */}
            {loading && <div className="loading-message">Se genereaza raspunsul...</div>}
            {/* Mesajul de eroare */}
            {error && <div className="error-message">{error}</div>}
            {/* Referinta pentru derularea automata */}
            <div ref={messagesEndRef} />
          </div>
          <div className="chat-footer">
            {/* Campul de input pentru mesaje */}
            <input
              type="text"
              placeholder="Scrie un mesaj..."
              className="chat-input"
              value={message}
              onChange={(e) => setMessage(e.target.value)}
              onKeyDown={handleKeyDown}
              disabled={loading} // Dezactiveaza input-ul in timpul incarcarii
            />
            {/* Butonul de trimitere a mesajului */}
            <button className="chat-send-btn" onClick={sendMessage} disabled={loading}>
              <img src="/send.png" alt="Trimite mesajul" />
            </button>
          </div>
        </div>
      )}
    </div>
  );
};

export default ChatWindow;

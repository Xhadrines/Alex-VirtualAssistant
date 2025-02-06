import React, { useState, useEffect, useRef } from "react"; // Importam hook-urile React necesare
import axios from "axios"; // Importam axios pentru a face cereri HTTP catre server
import "./ChatWindow.css"; // Importam fisierul CSS pentru stilizarea componentelor

// Componenta principala ChatWindow
const ChatWindow = () => {
  // State-urile pentru gestionarea diferitelor aspecte ale chat-ului
  const [isOpen, setIsOpen] = useState(false); // Controlam daca fereastra de chat este deschisa sau nu
  const [message, setMessage] = useState(""); // Mesajul curent pe care utilizatorul il scrie
  const [chatMessages, setChatMessages] = useState([]); // Listeaza toate mesajele de chat
  const [loading, setLoading] = useState(false); // Starea de incarcare (pentru a arata un mesaj de "se genereaza raspunsul")
  const [error, setError] = useState(null); // Mesajul de eroare, daca apare vreo problema
  const [welcomeSent, setWelcomeSent] = useState(false); // Verifica daca mesajul de bun venit a fost trimis deja
  const messagesEndRef = useRef(null); // Folosit pentru a face scroll automat la ultimul mesaj

  // Functia care deschide sau inchide chat-ul
  const toggleChat = async () => {
    setIsOpen(!isOpen); // Schimbam starea de deschidere a chat-ului

    // Daca chat-ul nu este deschis si mesajul de bun venit nu a fost trimis
    if (!isOpen && !welcomeSent) {
      setLoading(true); // Setam starea de incarcare la true

      try {
        // Facem o cerere HTTP catre backend pentru a trimite mesajul de bun venit
        const response = await axios.post("http://127.0.0.1:8000/api/chat/", { message: "Salut, sunt asistentul tau virtual!" });

        // Daca raspunsul contine un mesaj valid, il adaugam la chat
        if (response.data && response.data.answer) {
          setChatMessages([{ sender: "bot", text: response.data.answer }]); // Adaugam mesajul botului
          setWelcomeSent(true); // Marcam mesajul de bun venit ca trimis
        } else {
          setError("Raspuns invalid de la server. Te rog incearca din nou."); // Setam eroarea daca raspunsul nu este valid
        }
      } catch (error) {
        setError("Ceva a mers prost. Te rog incearca din nou."); // Setam eroarea in cazul unui esec al cererii
      } finally {
        setLoading(false); // Oprim starea de incarcare
      }
    }
  };

  // Functia care trimite un mesaj
  const sendMessage = async () => {
    // Daca mesajul este gol, nu facem nimic
    if (!message.trim()) return;

    // Adaugam mesajul utilizatorului in lista de mesaje
    setChatMessages([...chatMessages, { sender: "user", text: message }]);
    setLoading(true); // Setam starea de incarcare
    setMessage(""); // Resetam campul de mesaj

    try {
      // Facem o cerere HTTP catre backend pentru a trimite mesajul utilizatorului
      const response = await axios.post("http://127.0.0.1:8000/api/chat/", { message });

      // Daca raspunsul contine un mesaj valid, il adaugam la chat
      if (response.data && response.data.answer) {
        setChatMessages((prevMessages) => [
          ...prevMessages, // Adaugam mesajele anterioare
          { sender: "bot", text: response.data.answer }, // Adaugam raspunsul botului
        ]);
      } else {
        setError("Raspuns invalid de la server. Te rog incearca din nou."); // Setam eroarea daca raspunsul nu este valid
      }
    } catch (error) {
      setError("Ceva a mers prost. Te rog incearca din nou."); // Setam eroarea in cazul unui esec al cererii
    } finally {
      setLoading(false); // Oprim starea de incarcare
    }
  };

  // Functia care asculta apasarea tastei Enter pentru trimiterea unui mesaj
  const handleKeyDown = (e) => {
    if (e.key === "Enter") {
      e.preventDefault(); // Prevenim comportamentul default al tastei Enter (de a trimite formularul)
      sendMessage(); // Trimitem mesajul
    }
  };

  // Folosim useEffect pentru a face scroll automat la ultimul mesaj
  useEffect(() => {
    messagesEndRef.current?.scrollIntoView({ behavior: "smooth" }); // Facem scroll automat la ultimul mesaj
  }, [chatMessages]); // Aceasta actiune se va executa ori de cate ori chatMessages se modifica

  return (
    <div>
      {/* Daca chat-ul nu este deschis, afisam un buton pentru a-l deschide */}
      {!isOpen && (
        <button className="chat-toggle-btn" onClick={toggleChat}>
          Alex - Asistent Virtual
        </button>
      )}

      {/* Daca chat-ul este deschis, afisam fereastra de chat */}
      {isOpen && (
        <div className={`chat-container ${isOpen ? "open" : ""}`}>
          <div className="chat-header">
            <span className="chat-title">Alex - Asistent Virtual</span>
            <button className="chat-close" onClick={toggleChat}>
              - {/* Butonul de inchidere a chat-ului */}
            </button>
          </div>
          <div className="chat-messages">
            {/* Afisam toate mesajele din chat */}
            {chatMessages.map((msg, index) => (
              <div key={index} className={`chat-message ${msg.sender === "bot" ? "bot" : "user"}`}>
                {msg.text}
              </div>
            ))}
            {/* Afisam mesajul de incarcare daca este activ */}
            {loading && <div className="loading-message">Se genereaza raspunsul...</div>}
            {/* Afisam mesajul de eroare, daca este cazul */}
            {error && <div className="error-message">{error}</div>}

            <div ref={messagesEndRef} /> {/* Referinta pentru a face scroll automat la ultimul mesaj */}
          </div>
          <div className="chat-footer">
            {/* Campul de input pentru a scrie mesajul */}
            <input
              type="text"
              placeholder="Scrie un mesaj..."
              className="chat-input"
              value={message}
              onChange={(e) => setMessage(e.target.value)} // Actualizam starea cu mesajul utilizatorului
              onKeyDown={handleKeyDown} // Ascultam pentru apasarea tastei Enter
              disabled={loading} // Dezactivam input-ul in timpul incarcarii
            />
            {/* Butonul pentru trimiterea mesajului */}
            <button
              className="chat-send-btn"
              onClick={sendMessage} // Trimitem mesajul
              disabled={loading} // Dezactivam butonul in timpul incarcarii
            >
              Send
            </button>
          </div>
        </div>
      )}
    </div>
  );
};

export default ChatWindow; // Exportam componenta pentru a o putea folosi in alte parti ale aplicatiei

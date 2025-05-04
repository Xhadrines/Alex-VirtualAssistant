import React, { useState, useEffect, useRef } from "react";
import axios from "axios";
import { useNavigate } from "react-router-dom";
import "./ChatWindow.css";

const API_URL = import.meta.env.VITE_CHAT_API;

const ChatWindow = () => {
    const [isOpen, setIsOpen] = useState(false);
    const [message, setMessage] = useState("");
    const [chatMessages, setChatMessages] = useState([]);
    const [loading, setLoading] = useState(false);
    const [error, setError] = useState(null);
    const [welcomeSent, setWelcomeSent] = useState(false);
    const messagesEndRef = useRef(null);
    const navigate = useNavigate();

    const toggleChat = async () => {
        setIsOpen(!isOpen);

        if (!isOpen && !welcomeSent) {
            setLoading(true);
            try {
                const response = await axios.post(`${API_URL}/api/conversation/chat/`, {
                    message: "Generaza un mesaj scurt (maxim 50 de cuvinte) pentru student/viitor student/utilizator, dupa urmatorul template: mesajul de bun venit, cum te cheama, din ce facultate faci parte, si cu ce il poti ajuta.",
                });

                if (response.data?.answer) {
                    setChatMessages([{ sender: "bot", text: response.data.answer }]);
                    setWelcomeSent(true);
                } else {
                    setError("Raspuns invalid de la server. Te rog incearca din nou.");
                }
            } catch {
                setError("Ceva a mers prost. Te rog incearca din nou.");
            } finally {
                setLoading(false);
            }
        }
    };

    const sendMessage = async () => {
        if (!message.trim()) 
            return;

        setChatMessages([...chatMessages, { sender: "user", text: message }]);
        setLoading(true);
        setMessage("");

        try {
            const response = await axios.post(`${API_URL}/api/conversation/chat/`, { message });

            if (response.data?.answer) {
                setChatMessages((prevMessages) => [ ...prevMessages, { sender: "bot", text: response.data.answer },]);
            } else {
                setError("Raspuns invalid de la server. Te rog incearca din nou.");
            }
        } catch {
            setError("Ceva a mers prost. Te rog incearca din nou.");
        } finally {
            setLoading(false);
        }
    };

    const handleKeyDown = (e) => {
        if (e.key === "Enter") {
            e.preventDefault();
            sendMessage()
        }
    };

    useEffect(() => {
        messagesEndRef.current?.scrollIntoView({ behavior: "smooth" });
    }, [chatMessages]);

    const navigateToChat = () => {
        navigate("/chat");
    };

    return (
        <div>
            {!isOpen && (<button className="chat-toggle-btn" onClick={toggleChat}>Alex - Asistent Virtual</button>)}
            
            {isOpen && (
                <div className={`chat-container ${isOpen ? "open" : ""}`}>
                    <div className="chat-header">
                        <button className="chat-open" onClick={navigateToChat}>
                            <img src="/new.png" alt="Deschide chat-ul mare" />
                        </button>
                        <span className="chat-title">Alex - Asistent Virtual</span>
                        <button className="chat-close" onClick={toggleChat}>
                            <img src="/close.png" alt="Inchide chat-ul" />
                        </button>
                    </div>
                    <div className="chat-messages">
                        {chatMessages.map((msg, index) => (
                            <div
                                key={index}
                                className={`chat-message ${msg.sender === "bot" ? "bot" : "user"}`}
                            >
                                {msg.text}
                            </div>
                        ))}
                        {loading && <div className="loading-message">Se genereaza raspunsul...</div>}
                        {error && <div className="error-message">{error}</div>}
                        <div ref={messagesEndRef} />
                    </div>
                    <div className="chat-footer">
                        <input
                        type="text"
                        placeholder="Scrie un mesaj..."
                        className="chat-input"
                        value={message}
                        onChange={(e) => setMessage(e.target.value)}
                        onKeyDown={handleKeyDown}
                        disabled={loading}
                        />
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

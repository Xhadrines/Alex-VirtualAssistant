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
          message:
            "Generaza un mesaj scurt (maxim 50 de cuvinte) pentru student/viitor student/utilizator, dupa urmatorul template: mesajul de bun venit, cum te cheama, din ce facultate faci parte, si cu ce il poti ajuta.",
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
    if (!message.trim()) return;

    setChatMessages([...chatMessages, { sender: "user", text: message }]);
    setLoading(true);
    setMessage("");

    try {
      const response = await axios.post(`${API_URL}/api/conversation/chat/`, {
        message,
      });

      if (response.data?.answer) {
        setChatMessages((prevMessages) => [
          ...prevMessages,
          { sender: "bot", text: response.data.answer },
        ]);
      } else {
        setError("Raspuns invalid de la server. Te rog incearca din nou.");
      }
    } catch {
      setError("Ceva a mers prost. Te rog incearca din nou.");
    } finally {
      setLoading(false);
    }
  };

  const formatAnswerText = (text) => {
    if (!text) return null;

    const lines = text.split("\n");
    let listItems = [];
    let olItems = [];
    const content = [];

    const olRegex = /^\d+\.\s+/;

    const parseInlineFormatting = (str) => {
      const elements = [];
      let lastIndex = 0;

      const combinedRegex =
        /(\*\*(.*?)\*\*)|(\*(?!\*)(.*?)\*)|(_(.*?)_)|(https?:\/\/[^\s]+)|(<sub>(.*?)<\/sub>)/g;

      let match;
      while ((match = combinedRegex.exec(str)) !== null) {
        if (match.index > lastIndex) {
          elements.push(str.slice(lastIndex, match.index));
        }

        if (match[1]) {
          elements.push(<strong key={match.index}>{match[2]}</strong>);
        } else if (match[3]) {
          elements.push(<em key={match.index}>{match[4]}</em>);
        } else if (match[5]) {
          elements.push(<em key={match.index}>{match[6]}</em>);
        } else if (match[7]) {
          elements.push(
            <a
              href={match[7]}
              target="_blank"
              rel="noopener noreferrer"
              key={match.index}
              style={{ color: "#4eaaff" }}
            >
              {match[7]}
            </a>
          );
        } else if (match[8]) {
          elements.push(<sub key={match.index}>{match[9]}</sub>);
        }

        lastIndex = combinedRegex.lastIndex;
      }

      if (lastIndex < str.length) {
        elements.push(str.slice(lastIndex));
      }

      return elements;
    };

    const flushList = () => {
      if (listItems.length > 0) {
        content.push(
          <ul key={`list-${content.length}`} style={{ paddingLeft: "20px" }}>
            {listItems}
          </ul>
        );
        listItems = [];
      }
      if (olItems.length > 0) {
        content.push(
          <ol key={`olist-${content.length}`} style={{ paddingLeft: "20px" }}>
            {olItems}
          </ol>
        );
        olItems = [];
      }
    };

    lines.forEach((line, index) => {
      if (/^\*\s+/.test(line)) {
        const itemText = line.replace(/^\*\s+/, "");
        listItems.push(
          <li key={`li-${index}`}>{parseInlineFormatting(itemText)}</li>
        );
      } else if (olRegex.test(line)) {
        const itemText = line.replace(olRegex, "");
        olItems.push(
          <li key={`oli-${index}`}>{parseInlineFormatting(itemText)}</li>
        );
      } else {
        flushList();
        content.push(
          <p key={`line-${index}`}>{parseInlineFormatting(line)}</p>
        );
      }
    });

    flushList();

    return content;
  };

  const handleKeyDown = (e) => {
    if (e.key === "Enter") {
      e.preventDefault();
      sendMessage();
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
      {!isOpen && (
        <button className="chat-toggle-btn" onClick={toggleChat}>
          Alex - Asistent Virtual
        </button>
      )}

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
                className={`chat-message ${
                  msg.sender === "bot" ? "bot" : "user"
                }`}
              >
                {formatAnswerText(msg.text)}
              </div>
            ))}
            {loading && (
              <div className="loading-message">Se genereaza raspunsul...</div>
            )}
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
            <button
              className="chat-send-btn"
              onClick={sendMessage}
              disabled={loading}
            >
              <img src="/send.png" alt="Trimite mesajul" />
            </button>
          </div>
        </div>
      )}
    </div>
  );
};

export default ChatWindow;

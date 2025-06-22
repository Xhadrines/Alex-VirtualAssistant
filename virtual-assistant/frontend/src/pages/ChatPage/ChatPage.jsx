import React, { useState, useEffect, useRef } from "react";
import { useNavigate } from "react-router-dom";
import axios from "axios";
import "./ChatPage.css";

const API_URL = import.meta.env.VITE_CHAT_API;

const ChatPage = () => {
  const [messages, setMessages] = useState([]);
  const [inputMessage, setInputMessage] = useState("");
  const [loading, setLoading] = useState(false);
  const [error, setError] = useState(null);
  const [isMenuOpen, setIsMenuOpen] = useState(false);
  const [user, setUser] = useState(null);

  const [isSuperuser, setIsSuperuser] = useState(false);
  const [isStaff, setIsStaff] = useState(false);

  const messagesEndRef = useRef(null);
  const navigate = useNavigate();

  useEffect(() => {
    const token = localStorage.getItem("token");
    const username = localStorage.getItem("username");
    const userId = localStorage.getItem("user_id");

    const superuserFlag = localStorage.getItem("is_superuser") === "true";
    const staffFlag = localStorage.getItem("is_staff") === "true";

    if (token && username && userId) {
      setUser({ username });
      setIsSuperuser(superuserFlag);
      setIsStaff(staffFlag);
      fetchConversationHistory(userId);
    } else {
      navigate("/login");
    }
  }, [navigate]);

  const fetchConversationHistory = async (userId) => {
    const token = localStorage.getItem("token");

    try {
      const response = await axios.get(
        `${API_URL}/api/conversation/history/filter/${userId}/`,
        {
          headers: {
            Authorization: `Bearer ${token}`,
          },
        }
      );

      if (response.data) {
        const historicalMessages = response.data
          .map((convo) => [
            { text: convo.question, sender: "user" },
            { text: convo.answer, sender: "bot" },
          ])
          .flat();

        setMessages(historicalMessages);
      }
    } catch (error) {
      console.error("Eroare la incarcarea istoricului conversatiei:", error);
      setError("Nu am reusit sa obtinem istoricul conversatiei.");
    }
  };

  const handleSendMessage = async () => {
    if (!inputMessage.trim() || loading) return;

    setMessages((prevMessages) => [
      ...prevMessages,
      { text: inputMessage, sender: "user" },
    ]);
    setInputMessage("");
    setLoading(true);

    try {
      const token = localStorage.getItem("token");

      const response = await axios.post(
        `${API_URL}/api/conversation/chat/`,
        { message: inputMessage },
        {
          headers: {
            Authorization: `Bearer ${token}`,
          },
        }
      );

      console.log("Response from chat API:", response.data);

      if (response.data && response.data.answer) {
        setMessages((prevMessages) => [
          ...prevMessages,
          { text: response.data.answer, sender: "bot" },
        ]);
      } else {
        setError("Raspuns invalid de la server. Te rog incearca din nou.");
      }
    } catch (error) {
      console.error("Error occurred while sending message:", error);
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

  const handleKeyDown = (event) => {
    if (event.key === "Enter") {
      event.preventDefault();
      handleSendMessage();
    }
  };

  useEffect(() => {
    messagesEndRef.current?.scrollIntoView({ behavior: "smooth" });
  }, [messages]);

  const toggleMenu = () => setIsMenuOpen(!isMenuOpen);

  const navigateToHome = () => {
    navigate("/");
  };

  const handleLogout = () => {
    localStorage.removeItem("token");
    localStorage.removeItem("username");
    localStorage.removeItem("user_id");
    setUser(null);
    navigate("/login");
  };

  const navigateToSettings = () => {
    navigate("/settings");
  };

  return (
    <div className="chatpage-container">
      <div className="header">
        <button className="back-btn" onClick={navigateToHome}>
          <img src="/back.png" alt="Inapoi" className="button-icon" />
        </button>
        <h1>Alex - Asistent Virtual</h1>
        {user ? (
          <div className={`user-menu ${isMenuOpen ? "open" : ""}`}>
            <button className="user-btn" onClick={toggleMenu}>
              <img src="/user.png" alt="User" className="button-icon" />
            </button>
            <div className="user-menu-dropdown">
              {(isSuperuser || isStaff) && (
                <button onClick={navigateToSettings}>
                  <img
                    src="/settings.png"
                    alt="Settings"
                    className="button-icon"
                  />{" "}
                  Setări
                </button>
              )}
              <button onClick={handleLogout}>
                <img src="/logout.png" alt="Logout" className="button-icon" />{" "}
                Deconectare
              </button>
            </div>
          </div>
        ) : (
          <button className="login-btn" onClick={() => navigate("/login")}>
            <img src="/login.png" alt="Login" className="button-icon" />
          </button>
        )}
      </div>
      <div className="chat-window">
        <div className="message-container">
          {messages.map((message, index) => (
            <div
              key={index}
              className={
                message.sender === "user" ? "user-message" : "bot-message"
              }
            >
              {formatAnswerText(message.text)}
            </div>
          ))}
          {loading && (
            <div className="loading-message">Se genereaza raspunsul...</div>
          )}
          {error && <div className="error-message">{error}</div>}
          <div ref={messagesEndRef} />
        </div>
      </div>
      <div className="input-area">
        <input
          type="text"
          className="message-input"
          value={inputMessage}
          onChange={(e) => setInputMessage(e.target.value)}
          onKeyDown={handleKeyDown}
          placeholder="Scrie un mesaj..."
          disabled={loading}
        />
        <button
          className="send-btn"
          onClick={handleSendMessage}
          disabled={loading}
        >
          <img src="/send.png" alt="Trimite" className="send-icon" />
        </button>
      </div>
    </div>
  );
};

export default ChatPage;

import React, { useState, useEffect } from 'react';
import './SettingsPage.css';

const API_URL = import.meta.env.VITE_CHAT_API;

const SettingsPage = () => {
  const [file, setFile] = useState(null);

  const [loading, setLoading] = useState(false);
  const [elapsedTime, setElapsedTime] = useState(0);
  const [showContinue, setShowContinue] = useState(false);

  const handleFileChange = (e) => {
    setFile(e.target.files[0]);
  };

  const handleUpload = async () => {
    if (!file) {
      alert('Te rog să selectezi un fișier.');
      return;
    }

    const formData = new FormData();
    formData.append('file', file);

    try {
      const token = localStorage.getItem('token');

      const response = await fetch(`${API_URL}/api/user/import/`, {
        method: 'POST',
        headers: {
          Authorization: token ? `Token ${token}` : '',
        },
        body: formData,
      });

      if (!response.ok) {
        const error = await response.json();
        alert(`Eroare: ${error.error || 'Serverul a returnat o eroare'}`);
        return;
      }

      const data = await response.json();
      alert(`Succes: ${data.message}`);
      setFile(null);
    } catch (err) {
      alert('A apărut o eroare la încărcare.');
      console.error(err);
    }
  };

  useEffect(() => {
    let timer;
    if (loading) {
      timer = setInterval(() => {
        setElapsedTime((prev) => prev + 1);
      }, 1000);
    } else {
      clearInterval(timer);
      setElapsedTime(0);
    }
    return () => clearInterval(timer);
  }, [loading]);

  const handleUpdateFiles = async () => {
    setLoading(true);
    setElapsedTime(0);
    try {
      const token = localStorage.getItem('token');
      console.log('Trimitem request pentru actualizare fisiere...');

      const response = await fetch(`${API_URL}/api/download/files/`, {
        method: 'POST',
        headers: {
          'Content-Type': 'application/json',
          Authorization: token ? `Token ${token}` : '',
        },
        body: JSON.stringify({}),
      });

      console.log('Raspuns status:', response.status);
      const data = await response.json();
      console.log('Raspuns data:', data);

      if (!response.ok) {
        alert(`Eroare: ${data.message || 'Serverul a returnat o eroare'}`);
        setLoading(false);
        return;
      }

      alert(`Succes: ${data.message}`);
    } catch (err) {
      alert('A apărut o eroare la actualizarea fișierelor.');
      console.error(err);
    } finally {
      setLoading(false);
    }
  };


  return (
    <>
      {loading && (
        <div className="loading-overlay">
          <div className="spinner-container">
            <div className="spinner-bg"></div>
            <div className="spinner-fg"></div>
            <div className="spinner-text">
              Așteptați...<br />
              Timp trecut: {elapsedTime} s
            </div>
          </div>
        </div>
      )}

      <div className="settings-container">
        <div className="header">
          <button className="back-btn" onClick={() => window.history.back()}>
            <img src="/back.png" alt="Înapoi" className="button-icon" />
          </button>
          <h1>Setări</h1>
        </div>

        <form className="settings-form" onSubmit={(e) => e.preventDefault()}>
          <div className="input-group">
            <label>Selectează fișierul Excel</label>
            <input
              type="file"
              accept=".xlsx, .xls"
              onChange={handleFileChange}
            />
          </div>
          <button
            className="settings-btn"
            type="button"
            onClick={handleUpload}
            disabled={!file}
          >
            Încarcă
          </button>

          <button
            className="settings-btn"
            type="button"
            onClick={handleUpdateFiles}
            style={{ marginTop: '20px' }}
          >
            Actualizare fișiere
          </button>
        </form>
      </div>
    </>
  );
};

export default SettingsPage;

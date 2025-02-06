// Importa componenta Frame si ChatWindow, precum si fisierul CSS asociat
import React from 'react';
import Frame from "../../components/Frame/Frame"; // Componenta care incarca un iframe
import ChatWindow from "../../components/ChatWindow/ChatWindow"; // Componenta pentru fereastra de chat
import "./Home.css"; // Fisierul CSS pentru stilizarea paginii Home

// Definirea componentei Home
const Home = () => {
  return (
    // Containerul principal al paginii Home care contine atat iframe-ul, cat si fereastra de chat
    <div className="home-container">
      {/* Inserarea componentei Frame care incarca iframe-ul */}
      <Frame />
      {/* Inserarea componentei ChatWindow care reprezinta fereastra de chat */}
      <ChatWindow />
    </div>
  );
};

// Exporta componenta Home pentru a fi utilizata in alte parti ale aplicatiei
export default Home;

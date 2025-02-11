import { BrowserRouter as Router, Route, Routes } from 'react-router-dom';
import Home from "../pages/Home/Home";
import ChatPage from "../pages/ChatPage/ChatPage";

// Componenta principala a aplicatiei
function App() {
  return (
    <Router>
      <Routes>
        {/* Ruta pentru pagina principala (Home) */}
        <Route path="/" element={<Home />} />
        
        {/* Ruta pentru pagina de chat */}
        <Route path="/chat" element={<ChatPage />} />
      </Routes>
    </Router>
  );
}

export default App;

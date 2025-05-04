import { BrowserRouter as Router, Route, Routes } from 'react-router-dom';
import Home from '../pages/Home/Home';
import ChatPage from '../pages/ChatPage/ChatPage';
import LoginPage from '../pages/LoginPage/LoginPage';
import SettingsPage from '../pages/SettingsPage/SettingsPage';

function App() {
  return (
    <Router>
      <Routes>
        <Route path="/" element={<Home />} />

        <Route path="/chat" element={<ChatPage />} />

        <Route path="/login" element={<LoginPage />} />

        <Route path="/settings" element={<SettingsPage />} />
      </Routes>
    </Router>
  );
}

export default App;

import { BrowserRouter as Router, Route, Routes } from "react-router-dom";
import Home from "../pages/Home/Home";
import ChatPage from "../pages/ChatPage/ChatPage";
import LoginPage from "../pages/LoginPage/LoginPage";
import RegisterPage from "../pages/RegisterPage/RegisterPage";
import RegisterConfirmPage from "../pages/RegisterConfirmPage/RegisterConfirmPage";
import ResetPasswordPage from "../pages/ResetPasswordPage/ResetPasswordPage";
import ResetPasswordConfirmPage from "../pages/ResetPasswordConfirmPage/ResetPasswordConfirmPage";
import SettingsPage from "../pages/SettingsPage/SettingsPage";

function App() {
  return (
    <Router>
      <Routes>
        <Route path="/" element={<Home />} />

        <Route path="/chat" element={<ChatPage />} />

        <Route path="/login" element={<LoginPage />} />

        <Route path="/register" element={<RegisterPage />} />

        <Route path="/register-confirm" element={<RegisterConfirmPage />} />

        <Route path="/reset-password" element={<ResetPasswordPage />} />

        <Route
          path="/reset-password-confirm"
          element={<ResetPasswordConfirmPage />}
        />

        <Route path="/settings" element={<SettingsPage />} />
      </Routes>
    </Router>
  );
}

export default App;

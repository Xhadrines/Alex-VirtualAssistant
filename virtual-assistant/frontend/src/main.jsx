import { StrictMode } from "react";
import { createRoot } from "react-dom/client";
import "./index.css";
import App from "./App/App";

// Creaza si renderizeaza aplicatia React in elementul cu id-ul "root"
createRoot(document.getElementById("root")).render(
  <StrictMode>  {/* Activeaza verificari suplimentare pentru dezvoltare */}
    <App />  {/* Afiseaza aplicatia principala */}
  </StrictMode>
);

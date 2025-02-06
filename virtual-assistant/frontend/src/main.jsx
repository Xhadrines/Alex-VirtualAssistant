import { StrictMode } from "react"; // Importa StrictMode din React pentru a activa modurile stricte de dezvoltare
import { createRoot } from "react-dom/client"; // Importa createRoot pentru a crea un container pentru aplicatie in DOM
import "./index.css"; // Importa fisierul CSS global pentru stilizarea aplicatiei
import App from "./App/App"; // Importa componenta principala a aplicatiei

// Creaza un container root in DOM si randaza aplicatia in interiorul acestuia
createRoot(document.getElementById("root")).render(
  <StrictMode> 
    {/* Aici se renderizeaza aplicatia in modul StrictMode pentru verificari suplimentare in dezvoltare */}
    <App />
  </StrictMode>
);

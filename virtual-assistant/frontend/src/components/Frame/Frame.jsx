// Importa fisierul CSS pentru stilizare
import "./Frame.css";

// Definirea componentului Frame
const Frame = () => {
  return (
    // Creaza un iframe care incarca pagina dorita
    <iframe 
      src="https://fiesc.usv.ro/?r" // Seteaza sursa iframe-ului (pagina web care va fi incarcata)
      title="FIESC USV" // Atribuie un titlu pentru iframe
      className="iframe-container" // Atribuie clasa CSS pentru stilizare
    />
  );
};

// Exporta componenta Frame pentru a putea fi utilizata in alte fisiere
export default Frame;

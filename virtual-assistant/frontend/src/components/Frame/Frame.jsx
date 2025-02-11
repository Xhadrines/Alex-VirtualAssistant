import "./Frame.css";

// Componentea care incarca un iframe cu un URL specific
const Frame = () => {
  return (
    <iframe 
      src="https://fiesc.usv.ro/?r"  // URL-ul sursei iframe-ului
      title="FIESC USV"  // Titlul iframe-ului pentru accesibilitate
      className="iframe-container"  // Clasa CSS pentru stilizare
    />
  );
};

export default Frame;

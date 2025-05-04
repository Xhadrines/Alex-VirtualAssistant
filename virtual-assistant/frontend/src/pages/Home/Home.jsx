import React from 'react';
import Frame from '../../components/Frame/Frame';
import ChatWindow from '../../components/ChatWindow/ChatWindow';
import "./Home.css";

const Home = () => {
    return (
        <div className="home-container">
            <Frame />
            <ChatWindow />
        </div>
    );
};

export default Home;

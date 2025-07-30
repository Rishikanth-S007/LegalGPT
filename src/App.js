import React from 'react';
import { BrowserRouter as Router, Routes, Route } from 'react-router-dom';
import ServiceSelection from './components/ServiceSelection';
import ChatInterface from './components/ChatInterface';

function App() {
  return (
    <Router>
      <Routes>
        <Route path="/" element={<ServiceSelection />} />
        <Route path="/local-law" element={<ChatInterface serviceType="lawTeller" />} />
        <Route path="/scholarship" element={<ChatInterface serviceType="scholarship" />} />
      </Routes>
    </Router>
  );
}

export default App;

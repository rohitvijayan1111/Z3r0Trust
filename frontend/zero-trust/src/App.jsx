import { useState } from 'react'
import './App.css'
import { GlobeDemo } from './components/Home/LandingPage'
import './index.css'
import { Route, Router, Routes } from 'react-router-dom';
import { FloatingMessages } from './components/Home/FloatingMessages';

function App() {
  return (
    <>
      <Routes>
        <Route path="/" element={<GlobeDemo />} />
        <Route path="/test" element={<FloatingMessages />} />
      </Routes>
    </>
  );
}

export default App

import { useState } from 'react'
import './App.css'
import { GlobeDemo } from './components/Home/LandingPage'
import './index.css'
import { Route, Router, Routes } from 'react-router-dom';

function App() {
  return (
    <>
      <Routes>
        <Route path="/" element={<GlobeDemo />} />
      </Routes>
    </>
  );
}

export default App

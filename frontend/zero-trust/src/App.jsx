import { useState } from 'react'
import './App.css'
import { GlobeDemo } from './components/Home/LandingPage'
import './index.css'
import { Route, Router, Routes } from 'react-router-dom';
import { FloatingMessages } from './components/Home/FloatingMessages';
import { SignupFormDemo } from './components/Auth/SignupFormDemo';
import { EvervaultCardDemo } from './components/Dashboard/EvervaultCardDemo';
import { AlertsPage } from './components/Dashboard/AlertsPage';
import ResponsesPage from './components/Dashboard/ResponsesPage';
import { SignupFormDemo1 } from './components/Signup and Login/SignupFormDemo';

function App() {
  return (
    <>
      <Routes>
        <Route path="/" element={<GlobeDemo />} />
        <Route path="/userAuth" element={<SignupFormDemo />} />
        <Route path="/dashboard" element={<EvervaultCardDemo />} />
        <Route path="/alerts" element={<AlertsPage />} />
        <Route path="/responses" element={<ResponsesPage />} />
        <Route path="/auth" element={<SignupFormDemo1 />} />
      </Routes>
    </>
  );
}

export default App

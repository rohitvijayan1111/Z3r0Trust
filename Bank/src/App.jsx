import { useState } from 'react'
import reactLogo from './assets/react.svg'
import viteLogo from '/vite.svg'
import './App.css'
import { Route, Router, Routes } from "react-router-dom";
import { SignupFormDemo1 } from './components/Signup and Login/SignupFormDemo';
import { UserDashboard } from './components/Dashboard/UserDashboard';
import { DataDownload } from './components/DataDownload/DataDownload';
import { AdminPanel } from './components/Admin/AdminPanel';
import { FundTransfer } from './components/Fund Transfer/FundTransfer';
import { InternalUserPanel } from './components/InternalUserPanel';
import { MFAEnforcement } from './components/MFAEnforcement';
import { NetworkAnomalySimulation } from './components/NetworkAnomalySimulation';
import { SuspiciousApiPlayground } from './components/SuspiciousApiPlayground';

function App() {
  const [count, setCount] = useState(0)

  return (
    <>
      <Routes>
        <Route path="/" element={<SignupFormDemo1/>} />
        <Route path="/dashboard" element={<UserDashboard/>} />
        <Route path="/dataDownload" element={<DataDownload/>} />
        <Route path="/admin" element={<AdminPanel/>} />
        <Route path="/fund" element={<FundTransfer/>} />
        <Route path="/userpanel" element={<InternalUserPanel/>} />
        <Route path="/mfa" element={<MFAEnforcement/>} />
        <Route path="/network" element={<NetworkAnomalySimulation/>} />
        <Route path="/suspicious" element={<SuspiciousApiPlayground/>} />
       

      </Routes>
    </>

  )
}

export default App

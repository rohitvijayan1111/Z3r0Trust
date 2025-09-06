import { useState } from 'react'
import reactLogo from './assets/react.svg'
import viteLogo from '/vite.svg'
import './App.css'
import { Route, Router, Routes } from "react-router-dom";
import { SignupFormDemo1 } from './components/Signup and Login/SignupFormDemo';
import { UserDashboard } from './components/Dashboard/UserDashboard';

function App() {
  const [count, setCount] = useState(0)

  return (
    <>
      <Routes>
        <Route path="/" element={<SignupFormDemo1/>} />
        <Route path="/dashboard" element={<UserDashboard/>} />

      </Routes>
    </>

  )
}

export default App

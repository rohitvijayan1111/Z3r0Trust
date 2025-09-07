import { useState } from "react";
import "./App.css";
import { GlobeDemo } from "./components/Home/LandingPage";
import "./index.css";
import { Route, Router, Routes } from "react-router-dom";
import { SignupFormDemo } from "./components/Auth/SignupFormDemo";
import { EvervaultCardDemo } from "./components/Dashboard/EvervaultCardDemo";
import { AlertsPage } from "./components/Dashboard/AlertsPage";
import ResponsesPage from "./components/Dashboard/ResponsesPage";
import { SignupFormDemo1 } from "./components/Signup and Login/SignupFormDemo";
import { FeaturesSectionDemo } from "./components/Attack/FeaturesSectionDemo";
import { AppealPage } from "./components/Dashboard/AppealPage";
import { ApiIntegrationForm } from "./components/third-party/ApiIntegrationForm";
import { IntegrationSidebar } from "./components/third-party/IntegrationSidebar";

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
        <Route path="/beginAttack" element={<FeaturesSectionDemo />} />
        <Route path="/appeal" element={<AppealPage />} />
        <Route path="/integrateApi" element={<IntegrationSidebar />} />
      </Routes>
    </>
  );
}

export default App;

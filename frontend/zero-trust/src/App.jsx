import "./App.css";
import { GlobeDemo } from "./components/Home/LandingPage";
import "./index.css";
import { Route, Routes } from "react-router-dom";
import { SignupFormDemo } from "./components/Auth/SignupFormDemo";
import { EvervaultCardDemo } from "./components/Dashboard/EvervaultCardDemo";
import { AlertsPage } from "./components/Dashboard/AlertsPage";
import ResponsesPage from "./components/Dashboard/ResponsesPage";
import { SignupFormDemo1 } from "./components/Signup and Login/SignupFormDemo";
import { FeaturesSectionDemo } from "./components/Attack/FeaturesSectionDemo";
import { AppealPage } from "./components/Dashboard/AppealPage";
import { IntegrationSidebar } from "./components/third-party/IntegrationSidebar";
import { TeamSection } from "./components/Developers_Profile/TeamSection";

function App() {
  return (
    <>
      <Routes>
        <Route path="/" element={<GlobeDemo />} />
        <Route path="/userAuth" element={<SignupFormDemo />} />
        <Route path="/dashboard" element={<EvervaultCardDemo />} />
        <Route path="/alerts" element={<AlertsPage />} />
        <Route path="/auth" element={<SignupFormDemo1 />} />
        <Route path="/beginAttack" element={<FeaturesSectionDemo />} />
        <Route path="/appeal" element={<AppealPage />} />
        <Route path="/integrateApi" element={<IntegrationSidebar />} />
        <Route path="/team" element={<TeamSection />} />
      </Routes>
    </>
  );
}

export default App;

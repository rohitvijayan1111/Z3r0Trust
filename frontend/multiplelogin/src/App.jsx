import React, { useState, useEffect } from "react";
import "bootstrap/dist/css/bootstrap.min.css";

function App() {
  const [mode, setMode] = useState("manual"); // "manual" | "auto"
  const [email, setEmail] = useState("");
  const [password, setPassword] = useState("");
  const [requestType, setRequestType] = useState("login");
  const [result, setResult] = useState(null);
  const [loading, setLoading] = useState(false);
  const [logs, setLogs] = useState([]);
  const [currentIndex, setCurrentIndex] = useState(0);

  // Test credentials for auto-login loop
  const credentials = [
    { email: "test1@example.com", password: "Password123" },
    { email: "diva22022.it@rmkec.ac.in", password: "123qwe!@#QWE" },
    { email: "test2@example.com", password: "MySecret789" },
    { email: "test3@example.com", password: "12345678Rr@" },
  ];

  // Common login function (manual + auto)
  const loginRequest = async (email, password) => {
    try {
      const response = await fetch("http://127.0.0.1:8000/login-with-email", {
        method: "POST",
        headers: { "Content-Type": "application/json" },
        body: JSON.stringify({ email, password, request_type: requestType }),
      });
      return await response.json();
    } catch (error) {
      return { status: "failure", message: error.message };
    }
  };

  // Manual submit
  const handleSubmit = async (e) => {
    e.preventDefault();
    setLoading(true);
    setResult(null);

    const data = await loginRequest(email, password);
    setResult(data);

    setLoading(false);
  };

  // Auto login loop
  useEffect(() => {
    if (mode === "auto") {
      const cred = credentials[currentIndex];
      loginRequest(cred.email, cred.password).then((res) => {
        setLogs((prev) => [...prev, { email: cred.email, response: res }]);
      });

      const timer = setTimeout(() => {
        setCurrentIndex((prev) => (prev + 1) % credentials.length);
      }, 3000);

      return () => clearTimeout(timer);
    }
  }, [mode, currentIndex]);

  return (
    <div className="container mt-5" style={{ maxWidth: "600px" }}>
      <h2 className="mb-4 text-center">Login Portal</h2>

      {/* Mode Selector */}
      <div className="d-flex justify-content-center mb-3">
        <div className="btn-group">
          <button
            className={`btn btn-${mode === "manual" ? "primary" : "outline-primary"}`}
            onClick={() => setMode("manual")}
          >
            Manual Login
          </button>
          <button
            className={`btn btn-${mode === "auto" ? "primary" : "outline-primary"}`}
            onClick={() => setMode("auto")}
          >
            Auto Login Loop
          </button>
        </div>
      </div>

      {mode === "manual" ? (
        <>
          {/* Manual Form */}
          <form onSubmit={handleSubmit} className="card p-4 shadow-sm">
            <div className="mb-3">
              <label className="form-label">Email address</label>
              <input
                type="email"
                className="form-control"
                value={email}
                onChange={(e) => setEmail(e.target.value)}
                placeholder="Enter your email"
                required
              />
            </div>
            <div className="mb-3">
              <label className="form-label">Password</label>
              <input
                type="password"
                className="form-control"
                value={password}
                onChange={(e) => setPassword(e.target.value)}
                placeholder="Enter your password"
                required
              />
            </div>
            <button type="submit" className="btn btn-primary w-100" disabled={loading}>
              {loading ? "Logging in..." : "Login"}
            </button>
          </form>

          {result && (
            <div className="card mt-4 p-3">
              <h5>Response</h5>
              <pre style={{ fontSize: "0.9rem" }}>
                {JSON.stringify(result, null, 2)}
              </pre>
            </div>
          )}
        </>
      ) : (
        <>
          {/* Auto Login Logs */}
          <div className="card p-3 shadow-sm">
            <h5>Auto Login Logs</h5>
            <p className="text-muted">Cycling through {credentials.length} test accounts...</p>
            <div style={{ maxHeight: "400px", overflowY: "auto" }}>
              {logs.map((log, idx) => (
                <div key={idx} className="card mb-2">
                  <div className="card-body">
                    <strong>{log.email}</strong>
                    <pre style={{ fontSize: "0.8rem" }}>
                      {JSON.stringify(log.response, null, 2)}
                    </pre>
                  </div>
                </div>
              ))}
            </div>
          </div>
        </>
      )}
    </div>
  );
}

export default App;

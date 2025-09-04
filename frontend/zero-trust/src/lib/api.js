const API_BASE = "http://127.0.0.1:5000/api/auth";

export const signupUser = async (userData) => {
  try {
    const res = await fetch(`${API_BASE}/signup`, {
      method: "POST",
      headers: { "Content-Type": "application/json" },
      body: JSON.stringify(userData),
    });
    return await res.json();
  } catch (err) {
    console.error("Signup error:", err);
    return { message: "Failed to connect to backend" };
  }
};

export const loginUser = async (credentials) => {
  try {
    const res = await fetch(`${API_BASE}/login`, {
      method: "POST",
      headers: { "Content-Type": "application/json" },
      body: JSON.stringify(credentials),
    });
    return await res.json();
  } catch (err) {
    console.error("Login error:", err);
    return { message: "Failed to connect to backend" };
  }
};

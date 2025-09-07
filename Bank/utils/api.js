export const apiFetch = async (url, options = {}) => {
  const sessionKey = localStorage.getItem("session_jwt");

  const headers = {
    ...(options.headers || {}),
    "Content-Type": "application/json",
    "X-Session-Key": sessionKey,
  };

  return fetch(url, {
    ...options,
    headers,
  });
};

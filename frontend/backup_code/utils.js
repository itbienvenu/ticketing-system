// utils.js
export function isTokenValid(token) {
  if (!token) return false;

  try {
    // JWT structure: header.payload.signature
    const payload = JSON.parse(atob(token.split('.')[1]));
    const exp = payload.exp; // expiration time in seconds

    if (!exp) return false;

    const currentTime = Math.floor(Date.now() / 1000); // cu
    return currentTime < exp;
  } catch (err) {
    console.error("Invalid token", err);
    return false;
  }
}

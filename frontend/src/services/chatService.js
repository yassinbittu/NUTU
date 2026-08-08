const configuredApiUrl = import.meta.env.VITE_API_BASE_URL?.trim();

// Vite exposes VITE_* variables at build time. A production frontend must
// set this to its public HTTPS backend URL before it is built.
export const API_BASE_URL = configuredApiUrl?.replace(/\/$/, "");
const REQUEST_TIMEOUT_MS = 45_000;

const getApiUrl = (path) => {
  if (!API_BASE_URL) {
    throw new Error("NUTU is not configured with an API URL. Set VITE_API_BASE_URL and redeploy.");
  }

  if (import.meta.env.PROD && !API_BASE_URL.startsWith("https://")) {
    throw new Error("NUTU needs an HTTPS API URL in production. Update VITE_API_BASE_URL and redeploy.");
  }

  return `${API_BASE_URL}${path}`;
};

export const sendChatMessage = async (message) => {
  const controller = new AbortController();
  const timeout = window.setTimeout(() => controller.abort(), REQUEST_TIMEOUT_MS);

  try {
    const response = await fetch(getApiUrl("/chat"), {
      method: "POST",
      headers: {
        "Content-Type": "application/json",
      },
      body: JSON.stringify({ message }),
      signal: controller.signal,
    });

    if (!response.ok) {
      throw new Error(`NUTU API returned ${response.status}`);
    }

    return await response.json();
  } catch (error) {
    if (error.name === "AbortError") {
      throw new Error(
        "NUTU took too long to respond. Please try again.",
        { cause: error }
      );
    }

    throw error;
  } finally {
    window.clearTimeout(timeout);
  }
};


// Convert backend relative URLs into complete URLs
export const getFileUrl = (url) => {
  if (!url) {
    return null;
  }

  // If backend already sends a complete URL
  if (
    url.startsWith("http://") ||
    url.startsWith("https://")
  ) {
    return url;
  }

  return getApiUrl(url);
};


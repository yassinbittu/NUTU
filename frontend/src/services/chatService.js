export const API_BASE_URL = "http://127.0.0.1:8000";


export const sendChatMessage = async (message) => {
  const response = await fetch(`${API_BASE_URL}/chat`, {
    method: "POST",

    headers: {
      "Content-Type": "application/json",
    },

    body: JSON.stringify({
      message: message,
    }),
  });


  if (!response.ok) {
    throw new Error("Failed to get response from NUTU");
  }


  const data = await response.json();

  return data;
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

  return `${API_BASE_URL}${url}`;
};


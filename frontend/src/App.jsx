import { useState } from "react";

import Header from "./components/Header";
import ChatWindow from "./components/ChatWindow";
import ChatInput from "./components/ChatInput";

import { sendChatMessage } from "./services/chatService";


function App() {
  const [messages, setMessages] = useState([
    {
      role: "assistant",
      content:
        "Hi! I'm NUTU. Ask me anything about Mohammed Yassin.",
    },
  ]);

  const [isLoading, setIsLoading] = useState(false);


  const handleSend = async (message) => {

    // User message
    const userMessage = {
      role: "user",
      content: message,
    };


    // Immediately show user message
    setMessages((previousMessages) => [
      ...previousMessages,
      userMessage,
    ]);


    // Start loading
    setIsLoading(true);


    try {

      // Send message to FastAPI
      const response = await sendChatMessage(
        message
      );


      // NUTU response
      const assistantMessage = {
        role: "assistant",
        content: response.answer,
        type: response.type,
        action: response.action,
      };


      // Add NUTU response
      setMessages((previousMessages) => [
        ...previousMessages,
        assistantMessage,
      ]);

    } catch (error) {

      console.error(error);


      const errorMessage = {
        role: "assistant",
        content:
          "Sorry, I'm having trouble connecting right now. Please try again.",
        type: "error",
      };


      setMessages((previousMessages) => [
        ...previousMessages,
        errorMessage,
      ]);

    } finally {

      setIsLoading(false);

    }
  };


  return (
    <div className="flex h-screen flex-col bg-slate-950 text-white">

      <Header />

      <ChatWindow
        messages={messages}
        isLoading={isLoading}
      />

      <ChatInput
        onSend={handleSend}
        isLoading={isLoading}
      />

    </div>
  );
}


export default App;
import { useEffect, useState } from "react";

import Header from "./components/Header";
import ChatWindow from "./components/ChatWindow";
import ChatInput from "./components/ChatInput";
import AppLoader from "./components/AppLoader";
import { sendChatMessage } from "./services/chatService";
import { speakText, stopSpeaking } from "./services/voiceService";


function App() {
  const [appLoading, setAppLoading] = useState(true);
  const [messages, setMessages] = useState([
    {
      role: "assistant",
      content: "Hi! I'm NUTU. Ask me anything about Mohammed Yassin.",
      action: {
        suggestions: [
          { label: "Show resume", message: "Show resume" },
          { label: "Tell me about experience", message: "Tell me about experience" },
          { label: "List projects", message: "List projects" },
          { label: "What are his skills?", message: "What are his skills?" },
          { label: "Contact information", message: "Contact information", variant: "secondary" },
        ],
      },
    },
  ]);
  const [isLoading, setIsLoading] = useState(false);
  const [voiceState, setVoiceState] = useState("idle");
  const [voiceRestart, setVoiceRestart] = useState(0);

  useEffect(() => {
    const timer = setTimeout(() => setAppLoading(false), 1800);
    return () => clearTimeout(timer);
  }, []);

  const handleSend = async (message, isVoice = false) => {
    if (!message.trim() || isLoading) return;

    setMessages((previousMessages) => [
      ...previousMessages,
      { role: "user", content: message },
    ]);
    setIsLoading(true);

    if (isVoice) setVoiceState("thinking");

    try {
      const response = await sendChatMessage(message);
      setMessages((previousMessages) => [
        ...previousMessages,
        {
          role: "assistant",
          content: response.answer,
          type: response.type,
          action: response.action,
        },
      ]);

      if (isVoice && response.answer) {
        setVoiceState("speaking");
        speakText(response.answer, () => {
          setVoiceState("listening");
          setVoiceRestart((previous) => previous + 1);
        });
      }
    } catch (error) {
      console.error(error);
      setMessages((previousMessages) => [
        ...previousMessages,
        {
          role: "assistant",
          content: error.message || "Sorry, I'm having trouble connecting right now. Please try again.",
          type: "error",
        },
      ]);

      if (isVoice) {
        setVoiceState("speaking");
        speakText("Sorry, I'm having trouble connecting right now.", () => {
          setVoiceState("listening");
          setVoiceRestart((previous) => previous + 1);
        });
      }
    } finally {
      setIsLoading(false);
    }
  };

  const handleEndVoice = () => {
    stopSpeaking();
    setVoiceState("idle");
  };

  if (appLoading) return <AppLoader />;

  return (
    <div className="flex h-screen flex-col bg-slate-950 text-white">
      <Header />
      <ChatWindow
        messages={messages}
        isLoading={isLoading}
        onQuickReply={(message) => handleSend(message)}
      />
      <ChatInput
        onSend={handleSend}
        isLoading={isLoading}
        voiceState={voiceState}
        setVoiceState={setVoiceState}
        voiceRestart={voiceRestart}
        onEndVoice={handleEndVoice}
      />
    </div>
  );
}


export default App;

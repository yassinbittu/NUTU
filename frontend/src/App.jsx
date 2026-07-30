import { useEffect, useState } from "react";

import Header from "./components/Header";
import ChatWindow from "./components/ChatWindow";
import ChatInput from "./components/ChatInput";
import AppLoader from "./components/AppLoader";

import { sendChatMessage } from "./services/chatService";

import {
  speakText,
  stopSpeaking,
} from "./services/voiceService";


function App() {

  // -----------------------------------------
  // APP LOADING SCREEN
  // -----------------------------------------

  const [appLoading, setAppLoading] =
    useState(true);


  // -----------------------------------------
  // CHAT MESSAGES
  // -----------------------------------------

  const [messages, setMessages] = useState([
    {
      role: "assistant",
      content:
        "Hi! I'm NUTU. Ask me anything about Mohammed Yassin.",
    },
  ]);


  // -----------------------------------------
  // CHAT LOADING
  // -----------------------------------------

  const [isLoading, setIsLoading] =
    useState(false);


  // -----------------------------------------
  // VOICE STATE
  //
  // idle
  // listening
  // thinking
  // speaking
  // -----------------------------------------

  const [voiceState, setVoiceState] =
    useState("idle");


  // -----------------------------------------
  // Used to restart microphone automatically
  // after NUTU finishes speaking
  // -----------------------------------------

  const [voiceRestart, setVoiceRestart] =
    useState(0);


  // -----------------------------------------
  // APP STARTUP LOADER
  // -----------------------------------------

  useEffect(() => {

    const timer = setTimeout(() => {

      setAppLoading(false);

    }, 1800);


    return () => {

      clearTimeout(timer);

    };

  }, []);


  // -----------------------------------------
  // SEND MESSAGE
  // -----------------------------------------

  const handleSend = async (
    message,
    isVoice = false
  ) => {

    if (!message.trim() || isLoading) {
      return;
    }


    // ---------------------------------------
    // USER MESSAGE
    // ---------------------------------------

    const userMessage = {
      role: "user",
      content: message,
    };


    setMessages((previousMessages) => [
      ...previousMessages,
      userMessage,
    ]);


    // ---------------------------------------
    // START LOADING
    // ---------------------------------------

    setIsLoading(true);


    if (isVoice) {

      setVoiceState("thinking");

    }


    try {

      // -------------------------------------
      // SEND MESSAGE TO FASTAPI
      // -------------------------------------

      const response =
        await sendChatMessage(message);


      // -------------------------------------
      // NUTU RESPONSE
      // -------------------------------------

      const assistantMessage = {
        role: "assistant",
        content: response.answer,
        type: response.type,
        action: response.action,
      };


      setMessages((previousMessages) => [
        ...previousMessages,
        assistantMessage,
      ]);


      // -------------------------------------
      // VOICE RESPONSE
      // -------------------------------------

      if (isVoice && response.answer) {

        setVoiceState("speaking");


        speakText(
          response.answer,

          () => {

            // NUTU finished speaking
            // Start listening again

            setVoiceState("listening");


            setVoiceRestart(
              (previous) =>
                previous + 1
            );

          }
        );

      }


    } catch (error) {

      console.error(error);


      // -------------------------------------
      // ERROR MESSAGE
      // -------------------------------------

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


      // -------------------------------------
      // SPEAK ERROR
      // -------------------------------------

      if (isVoice) {

        setVoiceState("speaking");


        speakText(
          "Sorry, I'm having trouble connecting right now.",

          () => {

            setVoiceState("listening");


            setVoiceRestart(
              (previous) =>
                previous + 1
            );

          }
        );

      }


    } finally {

      setIsLoading(false);

    }

  };


  // -----------------------------------------
  // END VOICE SESSION
  // -----------------------------------------

  const handleEndVoice = () => {

    stopSpeaking();

    setVoiceState("idle");

  };


  // -----------------------------------------
  // APP LOADING SCREEN
  // -----------------------------------------

  if (appLoading) {

    return <AppLoader />;

  }


  // -----------------------------------------
  // MAIN APP
  // -----------------------------------------

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
        voiceState={voiceState}
        setVoiceState={setVoiceState}
        voiceRestart={voiceRestart}
        onEndVoice={handleEndVoice}
      />

    </div>

  );

}


export default App;
import {
  useEffect,
  useRef,
  useState,
} from "react";

import {
  Mic,
  X,
  AudioLines,
  LoaderCircle,
  Volume2,
} from "lucide-react";

import {
  createSpeechRecognition,
  isSpeechRecognitionSupported,
} from "../services/voiceService";


function ChatInput({
  onSend,
  isLoading,
  voiceState,
  setVoiceState,
  voiceRestart,
  onEndVoice,
}) {

  const [message, setMessage] =
    useState("");

  const [showVoice, setShowVoice] =
    useState(false);

  const recognitionRef = useRef(null);
  const voiceSupported = isSpeechRecognitionSupported();

  // Important:
  // tells callbacks whether voice mode is active
  const voiceActiveRef = useRef(false);


  // -----------------------------------------
  // TEXT MESSAGE
  // -----------------------------------------

  const handleSend = () => {

    if (!message.trim() || isLoading) {
      return;
    }

    // default: normal chat send
    onSend(message.trim(), false);

    setMessage("");
  };


  // -----------------------------------------
  // START LISTENING
  // -----------------------------------------

  const startListening = () => {

    if (!voiceActiveRef.current) {
      return;
    }


    const recognition =
  createSpeechRecognition();


    if (!recognition) {

      console.error(
        "Speech recognition is not supported."
      );

      voiceActiveRef.current = false;

      setShowVoice(false);

      setVoiceState("idle");

      return;
    }


    recognitionRef.current =
      recognition;


    recognition.onstart = () => {

      if (!voiceActiveRef.current) {
        recognition.stop();
        return;
      }

      setVoiceState("listening");

    };


    // ---------------------------------------
    // USER SPOKE
    // ---------------------------------------

    recognition.onresult = (event) => {

      if (!voiceActiveRef.current) {
        return;
      }


      const transcript =
        event.results[0][0].transcript;


      console.log(
        "Voice transcript:",
        transcript
      );


      if (transcript.trim()) {

        setVoiceState("thinking");


        onSend(
          transcript.trim(),
          true
        );

      }

    };


    // ---------------------------------------
    // LISTENING ENDED
    // ---------------------------------------

    recognition.onend = () => {

      recognitionRef.current = null;

    };


    // ---------------------------------------
    // ERROR
    // ---------------------------------------

    recognition.onerror = (event) => {

      console.error(
        "Speech recognition error:",
        event.error
      );


      recognitionRef.current = null;


      // Ignore harmless no-speech error
      if (
        event.error === "no-speech" &&
        voiceActiveRef.current
      ) {

        setTimeout(() => {

          if (voiceActiveRef.current) {
            startListening();
          }

        }, 500);

        return;
      }


      if (
        event.error === "aborted"
      ) {
        return;
      }


      voiceActiveRef.current = false;

      setShowVoice(false);

      setVoiceState("idle");

    };


    try {

      recognition.start();

    } catch (error) {

      console.error(
        "Could not start microphone:",
        error
      );

    }

  };


  // -----------------------------------------
  // OPEN VOICE MODE
  // -----------------------------------------

  const startVoice = () => {

    voiceActiveRef.current = true;

    setShowVoice(true);

    setVoiceState("listening");


    // Small delay so overlay opens first
    setTimeout(() => {

      if (voiceActiveRef.current) {
        startListening();
      }

    }, 200);

  };


  // -----------------------------------------
  // AUTO LISTEN AGAIN
  // AFTER NUTU FINISHES SPEAKING
  // -----------------------------------------

  useEffect(() => {

    if (
      voiceRestart > 0 &&
      voiceActiveRef.current &&
      showVoice
    ) {

      const timer = setTimeout(() => {

        if (voiceActiveRef.current) {
          startListening();
        }

      }, 400);


      return () => {
        clearTimeout(timer);
      };

    }

  }, [voiceRestart]);


  // -----------------------------------------
  // END VOICE SESSION
  // -----------------------------------------

  const closeVoice = () => {

    voiceActiveRef.current = false;


    if (recognitionRef.current) {

      try {
        recognitionRef.current.abort();
      } catch {
        // ignore
      }

      recognitionRef.current = null;

    }


    setShowVoice(false);

    setVoiceState("idle");

    onEndVoice();

  };


  // -----------------------------------------
  // STATUS
  // -----------------------------------------

  const getStatusTitle = () => {

    if (voiceState === "listening") {
      return "Listening...";
    }

    if (voiceState === "thinking") {
      return "NUTU is thinking...";
    }

    if (voiceState === "speaking") {
      return "NUTU is speaking...";
    }

    return "Talk to NUTU";
  };


  const getStatusText = () => {

    if (voiceState === "listening") {
      return "Go ahead, I'm listening.";
    }

    if (voiceState === "thinking") {
      return "Let me think about that.";
    }

    if (voiceState === "speaking") {
      return "NUTU is responding.";
    }

    return "";
  };


  return (
    <>

      {/* =====================================
          NORMAL CHAT INPUT
      ====================================== */}

      <footer className="border-t border-slate-800 bg-slate-950 px-4 py-5">

        <div className="mx-auto max-w-4xl">

          <div className="flex items-center gap-3 rounded-2xl border border-slate-700 bg-slate-900 p-2">


            {/* MIC */}

            <button
              type="button"
              onClick={startVoice}
              disabled={isLoading || !voiceSupported}
              title={
                voiceSupported
                  ? "Talk to NUTU"
                  : "Voice input is not supported by this browser"
              }
              className="flex h-11 w-11 shrink-0 items-center justify-center rounded-xl text-slate-400 transition hover:bg-slate-800 hover:text-white disabled:opacity-50"
            >
              <Mic size={20} />
            </button>


            {/* INPUT */}

            <input
              type="text"
              value={message}
              disabled={isLoading}
              onChange={(e) =>
                setMessage(e.target.value)
              }
              onKeyDown={(e) => {

                if (e.key === "Enter") {
                  handleSend();
                }

              }}
              placeholder={
                isLoading
                  ? "NUTU is thinking..."
                  : "Ask NUTU about Yassin..."
              }
              className="flex-1 bg-transparent px-2 py-3 text-sm text-white outline-none placeholder:text-slate-500 disabled:cursor-not-allowed"
            />


            {/* SEND */}

            <button
              type="button"
              onClick={handleSend}
              disabled={
                isLoading ||
                !message.trim()
              }
              className="rounded-xl bg-white px-5 py-3 text-sm font-semibold text-slate-950 transition hover:bg-slate-200 disabled:cursor-not-allowed disabled:opacity-50"
            >
              {isLoading ? "..." : "Send"}
            </button>

          </div>

        </div>

      </footer>


      {/* =====================================
          VOICE MODE
      ====================================== */}

      {showVoice && (

        <div className="fixed inset-0 z-50 flex items-center justify-center bg-slate-950/95 px-4 backdrop-blur-xl">


          {/* CLOSE */}

          <button
            type="button"
            onClick={closeVoice}
            title="End voice conversation"
            className="absolute right-6 top-6 flex h-11 w-11 items-center justify-center rounded-full bg-slate-800 text-slate-400 transition hover:bg-slate-700 hover:text-white"
          >
            <X size={21} />
          </button>


          <div className="flex flex-col items-center text-center">




            {/* CIRCLE */}

            <div className="relative flex h-44 w-44 items-center justify-center">


              {/* LISTENING PULSE */}

              {voiceState === "listening" && (
                <>

                  <div className="absolute h-44 w-44 animate-ping rounded-full bg-white/5" />

                  <div className="absolute h-36 w-36 animate-pulse rounded-full bg-white/10" />

                </>
              )}


              {/* SPEAKING PULSE */}

              {voiceState === "speaking" && (
                <div className="absolute h-36 w-36 animate-pulse rounded-full bg-white/10" />
              )}


              {/* MAIN CIRCLE */}

              <div className="relative flex h-24 w-24 items-center justify-center rounded-full bg-white text-slate-950 shadow-2xl shadow-white/10">


                {voiceState === "listening" && (
                  <AudioLines
                    size={35}
                    strokeWidth={1.8}
                  />
                )}


                {voiceState === "thinking" && (
                  <LoaderCircle
                    size={34}
                    className="animate-spin"
                    strokeWidth={1.8}
                  />
                )}


                {voiceState === "speaking" && (
                  <Volume2
                    size={34}
                    strokeWidth={1.8}
                  />
                )}


                {voiceState === "idle" && (
                  <Mic
                    size={32}
                    strokeWidth={1.8}
                  />
                )}

              </div>

            </div>


            {/* STATUS */}

            <h2 className="mt-8 text-2xl font-semibold text-white">
              {getStatusTitle()}
            </h2>


            <p className="mt-3 text-sm text-slate-500">
              {getStatusText()}
            </p>


            {/* END */}

            <button
              type="button"
              onClick={closeVoice}
              className="mt-10 rounded-full border border-slate-700 px-6 py-2.5 text-sm text-slate-300 transition hover:bg-slate-800 hover:text-white"
            >
              End voice
            </button>

          </div>

        </div>

      )}

    </>
  );
}


export default ChatInput;

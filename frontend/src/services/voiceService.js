export const createSpeechRecognition = () => {
  const SpeechRecognition =
    window.SpeechRecognition ||
    window.webkitSpeechRecognition;

  if (!SpeechRecognition) {
    return null;
  }

  const recognition = new SpeechRecognition();

  recognition.continuous = false;
  recognition.interimResults = false;

  // English only
  recognition.lang = "en-IN";

  return recognition;
};


// ---------------------------------------------
// SPEAK NUTU RESPONSE
// ---------------------------------------------

export const speakText = (
  text,
  onEnd = null
) => {
  if (!window.speechSynthesis) {
    console.error(
      "Speech synthesis is not supported."
    );
    return;
  }

  // Stop previous speech
  window.speechSynthesis.cancel();

  const speech =
    new SpeechSynthesisUtterance(text);

  speech.lang = "en-IN";
  speech.rate = 1;
  speech.pitch = 1;
  speech.volume = 1;


  speech.onstart = () => {
    console.log(
      "NUTU started speaking"
    );
  };


  speech.onend = () => {
    console.log(
      "NUTU finished speaking"
    );

    if (onEnd) {
      onEnd();
    }
  };


  speech.onerror = (event) => {
    console.error(
      "NUTU speech error:",
      event.error
    );

    if (onEnd) {
      onEnd();
    }
  };


  window.speechSynthesis.speak(speech);
};


// ---------------------------------------------
// STOP SPEAKING
// ---------------------------------------------

export const stopSpeaking = () => {
  if (window.speechSynthesis) {
    window.speechSynthesis.cancel();
  }
};
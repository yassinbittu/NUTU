// ---------------------------------------------
// CREATE SPEECH RECOGNITION
// ---------------------------------------------

export const isSpeechRecognitionSupported = () =>
  "SpeechRecognition" in window || "webkitSpeechRecognition" in window;

export const createSpeechRecognition = () => {
  const SpeechRecognition =
    window.SpeechRecognition ||
    window.webkitSpeechRecognition;

  if (!SpeechRecognition) {
    console.error("Speech Recognition is not supported.");
    return null;
  }

  const recognition = new SpeechRecognition();

  recognition.continuous = false;
  recognition.interimResults = false;
  recognition.lang = "en-IN";
  recognition.maxAlternatives = 1;

  return recognition;
};


// ---------------------------------------------
// LOAD VOICES
// ---------------------------------------------

let voices = [];

const loadVoices = () => {
  voices = window.speechSynthesis.getVoices();
};

loadVoices();

if ("speechSynthesis" in window) {
  window.speechSynthesis.onvoiceschanged = loadVoices;
}


// ---------------------------------------------
// SPEAK NUTU RESPONSE
// ---------------------------------------------

export const speakText = (
  text,
  onEnd = null
) => {

  if (!("speechSynthesis" in window)) {
    console.error("Speech synthesis not supported.");
    onEnd?.();
    return;
  }

  if (!text) {
    onEnd?.();
    return;
  }

  const speak = () => {

    // Stop previous speech
    window.speechSynthesis.cancel();

    const utterance =
      new SpeechSynthesisUtterance(text);

    // Voice settings
    utterance.lang = "en-US";
    utterance.rate = 1;
    utterance.pitch = 1;
    utterance.volume = 1;

    // Try English India first
    let selectedVoice =
      voices.find(
        voice => voice.lang === "en-IN"
      );

    // Otherwise English US
    if (!selectedVoice) {
      selectedVoice =
        voices.find(
          voice => voice.lang.startsWith("en-US")
        );
    }

    // Otherwise any English
    if (!selectedVoice) {
      selectedVoice =
        voices.find(
          voice => voice.lang.startsWith("en")
        );
    }

    // Otherwise first available
    if (!selectedVoice && voices.length > 0) {
      selectedVoice = voices[0];
    }

    if (selectedVoice) {
      utterance.voice = selectedVoice;
    }

    utterance.onstart = () => {
      console.log("NUTU started speaking");
    };

    utterance.onend = () => {
      console.log("NUTU finished speaking");

      if (onEnd) {
        onEnd();
      }
    };

    utterance.onerror = (event) => {
      console.error(
        "Speech Error:",
        event.error
      );

      if (onEnd) {
        onEnd();
      }
    };

    window.speechSynthesis.speak(
      utterance
    );
  };

  // Mobile browsers load voices asynchronously
  if (
    window.speechSynthesis.getVoices().length === 0
  ) {

    window.speechSynthesis.onvoiceschanged = () => {

      loadVoices();

      speak();
    };

  } else {

    loadVoices();

    speak();
  }

};


// ---------------------------------------------
// STOP SPEAKING
// ---------------------------------------------

export const stopSpeaking = () => {

  if ("speechSynthesis" in window) {

    window.speechSynthesis.cancel();

  }

};


// ---------------------------------------------
// UNLOCK SPEECH (Mobile)
// Call once when app starts
// ---------------------------------------------

export const unlockSpeech = () => {

  if (!("speechSynthesis" in window)) {
    return;
  }

  const unlock = () => {

    const utterance =
      new SpeechSynthesisUtterance("");

    window.speechSynthesis.speak(
      utterance
    );

    document.removeEventListener(
      "click",
      unlock
    );

    document.removeEventListener(
      "touchstart",
      unlock
    );
  };

  document.addEventListener(
    "click",
    unlock,
    {
      once: true
    }
  );

  document.addEventListener(
    "touchstart",
    unlock,
    {
      once: true
    }
  );

};

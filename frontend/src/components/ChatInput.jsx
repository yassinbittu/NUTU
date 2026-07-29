import { useState } from "react";


function ChatInput({ onSend, isLoading }) {
  const [message, setMessage] = useState("");


  const handleSend = () => {

    if (!message.trim() || isLoading) {
      return;
    }


    onSend(message.trim());

    setMessage("");
  };


  return (
    <footer className="border-t border-slate-800 bg-slate-950 px-4 py-5">

      <div className="mx-auto max-w-4xl">

        <div className="flex items-center gap-3 rounded-2xl border border-slate-700 bg-slate-900 p-2">

          <button
            type="button"
            className="flex h-11 w-11 shrink-0 items-center justify-center rounded-xl text-lg text-slate-400 transition hover:bg-slate-800 hover:text-white"
          >
            🎤
          </button>


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


          <button
            type="button"
            onClick={handleSend}
            disabled={isLoading}
            className="rounded-xl bg-white px-5 py-3 text-sm font-semibold text-slate-950 transition hover:bg-slate-200 disabled:cursor-not-allowed disabled:opacity-50"
          >
            {isLoading ? "..." : "Send"}
          </button>

        </div>


        <p className="mt-3 text-center text-xs text-slate-600">
          NUTU provides information about Mohammed Yassin.
        </p>

      </div>

    </footer>
  );
}


export default ChatInput;
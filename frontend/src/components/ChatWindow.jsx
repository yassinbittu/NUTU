import { useEffect, useRef } from "react";
import MessageBubble from "./MessageBubble";


function ChatWindow({
  messages,
  isLoading,
}) {

  const messagesEndRef = useRef(null);


  // Auto-scroll whenever a new message appears
  // or NUTU starts/stops thinking
  useEffect(() => {

    messagesEndRef.current?.scrollIntoView({
      behavior: "smooth",
    });

  }, [messages, isLoading]);


  return (
    <main className="flex-1 overflow-y-auto px-4 py-8">

      <div className="mx-auto flex max-w-4xl flex-col gap-6">

        {messages.map((message, index) => (

          <MessageBubble
            key={index}
            role={message.role}
            content={message.content}
            type={message.type}
            action={message.action}
          />

        ))}


        {/* Thinking indicator */}
        {isLoading && (

          <div className="flex items-start gap-3">

            <div className="flex h-9 w-9 shrink-0 items-center justify-center rounded-full bg-white font-bold text-slate-950">
              N
            </div>

            <div>

              <p className="mb-1 text-xs font-semibold text-slate-400">
                NUTU
              </p>

              <div className="rounded-2xl rounded-tl-sm bg-slate-800 px-4 py-3 text-sm text-slate-400">
                Thinking...
              </div>

            </div>

          </div>

        )}


        {/* Invisible element used for auto-scroll */}
        <div ref={messagesEndRef} />

      </div>

    </main>
  );
}


export default ChatWindow;
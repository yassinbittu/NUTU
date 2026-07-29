import { getFileUrl } from "../services/chatService";


function MessageBubble({
  role,
  content,
  type,
  action,
}) {
  const isUser = role === "user";


  // Create full resume URL only for resume responses
  const resumeUrl =
    type === "resume" && action?.url
      ? getFileUrl(action.url)
      : null;


  return (
    <div
      className={`flex items-start gap-3 ${
        isUser ? "justify-end" : "justify-start"
      }`}
    >

      {/* NUTU Avatar */}
      {!isUser && (
        <div className="flex h-9 w-9 shrink-0 items-center justify-center rounded-full bg-white font-bold text-slate-950">
          N
        </div>
      )}


      <div className={isUser ? "text-right" : ""}>

        {/* Sender Name */}
        <p className="mb-1 text-xs font-semibold text-slate-400">
          {isUser ? "You" : "NUTU"}
        </p>


        {/* Message Bubble */}
        <div
          className={`max-w-xl rounded-2xl px-4 py-3 text-left text-sm leading-6 ${
            isUser
              ? "rounded-tr-sm bg-white text-slate-950"
              : "rounded-tl-sm bg-slate-800 text-slate-100"
          }`}
        >

          {/* Message Text */}
          <p>
            {content}
          </p>


          {/* Resume Actions */}
          {resumeUrl && (
            <div className="mt-4 flex flex-wrap gap-3">

              {/* View Resume */}
              <a
                href={resumeUrl}
                target="_blank"
                rel="noopener noreferrer"
                className="rounded-lg bg-white px-4 py-2 text-xs font-semibold text-slate-950 transition hover:bg-slate-200"
              >
                View Resume
              </a>


              {/* Download Resume */}
              <a
                href={resumeUrl}
                download="Yassin_Mohammed_Resume.pdf"
                className="rounded-lg border border-slate-600 px-4 py-2 text-xs font-semibold text-white transition hover:bg-slate-700"
              >
                Download Resume
              </a>

            </div>
          )}

        </div>

      </div>

    </div>
  );
}


export default MessageBubble;
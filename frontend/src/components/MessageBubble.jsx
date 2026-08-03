import { getFileUrl } from "../services/chatService";


function MessageBubble({
  role,
  content,
  type,
  action,
  onQuickReply = () => {},
}) {
  const isUser = role === "user";
  const resumeUrl =
    type === "resume" && action?.url
      ? getFileUrl(action.url)
      : null;

  const quickReplies = action?.options || action?.suggestions || [];

  return (
    <div
      className={`flex items-start gap-3 ${
        isUser ? "justify-end" : "justify-start"
      }`}
    >
      {!isUser && (
        <div className="flex h-9 w-9 shrink-0 items-center justify-center rounded-full bg-white font-bold text-slate-950">
          N
        </div>
      )}

      <div className={isUser ? "text-right" : ""}>
        <p className="mb-1 text-xs font-semibold text-slate-400">
          {isUser ? "You" : "NUTU"}
        </p>

        <div
          className={`max-w-xl rounded-2xl px-4 py-3 text-left text-sm leading-6 ${
            isUser
              ? "rounded-tr-sm bg-white text-slate-950"
              : "rounded-tl-sm bg-slate-800 text-slate-100"
          }`}
        >
          <p className="whitespace-pre-wrap">{content}</p>

          {resumeUrl && (
            <div className="mt-4 flex flex-wrap gap-3">
              <a
                href={resumeUrl}
                target="_blank"
                rel="noopener noreferrer"
                className="rounded-lg bg-white px-4 py-2 text-xs font-semibold text-slate-950 transition hover:bg-slate-200"
              >
                View Resume
              </a>
              <a
                href={resumeUrl}
                download="Yassin_Mohammed_Resume.pdf"
                className="rounded-lg border border-slate-600 px-4 py-2 text-xs font-semibold text-white transition hover:bg-slate-700"
              >
                Download Resume
              </a>
            </div>
          )}

          {quickReplies.length > 0 && (
            <div className="mt-4 flex flex-wrap gap-2">
              {quickReplies.map((option) => (
                <button
                  key={`${option.label}-${option.message}`}
                  type="button"
                  onClick={() => onQuickReply(option.message)}
                  className={`rounded-lg px-4 py-2 text-xs font-semibold transition ${
                    option.variant === "secondary"
                      ? "border border-slate-600 text-white hover:bg-slate-700"
                      : "bg-white text-slate-950 hover:bg-slate-200"
                  }`}
                >
                  {option.label}
                </button>
              ))}
            </div>
          )}
        </div>
      </div>
    </div>
  );
}


export default MessageBubble;

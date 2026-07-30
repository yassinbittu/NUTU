function AppLoader() {
  return (
    <div className="fixed inset-0 z-[9999] flex items-center justify-center bg-slate-950">
      <div className="flex flex-col items-center">

        {/* Animated Logo */}
        <div className="relative flex h-32 w-32 items-center justify-center">

          {/* Pulse rings */}
          <div className="absolute h-28 w-28 animate-ping rounded-full bg-white/10" />

          <div className="absolute h-24 w-24 animate-pulse rounded-full bg-white/10" />

          {/* Logo */}
          <img
            src="/nutu-logo.png"
            alt="NUTU"
            className="relative z-10 h-20 w-20 animate-pulse rounded-full object-cover"
          />

        </div>

        <h1 className="mt-5 text-xl font-bold tracking-[0.3em] text-white">
          NUTU
        </h1>

        <p className="mt-2 text-xs text-slate-500">
          Personal AI Assistant
        </p>

        {/* Loading dots */}
        <div className="mt-6 flex gap-2">
          <span className="h-2 w-2 animate-bounce rounded-full bg-white" />

          <span
            className="h-2 w-2 animate-bounce rounded-full bg-white"
            style={{ animationDelay: "150ms" }}
          />

          <span
            className="h-2 w-2 animate-bounce rounded-full bg-white"
            style={{ animationDelay: "300ms" }}
          />
        </div>

      </div>
    </div>
  );
}

export default AppLoader;
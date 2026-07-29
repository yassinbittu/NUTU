function Header() {
  return (
    <header className="border-b border-slate-800 bg-slate-950 px-6 py-4">
      <div className="mx-auto flex max-w-5xl items-center justify-between">

        <div>
          <h1 className="text-2xl font-bold tracking-wide text-white">
            NUTU
          </h1>

          <p className="mt-1 text-sm text-slate-400">
            Personal AI Assistant for Mohammed Yassin
          </p>
        </div>

        <div className="flex items-center gap-2 text-sm text-slate-400">
          <span className="h-2 w-2 rounded-full bg-green-500"></span>
          Online
        </div>

      </div>
    </header>
  );
}

export default Header;
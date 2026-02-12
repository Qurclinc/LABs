function Header() {
  return (
    <header className="w-full h-20 border-b border-cyan flex items-center">
      <div className="max-w-screen-xl mx-auto w-full px-6 flex justify-between items-center">
        <h1 className="text-3xl font-bold text-purple">Crypto LabWork</h1>
        <span className="text-muted text-sm">
          Historical ciphers panel
        </span>
      </div>
    </header>
  );
}

export default Header;

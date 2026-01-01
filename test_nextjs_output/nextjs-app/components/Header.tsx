export default function Header() {
  return (
    <header className="border-b">
      <nav className="container mx-auto px-4 py-4">
        <div className="flex items-center justify-between">
          <a href="/" className="text-2xl font-heading font-bold">
            Demo Site
          </a>
          <div className="hidden md:flex gap-6">
            <a href="/" className="hover:text-primary transition-colors">Home</a>
            <a href="/about" className="hover:text-primary transition-colors">About</a>
          </div>
        </div>
      </nav>
    </header>
  )
}

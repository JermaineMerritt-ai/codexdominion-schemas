export default function Page() {
  return (
    <main>
      <nav style={{padding: '20px', background: 'var(--color-primary)', color: 'white'}}>
        <div style={{maxWidth: 'var(--container-width)', margin: '0 auto', display: 'flex', gap: '20px'}}>
          <a href="/" style={{color: "white", textDecoration: "none"}}>Home</a> | <a href="/about" style={{color: "white", textDecoration: "none"}}>About</a> | <a href="/services" style={{color: "white", textDecoration: "none"}}>Services</a> | <a href="/shop" style={{color: "white", textDecoration: "none"}}>Shop</a> | <a href="/contact" style={{color: "white", textDecoration: "none"}}>Contact</a> | <a href="/blog" style={{color: "white", textDecoration: "none"}}>Blog</a>
        </div>
      </nav>
      
        <section style={{padding: 'var(--section-padding) 0'}}>
          <div style={{maxWidth: 'var(--container-width)', margin: '0 auto', padding: '0 20px', textAlign: 'center'}}>
            <h1 style={{fontSize: '3rem', marginBottom: '1rem'}}>Welcome to Codex Digital Studios</h1>
            <p style={{fontSize: '1.25rem', marginBottom: '2rem'}}>AI-powered web development and digital solutions. Buy our premium templates and hire our expert team.</p>
            <a href="/contact" style={{display: 'inline-block', padding: '12px 24px', background: 'var(--color-accent)', color: 'white', textDecoration: 'none', borderRadius: '4px'}}>
              Get Started
            </a>
          </div>
        </section>

    </main>
  )
}

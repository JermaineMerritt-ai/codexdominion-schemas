export default function Page() {
  return (
    <main>
      <nav style={{padding: '20px', background: 'var(--color-primary)', color: 'white'}}>
        <div style={{maxWidth: 'var(--container-width)', margin: '0 auto', display: 'flex', gap: '20px'}}>
          <a href="/" style={{color: "white", textDecoration: "none"}}>Home</a> | <a href="/about" style={{color: "white", textDecoration: "none"}}>About</a> | <a href="/services" style={{color: "white", textDecoration: "none"}}>Services</a> | <a href="/shop" style={{color: "white", textDecoration: "none"}}>Shop</a> | <a href="/contact" style={{color: "white", textDecoration: "none"}}>Contact</a> | <a href="/blog" style={{color: "white", textDecoration: "none"}}>Blog</a>
        </div>
      </nav>
      
    </main>
  )
}

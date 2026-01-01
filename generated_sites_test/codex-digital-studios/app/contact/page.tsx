export default function Page() {
  return (
    <main>
      <nav style={{padding: '20px', background: 'var(--color-primary)', color: 'white'}}>
        <div style={{maxWidth: 'var(--container-width)', margin: '0 auto', display: 'flex', gap: '20px'}}>
          <a href="/" style={{color: "white", textDecoration: "none"}}>Home</a> | <a href="/about" style={{color: "white", textDecoration: "none"}}>About</a> | <a href="/services" style={{color: "white", textDecoration: "none"}}>Services</a> | <a href="/shop" style={{color: "white", textDecoration: "none"}}>Shop</a> | <a href="/contact" style={{color: "white", textDecoration: "none"}}>Contact</a> | <a href="/blog" style={{color: "white", textDecoration: "none"}}>Blog</a>
        </div>
      </nav>
      
        <section style={{padding: 'var(--section-padding) 0'}}>
          <div style={{maxWidth: '600px', margin: '0 auto', padding: '0 20px'}}>
            <h2 style={{fontSize: '2rem', marginBottom: '1rem', textAlign: 'center'}}>Get In Touch</h2>
            <form style={{display: 'flex', flexDirection: 'column', gap: '1rem'}}>
              <input type="text" placeholder="Name" style={{padding: '12px', border: '1px solid #ddd', borderRadius: '4px'}} />
              <input type="email" placeholder="Email" style={{padding: '12px', border: '1px solid #ddd', borderRadius: '4px'}} />
              <textarea placeholder="Message" rows={5} style={{padding: '12px', border: '1px solid #ddd', borderRadius: '4px'}}></textarea>
              <button type="submit" style={{padding: '12px', background: 'var(--color-accent)', color: 'white', border: 'none', borderRadius: '4px', cursor: 'pointer'}}>
                Send Message
              </button>
            </form>
          </div>
        </section>

    </main>
  )
}

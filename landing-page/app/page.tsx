'use client'

export default function Home() {
  const dashboardUrl = "https://codex-backend.bravefield-eea1536e.eastus.azurecontainerapps.io"
  
  return (
    <main style={{
      minHeight: '100vh',
      background: 'linear-gradient(135deg, #0F172A 0%, #1E293B 50%, #334155 100%)',
      color: '#F5F5F5',
      fontFamily: 'system-ui, -apple-system, sans-serif',
      padding: 0,
      margin: 0,
    }}>
      {/* Hero Section */}
      <section style={{
        padding: '80px 20px',
        textAlign: 'center',
        maxWidth: '1200px',
        margin: '0 auto',
      }}>
        <div style={{
          fontSize: '72px',
          marginBottom: '20px',
        }}>🔥</div>
        
        <h1 style={{
          fontSize: '3.5rem',
          fontWeight: '700',
          marginBottom: '20px',
          background: 'linear-gradient(135deg, #F5C542 0%, #FFD700 100%)',
          WebkitBackgroundClip: 'text',
          WebkitTextFillColor: 'transparent',
          backgroundClip: 'text',
        }}>
          Codex Dominion
        </h1>
        
        <p style={{
          fontSize: '1.5rem',
          color: '#94A3B8',
          marginBottom: '40px',
          maxWidth: '800px',
          margin: '0 auto 40px',
        }}>
          Your Digital Sovereignty Awaits
        </p>
        
        <div style={{
          display: 'flex',
          gap: '20px',
          justifyContent: 'center',
          flexWrap: 'wrap',
        }}>
          <a 
            href={dashboardUrl}
            target="_blank"
            rel="noopener noreferrer"
            style={{
              padding: '16px 40px',
              fontSize: '1.1rem',
              fontWeight: '600',
              background: 'linear-gradient(135deg, #F5C542 0%, #FFD700 100%)',
              color: '#0F172A',
              border: 'none',
              borderRadius: '8px',
              cursor: 'pointer',
              textDecoration: 'none',
              display: 'inline-block',
              transition: 'transform 0.2s',
            }}
            onMouseOver={(e) => e.currentTarget.style.transform = 'scale(1.05)'}
            onMouseOut={(e) => e.currentTarget.style.transform = 'scale(1)'}
          >
            🚀 Launch Dashboard
          </a>
        </div>
      </section>

      {/* Live Metrics Ticker */}
      <section style={{
        padding: '30px 20px',
        maxWidth: '1200px',
        margin: '0 auto',
        background: 'rgba(245, 197, 66, 0.1)',
        borderRadius: '12px',
        marginBottom: '40px',
      }}>
        <div style={{
          display: 'flex',
          justifyContent: 'space-around',
          alignItems: 'center',
          flexWrap: 'wrap',
          gap: '30px',
        }}>
          <MetricItem label="AI Agents Online" value="52+" icon="🤖" />
          <MetricItem label="Workflows Today" value="127" icon="🔄" />
          <MetricItem label="System Uptime" value="99.9%" icon="✅" />
          <MetricItem label="Last Update" value="2 min ago" icon="⚡" />
        </div>
      </section>

      {/* Features Section */}
      <section style={{
        padding: '60px 20px',
        maxWidth: '1200px',
        margin: '0 auto',
      }}>
        <div style={{
          display: 'grid',
          gridTemplateColumns: 'repeat(auto-fit, minmax(300px, 1fr))',
          gap: '30px',
        }}>
          <FeatureCard 
            icon="💰"
            title="Treasury Management"
            description="Track revenue streams, analyze financial metrics, and manage your digital empire with real-time insights."
          />
          <FeatureCard 
            icon="🤖"
            title="AI Agent System"
            description="52+ integrated AI agents working autonomously to optimize operations and execute workflows."
            badge="52+ Agents"
          />
          <FeatureCard 
            icon="👑"
            title="Council Governance"
            description="Democratic oversight system with workflow approval, budget allocation, and strategic planning."
          />
          <FeatureCard 
            icon="🎨"
            title="Creative Studio"
            description="Mythic branding, cultural storytelling, and commerce-ready content — powered by AI. Designed for diaspora creators, youth entrepreneurs, and digital empires."
            actionButton={{
              text: "Launch Studio",
              url: `${dashboardUrl}/studio`
            }}
          />
          <FeatureCard 
            icon="📊"
            title="Real-Time Analytics"
            description="Live dashboards for social media, e-commerce, affiliate marketing, and performance tracking."
          />
          <FeatureCard 
            icon="🔄"
            title="Workflow Automation"
            description="Database-backed workflow engine with PostgreSQL persistence and RQ job queue processing."
          />
          <FeatureCard 
            icon="☁️"
            title="Cloud Native"
            description="Deployed on Azure Container Apps with auto-scaling, managed PostgreSQL, and Redis caching."
          />
        </div>
      </section>

      {/* System Status */}
      <section style={{
        padding: '60px 20px',
        maxWidth: '800px',
        margin: '0 auto',
        textAlign: 'center',
      }}>
        <h2 style={{
          fontSize: '2rem',
          marginBottom: '30px',
          color: '#F5C542',
        }}>
          System Status
        </h2>
        
        <div style={{
          background: 'rgba(255, 255, 255, 0.05)',
          border: '1px solid rgba(245, 197, 66, 0.3)',
          borderRadius: '12px',
          padding: '30px',
          backdropFilter: 'blur(10px)',
        }}>
          <StatusRow label="Backend API" status="operational" />
          <StatusRow label="Database" status="operational" />
          <StatusRow label="AI Agents" status="operational" />
          <StatusRow label="Treasury Engine" status="operational" />
          <StatusRow label="Workflow Queue" status="operational" />
        </div>
      </section>

      {/* Footer */}
      <footer style={{
        padding: '40px 20px',
        textAlign: 'center',
        borderTop: '1px solid rgba(245, 197, 66, 0.2)',
        marginTop: '60px',
      }}>
        <div style={{
          display: 'flex',
          justifyContent: 'center',
          gap: '30px',
          marginBottom: '30px',
          flexWrap: 'wrap',
        }}>
          <a href={`${dashboardUrl}/dashboards`} style={{ color: '#94A3B8', textDecoration: 'none' }}>📚 Documentation</a>
          <a href={`${dashboardUrl}/council`} style={{ color: '#94A3B8', textDecoration: 'none' }}>👑 Council</a>
          <a href={`${dashboardUrl}/agents`} style={{ color: '#94A3B8', textDecoration: 'none' }}>🤖 AI Agents</a>
          <a href={`${dashboardUrl}/social`} style={{ color: '#94A3B8', textDecoration: 'none' }}>📱 Social Media</a>
          <a href={`${dashboardUrl}/stores`} style={{ color: '#94A3B8', textDecoration: 'none' }}>🛒 E-Commerce</a>
        </div>
        <p style={{
          color: '#64748B',
          fontSize: '0.9rem',
        }}>
          🔥 The Flame Burns Sovereign and Eternal 👑
        </p>
        <p style={{
          color: '#475569',
          fontSize: '0.8rem',
          marginTop: '10px',
        }}>
          Codex Dominion © 2025 | Powered by Azure Container Apps
        </p>
      </footer>
    </main>
  )
}

function FeatureCard({ icon, title, description, badge, actionButton }: { 
  icon: string, 
  title: string, 
  description: string,
  badge?: string,
  actionButton?: { text: string, url: string }
}) {
  return (
    <div style={{
      background: '#111',
      border: '1px solid #222',
      borderRadius: '10px',
      padding: '20px',
      transition: '0.3s ease',
      position: 'relative',
    }}
    onMouseOver={(e) => {
      e.currentTarget.style.transform = 'translateY(-5px)'
      e.currentTarget.style.borderColor = '#444'
    }}
    onMouseOut={(e) => {
      e.currentTarget.style.transform = 'translateY(0)'
      e.currentTarget.style.borderColor = '#222'
    }}
    >
      {badge && (
        <div style={{
          position: 'absolute',
          top: '15px',
          right: '15px',
          background: 'linear-gradient(135deg, #F5C542 0%, #FFD700 100%)',
          color: '#0F172A',
          padding: '4px 12px',
          borderRadius: '20px',
          fontSize: '0.75rem',
          fontWeight: '600',
        }}>
          {badge}
        </div>
      )}
      <div style={{ fontSize: '2.5rem', marginBottom: '15px' }}>{icon}</div>
      <h3 style={{ 
        fontSize: '1.3rem', 
        marginBottom: '10px',
      }}>{title}</h3>
      <p style={{ 
        color: '#ccc',
        lineHeight: '1.6',
        marginBottom: actionButton ? '15px' : '0',
      }}>{description}</p>
      
      {actionButton && (
        <a 
          href={actionButton.url}
          target="_blank"
          rel="noopener noreferrer"
          style={{
            display: 'inline-block',
            padding: '10px 16px',
            background: '#4f46e5',
            color: 'white',
            borderRadius: '6px',
            textDecoration: 'none',
            transition: '0.3s ease',
          }}
          onMouseOver={(e) => e.currentTarget.style.background = '#6366f1'}
          onMouseOut={(e) => e.currentTarget.style.background = '#4f46e5'}
        >
          {actionButton.text} →
        </a>
      )}
    </div>
  )
}

function StatusRow({ label, status }: { label: string, status: string }) {
  return (
    <div style={{
      display: 'flex',
      justifyContent: 'space-between',
      alignItems: 'center',
      padding: '12px 0',
      borderBottom: '1px solid rgba(255, 255, 255, 0.1)',
    }}>
      <span style={{ color: '#E2E8F0' }}>{label}</span>
      <span style={{
        color: '#10B981',
        display: 'flex',
        alignItems: 'center',
        gap: '8px',
      }}>
        <span style={{
          width: '8px',
          height: '8px',
          borderRadius: '50%',
          background: '#10B981',
          display: 'inline-block',
          animation: 'pulse 2s infinite',
        }}></span>
        {status}
      </span>
    </div>
  )
}

function MetricItem({ label, value, icon }: { label: string, value: string, icon: string }) {
  return (
    <div style={{
      textAlign: 'center',
    }}>
      <div style={{ fontSize: '1.5rem', marginBottom: '8px' }}>{icon}</div>
      <div style={{ 
        fontSize: '1.5rem', 
        fontWeight: '700',
        color: '#F5C542',
        marginBottom: '4px',
      }}>{value}</div>
      <div style={{ 
        fontSize: '0.85rem',
        color: '#94A3B8',
      }}>{label}</div>
    </div>
  )
}

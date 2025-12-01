import { useState } from 'react';
import Head from 'next/head';

export default function ChatbotHome() {
  const [messages, setMessages] = useState<{ role: string; content: string }[]>([]);
  const [input, setInput] = useState('');
  const [loading, setLoading] = useState(false);

  const sendMessage = async () => {
    if (!input.trim()) return;

    const userMessage = { role: 'user', content: input };
    setMessages(prev => [...prev, userMessage]);
    setInput('');
    setLoading(true);

    try {
      const response = await fetch('/api/chat', {
        method: 'POST',
        headers: { 'Content-Type': 'application/json' },
        body: JSON.stringify({ message: input })
      });

      const data = await response.json();
      setMessages(prev => [...prev, { role: 'assistant', content: data.response }]);
    } catch (error) {
      console.error('Chat error:', error);
      setMessages(prev => [...prev, { 
        role: 'assistant', 
        content: 'Sorry, I encountered an error. Please try again.' 
      }]);
    } finally {
      setLoading(false);
    }
  };

  return (
    <>
      <Head>
        <title>AI Chatbot - Codex Dominion</title>
      </Head>
      <div style={{ 
        display: 'flex', 
        flexDirection: 'column', 
        height: '100vh',
        fontFamily: 'system-ui, -apple-system, sans-serif',
        backgroundColor: '#0f172a'
      }}>
        <header style={{ 
          padding: '1rem 2rem',
          borderBottom: '1px solid #334155',
          backgroundColor: '#1e293b'
        }}>
          <h1 style={{ margin: 0, color: '#f8fafc', fontSize: '1.5rem' }}>
            🤖 AI Chatbot - Codex Dominion
          </h1>
          <p style={{ margin: '0.25rem 0 0 0', color: '#94a3b8', fontSize: '0.875rem' }}>
            Sovereign Chatbot Service
          </p>
        </header>

        <div style={{ 
          flex: 1, 
          overflowY: 'auto', 
          padding: '2rem',
          display: 'flex',
          flexDirection: 'column',
          gap: '1rem'
        }}>
          {messages.length === 0 && (
            <div style={{ 
              textAlign: 'center', 
              color: '#64748b',
              marginTop: '4rem'
            }}>
              <h2>Welcome to Codex Dominion AI Chatbot</h2>
              <p>Start a conversation to see the AI in action!</p>
            </div>
          )}
          
          {messages.map((msg, idx) => (
            <div
              key={idx}
              style={{
                alignSelf: msg.role === 'user' ? 'flex-end' : 'flex-start',
                backgroundColor: msg.role === 'user' ? '#3b82f6' : '#374151',
                color: '#ffffff',
                padding: '0.75rem 1rem',
                borderRadius: '0.5rem',
                maxWidth: '70%',
                wordWrap: 'break-word'
              }}
            >
              <strong>{msg.role === 'user' ? 'You' : 'AI'}:</strong> {msg.content}
            </div>
          ))}

          {loading && (
            <div style={{ 
              alignSelf: 'flex-start',
              color: '#64748b',
              fontStyle: 'italic'
            }}>
              AI is typing...
            </div>
          )}
        </div>

        <div style={{ 
          padding: '1rem 2rem',
          borderTop: '1px solid #334155',
          backgroundColor: '#1e293b',
          display: 'flex',
          gap: '1rem'
        }}>
          <input
            type="text"
            value={input}
            onChange={(e) => setInput(e.target.value)}
            onKeyPress={(e) => e.key === 'Enter' && sendMessage()}
            placeholder="Type your message..."
            disabled={loading}
            style={{
              flex: 1,
              padding: '0.75rem',
              borderRadius: '0.375rem',
              border: '1px solid #475569',
              backgroundColor: '#0f172a',
              color: '#f8fafc',
              fontSize: '1rem'
            }}
          />
          <button
            onClick={sendMessage}
            disabled={loading || !input.trim()}
            style={{
              padding: '0.75rem 2rem',
              borderRadius: '0.375rem',
              border: 'none',
              backgroundColor: loading || !input.trim() ? '#475569' : '#3b82f6',
              color: '#ffffff',
              fontSize: '1rem',
              cursor: loading || !input.trim() ? 'not-allowed' : 'pointer',
              fontWeight: 600
            }}
          >
            Send
          </button>
        </div>
      </div>
    </>
  );
}

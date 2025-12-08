import { useState, useEffect, useRef } from 'react';
import Head from 'next/head';
import styles from './index.module.css';

interface Message {
  role: 'user' | 'assistant';
  content: string;
  timestamp?: Date;
}

export default function ChatbotHome() {
  const [messages, setMessages] = useState<Message[]>([]);
  const [input, setInput] = useState('');
  const [loading, setLoading] = useState(false);
  const messagesEndRef = useRef<HTMLDivElement>(null);

  // Auto-scroll to bottom when new messages arrive
  useEffect(() => {
    messagesEndRef.current?.scrollIntoView({ behavior: 'smooth' });
  }, [messages]);

  const sendMessage = async () => {
    if (!input.trim()) return;

    const userMessage: Message = {
      role: 'user',
      content: input,
      timestamp: new Date()
    };

    setMessages(prev => [...prev, userMessage]);
    setInput('');
    setLoading(true);

    try {
      const response = await fetch('/api/chat', {
        method: 'POST',
        headers: { 'Content-Type': 'application/json' },
        body: JSON.stringify({ message: input })
      });

      if (!response.ok) {
        throw new Error(`HTTP error! status: ${response.status}`);
      }

      const data = await response.json();
      const assistantMessage: Message = {
        role: 'assistant',
        content: data.response || 'No response received.',
        timestamp: new Date()
      };

      setMessages(prev => [...prev, assistantMessage]);
    } catch (error) {
      console.error('Chat error:', error);
      const errorMessage: Message = {
        role: 'assistant',
        content: 'Sorry, I encountered an error. Please check your connection and try again.',
        timestamp: new Date()
      };
      setMessages(prev => [...prev, errorMessage]);
    } finally {
      setLoading(false);
    }
  };

  const handleKeyPress = (e: React.KeyboardEvent<HTMLInputElement>) => {
    if (e.key === 'Enter' && !loading) {
      sendMessage();
    }
  };

  return (
    <>
      <Head>
        <title>AI Chatbot - Codex Dominion</title>
        <meta name="description" content="Sovereign AI Chatbot powered by Codex Dominion" />
      </Head>
      <div className={styles.container}>
        <header className={styles.header}>
          <h1 className={styles.title}>
            🤖 AI Chatbot - Codex Dominion
          </h1>
          <p className={styles.subtitle}>
            Sovereign Chatbot Service
          </p>
        </header>

        <div className={styles.messagesContainer}>
          {messages.length === 0 && (
            <div className={styles.emptyState}>
              <h2>Welcome to Codex Dominion AI Chatbot</h2>
              <p>Start a conversation to see the AI in action!</p>
            </div>
          )}

          {messages.map((msg, idx) => (
            <div
              key={idx}
              className={`${styles.message} ${
                msg.role === 'user' ? styles.userMessage : styles.assistantMessage
              }`}
            >
              <span className={styles.messageLabel}>
                {msg.role === 'user' ? 'You' : 'AI'}:
              </span>
              <span className={styles.messageContent}>{msg.content}</span>
            </div>
          ))}

          {loading && (
            <div className={styles.loadingIndicator}>
              AI is thinking...
            </div>
          )}

          <div ref={messagesEndRef} />
        </div>

        <div className={styles.inputContainer}>
          <input
            type="text"
            value={input}
            onChange={(e) => setInput(e.target.value)}
            onKeyPress={handleKeyPress}
            placeholder="Type your message..."
            disabled={loading}
            className={styles.input}
            aria-label="Chat message input"
          />
          <button
            onClick={sendMessage}
            disabled={loading || !input.trim()}
            className={styles.sendButton}
            aria-label="Send message"
          >
            {loading ? 'Sending...' : 'Send'}
          </button>
        </div>
      </div>
    </>
  );
}

'use client'

import { useState } from 'react'

interface Command {
  icon: string
  label: string
  action: () => void
}

export default function AICommandStrip() {
  const [inputValue, setInputValue] = useState('')
  const [isProcessing, setIsProcessing] = useState(false)

  const quickCommands: Command[] = [
    { icon: '🎄', label: 'Generate Product', action: () => handleCommand('generate product') },
    { icon: '🎬', label: 'Create Video', action: () => handleCommand('create video') },
    { icon: '📱', label: 'Post Social', action: () => handleCommand('post social') },
    { icon: '📊', label: 'Run Report', action: () => handleCommand('run report') },
    { icon: '⚡', label: 'Execute Ritual', action: () => handleCommand('execute ritual') },
  ]

  const handleCommand = async (command: string) => {
    setIsProcessing(true)
    setInputValue(command)

    // Simulate AI processing
    await new Promise(resolve => setTimeout(resolve, 1500))

    console.log('AI Command:', command)
    setIsProcessing(false)
    setInputValue('')
  }

  const handleSubmit = (e: React.FormEvent) => {
    e.preventDefault()
    if (inputValue.trim()) {
      handleCommand(inputValue)
    }
  }

  return (
    <div className="codex-card mb-6">
      <div className="flex items-center space-x-3 mb-4">
        <span className="text-2xl">🤖</span>
        <h3 className="text-lg font-serif text-codex-gold">AI Command Center</h3>
        {isProcessing && (
          <div className="flex items-center space-x-2 text-xs text-blue-400">
            <div className="w-2 h-2 rounded-full bg-blue-500 animate-pulse"></div>
            <span>Processing...</span>
          </div>
        )}
      </div>

      {/* Command Input */}
      <form onSubmit={handleSubmit} className="mb-4">
        <div className="flex space-x-2">
          <input
            type="text"
            value={inputValue}
            onChange={(e) => setInputValue(e.target.value)}
            placeholder="Type a command or request... (e.g., 'create advent video', 'generate sales report')"
            className="flex-1 bg-codex-navy/50 border border-codex-gold/30 rounded px-4 py-2 text-codex-parchment focus:outline-none focus:border-codex-gold"
            disabled={isProcessing}
          />
          <button
            type="submit"
            disabled={isProcessing || !inputValue.trim()}
            className="codex-button disabled:opacity-50 disabled:cursor-not-allowed"
          >
            {isProcessing ? '⏳' : '▶️'} Execute
          </button>
        </div>
      </form>

      {/* Quick Commands */}
      <div className="flex flex-wrap gap-2">
        {quickCommands.map((cmd, idx) => (
          <button
            key={idx}
            onClick={cmd.action}
            disabled={isProcessing}
            className="codex-button text-sm disabled:opacity-50"
          >
            <span className="mr-1">{cmd.icon}</span>
            {cmd.label}
          </button>
        ))}
      </div>

      {/* Recent Commands */}
      <div className="mt-4 pt-4 border-t border-codex-gold/20">
        <h4 className="text-xs font-semibold text-codex-parchment/70 uppercase mb-2">
          Recent Commands
        </h4>
        <div className="space-y-1 text-xs text-codex-parchment/60">
          <div className="flex items-center space-x-2">
            <span className="text-green-400">✓</span>
            <span>Generated Advent Devotional Product</span>
            <span className="ml-auto">2 min ago</span>
          </div>
          <div className="flex items-center space-x-2">
            <span className="text-green-400">✓</span>
            <span>Executed Ritual Health Monitor</span>
            <span className="ml-auto">5 min ago</span>
          </div>
          <div className="flex items-center space-x-2">
            <span className="text-green-400">✓</span>
            <span>Created System Capsules</span>
            <span className="ml-auto">10 min ago</span>
          </div>
        </div>
      </div>
    </div>
  )
}

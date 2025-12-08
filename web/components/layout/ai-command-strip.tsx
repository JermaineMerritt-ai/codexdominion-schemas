'use client';

import { useState } from 'react';

interface AIModel {
  name: string;
  icon: string;
  color: string;
}

const aiModels: AIModel[] = [
  { name: 'Jermaine Super Action AI', icon: '⚡', color: 'bg-purple-600' },
  { name: 'Codex Copilot', icon: '🤖', color: 'bg-blue-600' },
  { name: 'Claude', icon: '🧠', color: 'bg-orange-600' },
  { name: 'VS Code Copilot', icon: '💻', color: 'bg-green-600' },
];

const modes = [
  { name: 'Explain', icon: '💡' },
  { name: 'Build', icon: '🔨' },
  { name: 'Operate', icon: '▶️' },
  { name: 'Debug', icon: '🐛' },
];

export function AICommandStrip() {
  const [selectedAI, setSelectedAI] = useState<string>('Jermaine Super Action AI');
  const [selectedMode, setSelectedMode] = useState<string>('Explain');
  const [command, setCommand] = useState('');
  const [isListening, setIsListening] = useState(false);

  const handleSubmit = (e: React.FormEvent) => {
    e.preventDefault();
    if (command.trim()) {
      console.log('Command submitted:', { ai: selectedAI, mode: selectedMode, command });
      // TODO: Send to backend API
      setCommand('');
    }
  };

  const toggleVoice = () => {
    setIsListening(!isListening);
    // TODO: Implement voice recognition
  };

  return (
    <div className="absolute bottom-0 left-0 right-0 bg-[#1A1F3C] text-white border-t border-[#FFD700]/50 shadow-2xl">
      <div className="p-4 space-y-3">
        {/* AI Model Selection */}
        <div className="flex items-center space-x-2 overflow-x-auto pb-2">
          <span className="text-xs font-semibold text-gray-400 whitespace-nowrap">AI:</span>
          {aiModels.map((ai) => (
            <button
              key={ai.name}
              onClick={() => setSelectedAI(ai.name)}
              className={`
                flex items-center space-x-2 px-3 py-1.5 rounded-lg text-sm font-medium whitespace-nowrap transition-all
                ${selectedAI === ai.name
                  ? `${ai.color} text-white shadow-lg scale-105`
                  : 'bg-[#0A0F29] text-gray-300 hover:bg-[#FFD700] hover:text-black'
                }
              `}
            >
              <span>{ai.icon}</span>
              <span>{ai.name}</span>
            </button>
          ))}
        </div>

        {/* Command Input */}
        <form onSubmit={handleSubmit} className="flex items-center space-x-3">
          <input
            type="text"
            value={command}
            onChange={(e) => setCommand(e.target.value)}
            placeholder="Ask or command any engine, tool, or realm..."
            className="flex-1 px-4 py-3 rounded-lg bg-[#0A0F29] text-white placeholder-gray-400 border border-[#FFD700]/30 focus:border-[#FFD700] focus:outline-none focus:ring-2 focus:ring-[#FFD700]/50 transition-all"
          />
          <button
            type="button"
            onClick={toggleVoice}
            className={`
              px-4 py-3 rounded-lg font-semibold transition-all
              ${isListening
                ? 'bg-red-600 text-white animate-pulse'
                : 'bg-[#FFD700] text-black hover:bg-[#FFA500]'
              }
            `}
            aria-label="Voice input"
          >
            <span className="text-xl">{isListening ? '⏹️' : '🎙️'}</span>
          </button>
          <button
            type="submit"
            disabled={!command.trim()}
            className="px-6 py-3 bg-[#FFD700] text-black font-semibold rounded-lg hover:bg-[#FFA500] disabled:opacity-50 disabled:cursor-not-allowed transition-all"
          >
            Send
          </button>
        </form>

        {/* Mode Selection */}
        <div className="flex items-center space-x-2 overflow-x-auto">
          <span className="text-xs font-semibold text-gray-400 whitespace-nowrap">Mode:</span>
          {modes.map((mode) => (
            <button
              key={mode.name}
              onClick={() => setSelectedMode(mode.name)}
              className={`
                flex items-center space-x-2 px-3 py-1.5 rounded-lg text-sm font-medium whitespace-nowrap transition-all
                ${selectedMode === mode.name
                  ? 'bg-[#FFD700] text-black shadow-lg scale-105'
                  : 'bg-[#0A0F29] text-gray-300 hover:bg-[#FFD700] hover:text-black'
                }
              `}
            >
              <span>{mode.icon}</span>
              <span>{mode.name}</span>
            </button>
          ))}
        </div>

        {/* Status Bar */}
        <div className="flex items-center justify-between text-xs text-gray-400 pt-2 border-t border-[#FFD700]/20">
          <div className="flex items-center space-x-4">
            <span>Selected: <strong className="text-[#FFD700]">{selectedAI}</strong></span>
            <span>Mode: <strong className="text-[#FFD700]">{selectedMode}</strong></span>
          </div>
          <div className="flex items-center space-x-2">
            <span className="w-2 h-2 bg-green-500 rounded-full animate-pulse"></span>
            <span>Backend Connected</span>
          </div>
        </div>
      </div>
    </div>
  );
}

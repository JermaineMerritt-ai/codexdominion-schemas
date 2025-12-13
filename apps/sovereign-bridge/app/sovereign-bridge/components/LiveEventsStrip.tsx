'use client'

import { useEffect, useState } from 'react'

interface LiveEvent {
  id: string
  message: string
  timestamp: Date
  type: 'success' | 'info' | 'warning' | 'error'
}

export default function LiveEventsStrip() {
  const [events, setEvents] = useState<LiveEvent[]>([])

  useEffect(() => {
    // Mock live events
    const mockEvents: LiveEvent[] = [
      { id: '1', message: 'Advent Devotional Product Created - ADVENT-2025', timestamp: new Date(), type: 'success' },
      { id: '2', message: 'Ritual Health Monitor Completed - 7/7 Active', timestamp: new Date(Date.now() - 60000), type: 'success' },
      { id: '3', message: 'System Capsules Restored - 5 capsules created', timestamp: new Date(Date.now() - 120000), type: 'info' },
    ]
    setEvents(mockEvents)
  }, [])

  const getEventColor = (type: string) => {
    switch (type) {
      case 'success': return 'border-green-500/50 bg-green-500/10 text-green-400'
      case 'info': return 'border-blue-500/50 bg-blue-500/10 text-blue-400'
      case 'warning': return 'border-yellow-500/50 bg-yellow-500/10 text-yellow-400'
      case 'error': return 'border-red-500/50 bg-red-500/10 text-red-400'
      default: return 'border-gray-500/50 bg-gray-500/10 text-gray-400'
    }
  }

  const getEventIcon = (type: string) => {
    switch (type) {
      case 'success': return '✅'
      case 'info': return 'ℹ️'
      case 'warning': return '⚠️'
      case 'error': return '❌'
      default: return '📌'
    }
  }

  const formatTimestamp = (date: Date) => {
    const diff = Date.now() - date.getTime()
    const minutes = Math.floor(diff / 60000)
    if (minutes < 1) return 'Just now'
    if (minutes < 60) return `${minutes}m ago`
    const hours = Math.floor(minutes / 60)
    return `${hours}h ago`
  }

  return (
    <div className="codex-panel overflow-x-auto">
      <div className="flex items-center space-x-4 min-w-max">
        <span className="text-sm font-semibold text-codex-gold whitespace-nowrap">🔴 LIVE</span>
        {events.map((event) => (
          <div
            key={event.id}
            className={`inline-flex items-center space-x-2 px-4 py-2 rounded-md border ${getEventColor(event.type)} whitespace-nowrap`}
          >
            <span>{getEventIcon(event.type)}</span>
            <span className="text-sm font-medium">{event.message}</span>
            <span className="text-xs opacity-70">{formatTimestamp(event.timestamp)}</span>
          </div>
        ))}
      </div>
    </div>
  )
}

/**
 * Timeline
 * ========
 * Article publication timeline and update history
 */

"use client"

import { Clock, CheckCircle2, AlertCircle } from 'lucide-react'

interface TimelineProps {
  articleId: string
  publishedAt: string
}

export default function Timeline({ articleId, publishedAt }: TimelineProps) {
  // Mock timeline data - in production, this would come from verification history
  const events = [
    {
      timestamp: publishedAt,
      type: 'published',
      title: 'Article Published',
      description: 'Original article published by primary source',
      icon: Clock
    },
    {
      timestamp: new Date(new Date(publishedAt).getTime() + 15 * 60000).toISOString(),
      type: 'verification',
      title: 'Verification Check Initiated',
      description: 'Automated verification process started',
      icon: Clock
    },
    {
      timestamp: new Date(new Date(publishedAt).getTime() + 30 * 60000).toISOString(),
      type: 'sources_found',
      title: '3 Additional Sources Found',
      description: 'Cross-referenced with Bloomberg, Reuters, WSJ',
      icon: CheckCircle2
    },
    {
      timestamp: new Date(new Date(publishedAt).getTime() + 45 * 60000).toISOString(),
      type: 'verification_complete',
      title: 'Verification Complete',
      description: 'Verification score: 87/100 (Highly Verified)',
      icon: CheckCircle2
    }
  ]

  return (
    <div className="space-y-6">
      <div className="flex items-center justify-between mb-4">
        <h3 className="font-semibold text-gray-900">Publication Timeline</h3>
        <span className="text-sm text-gray-500">
          {events.length} events
        </span>
      </div>

      <div className="relative">
        {/* Vertical Line */}
        <div className="absolute left-4 top-0 bottom-0 w-0.5 bg-gray-200"></div>

        {/* Timeline Events */}
        <div className="space-y-6">
          {events.map((event, index) => {
            const Icon = event.icon
            const isLast = index === events.length - 1

            return (
              <div key={index} className="relative pl-12">
                {/* Icon */}
                <div className={`absolute left-0 w-8 h-8 rounded-full flex items-center justify-center ${
                  event.type === 'verification_complete' ? 'bg-green-100' : 'bg-gray-100'
                }`}>
                  <Icon className={`h-4 w-4 ${
                    event.type === 'verification_complete' ? 'text-green-600' : 'text-gray-600'
                  }`} />
                </div>

                {/* Content */}
                <div className={`${!isLast ? 'pb-6' : ''}`}>
                  <div className="bg-gray-50 rounded-lg p-4 border border-gray-200">
                    <div className="flex items-start justify-between mb-2">
                      <h4 className="font-semibold text-gray-900">{event.title}</h4>
                      <span className="text-xs text-gray-500">
                        {formatTime(event.timestamp)}
                      </span>
                    </div>
                    <p className="text-sm text-gray-600">{event.description}</p>
                  </div>
                </div>
              </div>
            )
          })}
        </div>
      </div>

      {/* Auto-Update Notice */}
      <div className="mt-6 p-4 bg-blue-50 border border-blue-200 rounded-lg">
        <div className="flex items-start">
          <Clock className="h-5 w-5 text-blue-600 mr-3 flex-shrink-0 mt-0.5" />
          <div>
            <h4 className="font-semibold text-blue-900 mb-1">
              Automatic Monitoring
            </h4>
            <p className="text-sm text-blue-800">
              This article is continuously monitored for updates. New sources and fact-checks are added automatically.
            </p>
          </div>
        </div>
      </div>
    </div>
  )
}

function formatTime(timestamp: string): string {
  const date = new Date(timestamp)
  const now = new Date()
  const diffMs = now.getTime() - date.getTime()
  const diffMins = Math.floor(diffMs / 60000)
  const diffHours = Math.floor(diffMins / 60)

  if (diffMins < 1) return 'Just now'
  if (diffMins < 60) return `${diffMins}m ago`
  if (diffHours < 24) return `${diffHours}h ago`
  
  return date.toLocaleTimeString('en-US', {
    hour: '2-digit',
    minute: '2-digit',
    hour12: true
  })
}

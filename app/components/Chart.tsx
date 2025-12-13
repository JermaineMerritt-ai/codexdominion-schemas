'use client'

interface ChartProps {
  title?: string
  type: 'line' | 'bar' | 'donut' | 'area'
  data: any
  height?: number
  color?: string
}

export default function Chart({ title, type, data, height = 300, color = '#d4af37' }: ChartProps) {
  // Placeholder for chart library integration (Chart.js, Recharts, etc.)
  return (
    <div className="codex-panel">
      {title && (
        <h3 className="text-lg font-serif text-codex-gold mb-4">{title}</h3>
      )}
      <div
        className="bg-codex-navy/50 rounded-lg flex items-center justify-center"
        style={{ height: `${height}px` }}
      >
        <div className="text-center text-codex-parchment/50">
          <span className="text-4xl mb-2 block">📊</span>
          <p className="text-sm">{type.toUpperCase()} Chart</p>
          <p className="text-xs mt-1">Chart library integration pending</p>
        </div>
      </div>
    </div>
  )
}

// Simple bar chart component (no external library)
export function SimpleBarChart({
  data,
  title,
  height = 200,
}: {
  data: Array<{ label: string; value: number; color?: string }>
  title?: string
  height?: number
}) {
  const maxValue = Math.max(...data.map(d => d.value))

  return (
    <div className="codex-panel">
      {title && (
        <h3 className="text-lg font-serif text-codex-gold mb-4">{title}</h3>
      )}
      <div className="space-y-3">
        {data.map((item, idx) => (
          <div key={idx}>
            <div className="flex items-center justify-between text-sm mb-1">
              <span className="text-codex-parchment/80">{item.label}</span>
              <span className="font-semibold text-codex-gold">{item.value}</span>
            </div>
            <div className="w-full bg-codex-navy/50 rounded-full h-6">
              <div
                className={`h-6 rounded-full transition-all duration-500 flex items-center justify-end px-2 text-xs font-semibold`}
                style={{
                  width: `${(item.value / maxValue) * 100}%`,
                  backgroundColor: item.color || '#d4af37',
                }}
              >
                {item.value > 0 && `${Math.round((item.value / maxValue) * 100)}%`}
              </div>
            </div>
          </div>
        ))}
      </div>
    </div>
  )
}

// Simple line trend indicator
export function TrendLine({
  data,
  title,
  height = 100,
  color = '#d4af37',
}: {
  data: number[]
  title?: string
  height?: number
  color?: string
}) {
  const max = Math.max(...data)
  const min = Math.min(...data)
  const range = max - min || 1

  const points = data
    .map((value, index) => {
      const x = (index / (data.length - 1)) * 100
      const y = 100 - ((value - min) / range) * 100
      return `${x},${y}`
    })
    .join(' ')

  return (
    <div className="codex-panel">
      {title && (
        <h3 className="text-sm font-semibold text-codex-parchment/80 mb-2">{title}</h3>
      )}
      <svg
        viewBox="0 0 100 100"
        className="w-full rounded"
        style={{ height: `${height}px`, backgroundColor: 'rgba(15, 43, 74, 0.3)' }}
      >
        {/* Grid lines */}
        <line x1="0" y1="25" x2="100" y2="25" stroke="rgba(212, 175, 55, 0.1)" strokeWidth="0.5" />
        <line x1="0" y1="50" x2="100" y2="50" stroke="rgba(212, 175, 55, 0.1)" strokeWidth="0.5" />
        <line x1="0" y1="75" x2="100" y2="75" stroke="rgba(212, 175, 55, 0.1)" strokeWidth="0.5" />

        {/* Area fill */}
        <polyline
          points={`0,100 ${points} 100,100`}
          fill={color}
          fillOpacity="0.1"
        />

        {/* Line */}
        <polyline
          points={points}
          fill="none"
          stroke={color}
          strokeWidth="2"
          strokeLinecap="round"
          strokeLinejoin="round"
        />

        {/* Points */}
        {data.map((value, index) => {
          const x = (index / (data.length - 1)) * 100
          const y = 100 - ((value - min) / range) * 100
          return (
            <circle
              key={index}
              cx={x}
              cy={y}
              r="2"
              fill={color}
            />
          )
        })}
      </svg>

      <div className="flex justify-between text-xs text-codex-parchment/60 mt-2">
        <span>Min: {min}</span>
        <span>Max: {max}</span>
        <span>Latest: {data[data.length - 1]}</span>
      </div>
    </div>
  )
}

// Donut chart component
export function DonutChart({
  data,
  title,
  size = 200,
}: {
  data: Array<{ label: string; value: number; color: string }>
  title?: string
  size?: number
}) {
  const total = data.reduce((sum, item) => sum + item.value, 0)
  let cumulativePercent = 0

  const getCoordinatesForPercent = (percent: number) => {
    const x = Math.cos(2 * Math.PI * percent)
    const y = Math.sin(2 * Math.PI * percent)
    return [x, y]
  }

  return (
    <div className="codex-panel">
      {title && (
        <h3 className="text-lg font-serif text-codex-gold mb-4">{title}</h3>
      )}
      <div className="flex items-center space-x-6">
        <svg width={size} height={size} viewBox="-1 -1 2 2" className="transform -rotate-90">
          {data.map((item, idx) => {
            const [startX, startY] = getCoordinatesForPercent(cumulativePercent)
            cumulativePercent += item.value / total
            const [endX, endY] = getCoordinatesForPercent(cumulativePercent)
            const largeArcFlag = item.value / total > 0.5 ? 1 : 0

            const pathData = [
              `M ${startX} ${startY}`,
              `A 1 1 0 ${largeArcFlag} 1 ${endX} ${endY}`,
              'L 0 0',
            ].join(' ')

            return (
              <path
                key={idx}
                d={pathData}
                fill={item.color}
                opacity="0.8"
              />
            )
          })}
          <circle cx="0" cy="0" r="0.6" fill="#0f2b4a" />
        </svg>

        <div className="space-y-2">
          {data.map((item, idx) => (
            <div key={idx} className="flex items-center space-x-2">
              <div
                className="w-3 h-3 rounded"
                style={{ backgroundColor: item.color }}
              />
              <span className="text-sm text-codex-parchment/80">{item.label}</span>
              <span className="text-sm font-semibold text-codex-gold ml-auto">
                {Math.round((item.value / total) * 100)}%
              </span>
            </div>
          ))}
        </div>
      </div>
    </div>
  )
}

'use client'

import { ReactNode } from 'react'

interface Column<T = any> {
  key: string
  header: string
  render?: (value: any, row: T) => ReactNode
  align?: 'left' | 'center' | 'right'
  width?: string
  sortable?: boolean
}

interface TableProps<T = any> {
  data: T[]
  columns: Column<T>[]
  onRowClick?: (row: T) => void
  isLoading?: boolean
  emptyMessage?: string
  striped?: boolean
  hoverable?: boolean
  compact?: boolean
}

export default function Table<T = any>({
  data,
  columns,
  onRowClick,
  isLoading = false,
  emptyMessage = 'No data available',
  striped = true,
  hoverable = true,
  compact = false,
}: TableProps<T>) {
  const getCellValue = (row: T, column: Column<T>) => {
    const value = (row as any)[column.key]
    return column.render ? column.render(value, row) : value
  }

  const getAlignClass = (align?: string) => {
    switch (align) {
      case 'center': return 'text-center'
      case 'right': return 'text-right'
      default: return 'text-left'
    }
  }

  if (isLoading) {
    return (
      <div className="codex-panel">
        <div className="flex items-center justify-center py-12">
          <div className="text-center">
            <div className="w-12 h-12 border-4 border-codex-gold/30 border-t-codex-gold rounded-full animate-spin mx-auto mb-4"></div>
            <p className="text-codex-parchment/60">Loading data...</p>
          </div>
        </div>
      </div>
    )
  }

  if (data.length === 0) {
    return (
      <div className="codex-panel">
        <div className="flex items-center justify-center py-12">
          <div className="text-center">
            <span className="text-6xl mb-4 block">📊</span>
            <p className="text-codex-parchment/60">{emptyMessage}</p>
          </div>
        </div>
      </div>
    )
  }

  return (
    <div className="codex-panel overflow-x-auto">
      <table className="w-full">
        <thead>
          <tr className="border-b border-codex-gold/20">
            {columns.map((column, idx) => (
              <th
                key={idx}
                className={`
                  ${compact ? 'px-3 py-2' : 'px-4 py-3'}
                  ${getAlignClass(column.align)}
                  text-xs font-semibold text-codex-gold uppercase
                  ${column.sortable ? 'cursor-pointer hover:text-codex-gold/80' : ''}
                `}
                style={{ width: column.width }}
              >
                <div className="flex items-center space-x-1">
                  <span>{column.header}</span>
                  {column.sortable && <span className="text-xs">⇅</span>}
                </div>
              </th>
            ))}
          </tr>
        </thead>
        <tbody>
          {data.map((row, rowIdx) => (
            <tr
              key={rowIdx}
              className={`
                ${striped && rowIdx % 2 === 1 ? 'bg-codex-navy/30' : ''}
                ${hoverable ? 'hover:bg-codex-gold/5' : ''}
                ${onRowClick ? 'cursor-pointer' : ''}
                border-b border-codex-gold/10 last:border-b-0
                transition-colors
              `}
              onClick={() => onRowClick?.(row)}
            >
              {columns.map((column, colIdx) => (
                <td
                  key={colIdx}
                  className={`
                    ${compact ? 'px-3 py-2' : 'px-4 py-3'}
                    ${getAlignClass(column.align)}
                    text-sm text-codex-parchment
                  `}
                >
                  {getCellValue(row, column)}
                </td>
              ))}
            </tr>
          ))}
        </tbody>
      </table>
    </div>
  )
}

// Simple data table with minimal configuration
export function SimpleTable({
  headers,
  rows,
  onRowClick,
}: {
  headers: string[]
  rows: (string | number | ReactNode)[][]
  onRowClick?: (rowIndex: number) => void
}) {
  return (
    <div className="codex-panel overflow-x-auto">
      <table className="w-full">
        <thead>
          <tr className="border-b border-codex-gold/20">
            {headers.map((header, idx) => (
              <th
                key={idx}
                className="px-4 py-3 text-xs font-semibold text-codex-gold uppercase text-left"
              >
                {header}
              </th>
            ))}
          </tr>
        </thead>
        <tbody>
          {rows.map((row, rowIdx) => (
            <tr
              key={rowIdx}
              className={`
                ${rowIdx % 2 === 1 ? 'bg-codex-navy/30' : ''}
                hover:bg-codex-gold/5
                ${onRowClick ? 'cursor-pointer' : ''}
                border-b border-codex-gold/10 last:border-b-0
                transition-colors
              `}
              onClick={() => onRowClick?.(rowIdx)}
            >
              {row.map((cell, cellIdx) => (
                <td key={cellIdx} className="px-4 py-3 text-sm text-codex-parchment">
                  {cell}
                </td>
              ))}
            </tr>
          ))}
        </tbody>
      </table>
    </div>
  )
}

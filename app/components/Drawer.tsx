'use client'

import { ReactNode, useEffect } from 'react'

interface DrawerProps {
  isOpen: boolean
  onClose: () => void
  title?: string
  position?: 'left' | 'right'
  size?: 'sm' | 'md' | 'lg'
  children: ReactNode
  footer?: ReactNode
}

export default function Drawer({
  isOpen,
  onClose,
  title,
  position = 'right',
  size = 'md',
  children,
  footer,
}: DrawerProps) {
  useEffect(() => {
    if (isOpen) {
      document.body.style.overflow = 'hidden'
    } else {
      document.body.style.overflow = 'unset'
    }
    return () => {
      document.body.style.overflow = 'unset'
    }
  }, [isOpen])

  useEffect(() => {
    const handleEscape = (e: KeyboardEvent) => {
      if (e.key === 'Escape' && isOpen) {
        onClose()
      }
    }
    document.addEventListener('keydown', handleEscape)
    return () => document.removeEventListener('keydown', handleEscape)
  }, [isOpen, onClose])

  if (!isOpen) return null

  const sizeClasses = {
    sm: 'w-80',
    md: 'w-96',
    lg: 'w-[32rem]',
  }[size]

  const positionClasses = {
    left: 'left-0',
    right: 'right-0',
  }[position]

  const slideClasses = {
    left: isOpen ? 'translate-x-0' : '-translate-x-full',
    right: isOpen ? 'translate-x-0' : 'translate-x-full',
  }[position]

  return (
    <div className="fixed inset-0 z-50">
      {/* Backdrop */}
      <div
        className="absolute inset-0 bg-black/80 backdrop-blur-sm animate-fadeIn"
        onClick={onClose}
      />

      {/* Drawer Content */}
      <div
        className={`
          absolute top-0 ${positionClasses} h-full ${sizeClasses}
          bg-gradient-to-br from-codex-navy to-slate-900
          border-${position === 'left' ? 'r' : 'l'} border-codex-gold/30
          shadow-2xl
          transform transition-transform duration-300
          ${slideClasses}
          flex flex-col
        `}
      >
        {/* Header */}
        <div className="flex items-center justify-between px-6 py-4 border-b border-codex-gold/20">
          {title && <h2 className="text-xl font-serif text-codex-gold">{title}</h2>}
          <button
            onClick={onClose}
            className="ml-auto text-2xl text-codex-parchment/70 hover:text-codex-gold transition"
          >
            ✕
          </button>
        </div>

        {/* Body */}
        <div className="flex-1 overflow-y-auto px-6 py-4">
          {children}
        </div>

        {/* Footer */}
        {footer && (
          <div className="px-6 py-4 border-t border-codex-gold/20">
            {footer}
          </div>
        )}
      </div>
    </div>
  )
}

// Mini drawer for notifications/quick actions
export function MiniDrawer({
  isOpen,
  onClose,
  position = 'right',
  children,
}: {
  isOpen: boolean
  onClose: () => void
  position?: 'left' | 'right'
  children: ReactNode
}) {
  useEffect(() => {
    const handleEscape = (e: KeyboardEvent) => {
      if (e.key === 'Escape' && isOpen) {
        onClose()
      }
    }
    document.addEventListener('keydown', handleEscape)
    return () => document.removeEventListener('keydown', handleEscape)
  }, [isOpen, onClose])

  if (!isOpen) return null

  const positionClasses = {
    left: 'left-0',
    right: 'right-0',
  }[position]

  const slideClasses = {
    left: isOpen ? 'translate-x-0' : '-translate-x-full',
    right: isOpen ? 'translate-x-0' : 'translate-x-full',
  }[position]

  return (
    <>
      {/* Backdrop */}
      <div
        className="fixed inset-0 z-40 bg-black/40"
        onClick={onClose}
      />

      {/* Mini Drawer */}
      <div
        className={`
          fixed top-16 ${positionClasses} h-[calc(100vh-4rem)] w-72
          bg-codex-navy/95 backdrop-blur-sm
          border-${position === 'left' ? 'r' : 'l'} border-codex-gold/30
          shadow-xl
          transform transition-transform duration-200
          ${slideClasses}
          z-50
          overflow-y-auto
        `}
      >
        {children}
      </div>
    </>
  )
}

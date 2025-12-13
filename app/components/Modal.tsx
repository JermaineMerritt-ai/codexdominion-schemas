'use client'

import { ReactNode, useEffect } from 'react'

interface ModalProps {
  isOpen: boolean
  onClose: () => void
  title?: string
  size?: 'sm' | 'md' | 'lg' | 'xl' | 'full'
  children: ReactNode
  footer?: ReactNode
  closeOnBackdrop?: boolean
}

export default function Modal({
  isOpen,
  onClose,
  title,
  size = 'md',
  children,
  footer,
  closeOnBackdrop = true,
}: ModalProps) {
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
    sm: 'max-w-md',
    md: 'max-w-2xl',
    lg: 'max-w-4xl',
    xl: 'max-w-6xl',
    full: 'max-w-[95vw]',
  }[size]

  return (
    <div className="fixed inset-0 z-50 flex items-center justify-center p-4">
      {/* Backdrop */}
      <div
        className="absolute inset-0 bg-black/80 backdrop-blur-sm animate-fadeIn"
        onClick={closeOnBackdrop ? onClose : undefined}
      />

      {/* Modal Content */}
      <div
        className={`
          relative w-full ${sizeClasses}
          bg-gradient-to-br from-codex-navy to-slate-900
          border border-codex-gold/30
          rounded-lg shadow-2xl
          max-h-[90vh] overflow-hidden
          animate-scaleIn
        `}
      >
        {/* Header */}
        {title && (
          <div className="flex items-center justify-between px-6 py-4 border-b border-codex-gold/20">
            <h2 className="text-2xl font-serif text-codex-gold">{title}</h2>
            <button
              onClick={onClose}
              className="text-2xl text-codex-parchment/70 hover:text-codex-gold transition"
            >
              ✕
            </button>
          </div>
        )}

        {/* Body */}
        <div className="px-6 py-4 overflow-y-auto max-h-[calc(90vh-8rem)]">
          {children}
        </div>

        {/* Footer */}
        {footer && (
          <div className="flex items-center justify-end space-x-3 px-6 py-4 border-t border-codex-gold/20">
            {footer}
          </div>
        )}
      </div>
    </div>
  )
}

// Confirmation Modal Variant
export function ConfirmModal({
  isOpen,
  onClose,
  onConfirm,
  title = 'Confirm Action',
  message,
  confirmLabel = 'Confirm',
  cancelLabel = 'Cancel',
  variant = 'warning',
}: {
  isOpen: boolean
  onClose: () => void
  onConfirm: () => void
  title?: string
  message: string
  confirmLabel?: string
  cancelLabel?: string
  variant?: 'warning' | 'danger' | 'info'
}) {
  const getIcon = () => {
    switch (variant) {
      case 'warning': return '⚠️'
      case 'danger': return '🚨'
      case 'info': return 'ℹ️'
      default: return '❓'
    }
  }

  const getButtonClass = () => {
    switch (variant) {
      case 'danger':
        return 'bg-red-500/20 border-red-500/50 text-red-400 hover:bg-red-500/30'
      case 'warning':
        return 'bg-yellow-500/20 border-yellow-500/50 text-yellow-400 hover:bg-yellow-500/30'
      default:
        return 'codex-button'
    }
  }

  return (
    <Modal isOpen={isOpen} onClose={onClose} title={title} size="sm">
      <div className="text-center py-4">
        <div className="text-6xl mb-4">{getIcon()}</div>
        <p className="text-codex-parchment mb-6">{message}</p>
      </div>

      <div className="flex space-x-3">
        <button onClick={onClose} className="codex-button flex-1">
          {cancelLabel}
        </button>
        <button
          onClick={() => {
            onConfirm()
            onClose()
          }}
          className={`flex-1 ${getButtonClass()}`}
        >
          {confirmLabel}
        </button>
      </div>
    </Modal>
  )
}

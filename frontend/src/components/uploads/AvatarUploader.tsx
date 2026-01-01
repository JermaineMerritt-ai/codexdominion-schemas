'use client';

import React, { useState, useRef } from 'react';
import { uploadAvatar } from '@/lib/api/uploads';

export interface AvatarUploaderProps {
  currentAvatar?: string | null;
  onUploadSuccess?: (avatarUrl: string) => void;
  size?: 'sm' | 'md' | 'lg';
}

const sizeClasses = {
  sm: 'w-16 h-16',
  md: 'w-24 h-24',
  lg: 'w-32 h-32',
};

export default function AvatarUploader({
  currentAvatar,
  onUploadSuccess,
  size = 'md',
}: AvatarUploaderProps) {
  const [preview, setPreview] = useState<string | null>(currentAvatar || null);
  const [uploading, setUploading] = useState(false);
  const [error, setError] = useState<string | null>(null);
  const fileInputRef = useRef<HTMLInputElement>(null);

  const handleFileChange = async (e: React.ChangeEvent<HTMLInputElement>) => {
    const file = e.target.files?.[0];
    if (!file) return;

    // Validate file type
    if (!file.type.startsWith('image/')) {
      setError('Please select an image file');
      return;
    }

    // Validate file size (5MB max for avatar)
    const maxSize = 5 * 1024 * 1024;
    if (file.size > maxSize) {
      setError('Image must be less than 5MB');
      return;
    }

    // Show preview
    const reader = new FileReader();
    reader.onloadend = () => {
      setPreview(reader.result as string);
    };
    reader.readAsDataURL(file);

    // Upload
    setUploading(true);
    setError(null);

    try {
      const response = await uploadAvatar(file);
      if (onUploadSuccess) {
        onUploadSuccess(response.url);
      }
    } catch (err: any) {
      setError(err.message || 'Failed to upload avatar');
      setPreview(currentAvatar || null);
    } finally {
      setUploading(false);
    }
  };

  return (
    <div className="flex flex-col items-center space-y-4">
      {/* Avatar Display */}
      <div className={`relative ${sizeClasses[size]} group`}>
        <div
          className={`
            ${sizeClasses[size]} rounded-full overflow-hidden bg-gray-200
            border-4 border-white shadow-lg
          `}
        >
          {preview ? (
            <img src={preview} alt="Avatar" className="w-full h-full object-cover" />
          ) : (
            <div className="w-full h-full flex items-center justify-center text-gray-400 text-3xl">
              👤
            </div>
          )}
        </div>

        {/* Upload Overlay */}
        <div
          className={`
            absolute inset-0 ${sizeClasses[size]} rounded-full
            bg-black bg-opacity-50 opacity-0 group-hover:opacity-100
            transition-opacity cursor-pointer
            flex items-center justify-center
          `}
          onClick={() => fileInputRef.current?.click()}
        >
          <span className="text-white text-sm font-medium">
            {uploading ? '⏳' : '📷 Change'}
          </span>
        </div>

        <input
          ref={fileInputRef}
          type="file"
          accept="image/jpeg,image/png,image/webp,image/gif"
          onChange={handleFileChange}
          disabled={uploading}
          className="hidden"
        />
      </div>

      {/* Upload Button (Alternative) */}
      <button
        onClick={() => fileInputRef.current?.click()}
        disabled={uploading}
        className={`
          px-4 py-2 rounded-lg text-sm font-medium transition-colors
          ${
            uploading
              ? 'bg-gray-300 text-gray-500 cursor-not-allowed'
              : 'bg-blue-600 text-white hover:bg-blue-700'
          }
        `}
      >
        {uploading ? 'Uploading...' : 'Change Avatar'}
      </button>

      {/* Error Message */}
      {error && (
        <p className="text-sm text-red-600">❌ {error}</p>
      )}
    </div>
  );
}

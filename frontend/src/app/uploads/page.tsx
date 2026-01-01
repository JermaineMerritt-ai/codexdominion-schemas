'use client';

import React, { useState, useEffect } from 'react';
import { FileUploader, AvatarUploader } from '@/components/uploads';
import {
  uploadBatch,
  uploadMissionSubmission,
  uploadArtifact,
  getUploadStats,
  formatFileSize,
  UploadStats,
} from '@/lib/api/uploads';

export default function UploadsPage() {
  const [stats, setStats] = useState<UploadStats | null>(null);
  const [activeTab, setActiveTab] = useState<'avatar' | 'mission' | 'artifact' | 'batch'>('avatar');
  const [selectedMissionId, setSelectedMissionId] = useState('');
  const [selectedArtifactId, setSelectedArtifactId] = useState('');

  useEffect(() => {
    loadStats();
  }, []);

  const loadStats = async () => {
    try {
      const data = await getUploadStats();
      setStats(data);
    } catch (err) {
      console.error('Failed to load stats:', err);
    }
  };

  const handleBatchUpload = async (files: File[]) => {
    await uploadBatch(files);
    loadStats();
  };

  const handleMissionUpload = async (files: File[]) => {
    if (!selectedMissionId) {
      throw new Error('Please enter a mission ID');
    }
    await uploadMissionSubmission(selectedMissionId, files[0]);
    loadStats();
  };

  const handleArtifactUpload = async (files: File[]) => {
    if (!selectedArtifactId) {
      throw new Error('Please enter an artifact ID');
    }
    await uploadArtifact(selectedArtifactId, files[0]);
    loadStats();
  };

  const handleAvatarSuccess = (url: string) => {
    console.log('Avatar uploaded:', url);
    loadStats();
  };

  return (
    <div className="min-h-screen bg-gray-50 py-8 px-4">
      <div className="max-w-4xl mx-auto">
        {/* Header */}
        <div className="mb-8">
          <h1 className="text-3xl font-bold text-gray-900 mb-2">📤 File Uploads</h1>
          <p className="text-gray-600">Upload avatars, mission submissions, artifacts, and more</p>
        </div>

        {/* Stats Card */}
        {stats && (
          <div className="bg-white rounded-lg shadow p-6 mb-6">
            <h2 className="text-lg font-semibold text-gray-900 mb-4">📊 Upload Statistics</h2>
            <div className="grid grid-cols-3 gap-4">
              <div className="text-center">
                <div className="text-2xl font-bold text-blue-600">{stats.totalUploads}</div>
                <div className="text-sm text-gray-500">Total Uploads</div>
              </div>
              <div className="text-center">
                <div className="text-2xl font-bold text-green-600">
                  {formatFileSize(stats.totalSize)}
                </div>
                <div className="text-sm text-gray-500">Total Size</div>
              </div>
              <div className="text-center">
                <div className="text-2xl font-bold text-purple-600">
                  {Object.keys(stats.byType).length}
                </div>
                <div className="text-sm text-gray-500">File Types</div>
              </div>
            </div>
          </div>
        )}

        {/* Tab Navigation */}
        <div className="bg-white rounded-t-lg shadow overflow-hidden">
          <div className="flex border-b border-gray-200">
            <button
              onClick={() => setActiveTab('avatar')}
              className={`
                flex-1 px-4 py-3 text-sm font-medium transition-colors
                ${
                  activeTab === 'avatar'
                    ? 'bg-blue-50 text-blue-600 border-b-2 border-blue-600'
                    : 'text-gray-500 hover:text-gray-700 hover:bg-gray-50'
                }
              `}
            >
              👤 Avatar
            </button>
            <button
              onClick={() => setActiveTab('mission')}
              className={`
                flex-1 px-4 py-3 text-sm font-medium transition-colors
                ${
                  activeTab === 'mission'
                    ? 'bg-blue-50 text-blue-600 border-b-2 border-blue-600'
                    : 'text-gray-500 hover:text-gray-700 hover:bg-gray-50'
                }
              `}
            >
              🎯 Mission
            </button>
            <button
              onClick={() => setActiveTab('artifact')}
              className={`
                flex-1 px-4 py-3 text-sm font-medium transition-colors
                ${
                  activeTab === 'artifact'
                    ? 'bg-blue-50 text-blue-600 border-b-2 border-blue-600'
                    : 'text-gray-500 hover:text-gray-700 hover:bg-gray-50'
                }
              `}
            >
              🎨 Artifact
            </button>
            <button
              onClick={() => setActiveTab('batch')}
              className={`
                flex-1 px-4 py-3 text-sm font-medium transition-colors
                ${
                  activeTab === 'batch'
                    ? 'bg-blue-50 text-blue-600 border-b-2 border-blue-600'
                    : 'text-gray-500 hover:text-gray-700 hover:bg-gray-50'
                }
              `}
            >
              📦 Batch Upload
            </button>
          </div>

          {/* Tab Content */}
          <div className="p-6">
            {activeTab === 'avatar' && (
              <div className="space-y-4">
                <h3 className="text-lg font-semibold text-gray-900">Upload Profile Avatar</h3>
                <p className="text-sm text-gray-600">
                  Upload or change your profile picture. Supported formats: JPG, PNG, WebP, GIF. Max size: 5MB.
                </p>
                <AvatarUploader size="lg" onUploadSuccess={handleAvatarSuccess} />
              </div>
            )}

            {activeTab === 'mission' && (
              <div className="space-y-4">
                <h3 className="text-lg font-semibold text-gray-900">Upload Mission Submission</h3>
                <p className="text-sm text-gray-600">
                  Upload files as part of your mission submission. Supported: Images, PDFs, Word documents.
                </p>
                <div className="mb-4">
                  <label className="block text-sm font-medium text-gray-700 mb-2">
                    Mission ID *
                  </label>
                  <input
                    type="text"
                    value={selectedMissionId}
                    onChange={(e) => setSelectedMissionId(e.target.value)}
                    placeholder="Enter mission ID"
                    className="w-full px-4 py-2 border border-gray-300 rounded-lg focus:ring-2 focus:ring-blue-500 focus:border-transparent"
                  />
                </div>
                <FileUploader
                  accept="image/*,.pdf,.doc,.docx"
                  onUpload={handleMissionUpload}
                  uploadButtonText="Submit Mission File"
                  dropzoneText="Upload your mission submission file"
                />
              </div>
            )}

            {activeTab === 'artifact' && (
              <div className="space-y-4">
                <h3 className="text-lg font-semibold text-gray-900">Upload Creator Artifact</h3>
                <p className="text-sm text-gray-600">
                  Upload files for your creator artifact. Supported: Images, videos, PDFs, ZIP files.
                </p>
                <div className="mb-4">
                  <label className="block text-sm font-medium text-gray-700 mb-2">
                    Artifact ID *
                  </label>
                  <input
                    type="text"
                    value={selectedArtifactId}
                    onChange={(e) => setSelectedArtifactId(e.target.value)}
                    placeholder="Enter artifact ID"
                    className="w-full px-4 py-2 border border-gray-300 rounded-lg focus:ring-2 focus:ring-blue-500 focus:border-transparent"
                  />
                </div>
                <FileUploader
                  accept="image/*,video/*,.pdf,.zip"
                  onUpload={handleArtifactUpload}
                  uploadButtonText="Upload Artifact"
                  dropzoneText="Upload your creator artifact file"
                />
              </div>
            )}

            {activeTab === 'batch' && (
              <div className="space-y-4">
                <h3 className="text-lg font-semibold text-gray-900">Batch Upload Files</h3>
                <p className="text-sm text-gray-600">
                  Upload multiple files at once. Max 10 files, 50MB each.
                </p>
                <FileUploader
                  multiple
                  onUpload={handleBatchUpload}
                  uploadButtonText="Upload All Files"
                  dropzoneText="Drop multiple files here to upload in batch"
                />
              </div>
            )}
          </div>
        </div>

        {/* Info Section */}
        <div className="mt-6 bg-blue-50 border border-blue-200 rounded-lg p-4">
          <h3 className="text-sm font-semibold text-blue-900 mb-2">ℹ️ Upload Guidelines</h3>
          <ul className="text-sm text-blue-800 space-y-1">
            <li>• Maximum file size: 50MB per file</li>
            <li>• Avatar uploads support: JPG, PNG, WebP, GIF (5MB max)</li>
            <li>• Mission submissions support: Images, PDF, Word documents</li>
            <li>• Artifacts support: Images, videos, PDF, ZIP files</li>
            <li>• Batch uploads: Up to 10 files at once</li>
          </ul>
        </div>
      </div>
    </div>
  );
}

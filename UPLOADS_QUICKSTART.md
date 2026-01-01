# 🚀 Upload System - Quick Start Guide

## ✅ What's Been Added

The **complete upload system** has been integrated with:

### Backend (Already Implemented)
- ✅ 7 REST API endpoints in `backend/src/uploads/`
- ✅ File validation (size, type)
- ✅ JWT authentication
- ✅ Static file serving at `/uploads/`
- ✅ UploadsModule registered in app.module.ts

### Frontend (NEW - Just Added)
- ✅ **API Client** (`frontend/src/lib/api/uploads.ts`) - 7 upload functions + utilities
- ✅ **FileUploader Component** (`frontend/src/components/uploads/FileUploader.tsx`) - Drag & drop uploader
- ✅ **AvatarUploader Component** (`frontend/src/components/uploads/AvatarUploader.tsx`) - Profile picture uploader
- ✅ **Uploads Page** (`frontend/src/app/uploads/page.tsx`) - Demo page with all upload types

---

## 📦 Files Created (Just Now)

```
frontend/src/
├─ lib/api/uploads.ts                      # API client (7 functions)
├─ components/uploads/
│  ├─ FileUploader.tsx                     # Generic file uploader
│  ├─ AvatarUploader.tsx                   # Avatar uploader component
│  └─ index.ts                             # Component exports
└─ app/uploads/page.tsx                    # Demo/test page

docs/technical/UPLOADS_SYSTEM.md           # Complete documentation
```

---

## 🎯 How to Use

### 1. In Your Components

**Upload Avatar:**
```tsx
import { AvatarUploader } from '@/components/uploads';

<AvatarUploader
  currentAvatar={user?.avatar}
  size="lg"
  onUploadSuccess={(url) => {
    console.log('New avatar:', url);
    // Update user profile
  }}
/>
```

**Upload Files:**
```tsx
import { FileUploader } from '@/components/uploads';
import { uploadMissionSubmission } from '@/lib/api/uploads';

<FileUploader
  accept="image/*,.pdf,.doc,.docx"
  onUpload={async (files) => {
    await uploadMissionSubmission(missionId, files[0]);
  }}
  uploadButtonText="Submit Mission"
/>
```

**Direct API Calls:**
```tsx
import { 
  uploadAvatar, 
  uploadBatch, 
  getUploadStats 
} from '@/lib/api/uploads';

// Upload single file
const response = await uploadAvatar(file);
console.log('Uploaded to:', response.url);

// Batch upload
const batchResponse = await uploadBatch([file1, file2, file3]);
console.log('Uploaded', batchResponse.count, 'files');

// Get stats
const stats = await getUploadStats();
console.log('Total uploads:', stats.totalUploads);
```

---

## 🧪 Test the System

### Option 1: Visit Demo Page
1. Start backend: `cd backend && npm run start:dev`
2. Start frontend: `cd frontend && npm run dev`
3. Navigate to: `http://localhost:3000/uploads`
4. Try all 4 tabs: Avatar, Mission, Artifact, Batch

### Option 2: Test with curl
```bash
# Upload avatar
curl -X POST http://localhost:4000/api/v1/uploads/avatar \
  -H "Authorization: Bearer YOUR_TOKEN" \
  -F "file=@avatar.jpg"

# Batch upload
curl -X POST http://localhost:4000/api/v1/uploads/batch \
  -H "Authorization: Bearer YOUR_TOKEN" \
  -F "files=@file1.pdf" \
  -F "files=@file2.png"

# Get stats
curl http://localhost:4000/api/v1/uploads/stats \
  -H "Authorization: Bearer YOUR_TOKEN"
```

---

## 📋 Available API Endpoints

| Endpoint | Method | Purpose | Max Size |
|----------|--------|---------|----------|
| `/uploads/avatar` | POST | Upload user avatar | 50MB |
| `/uploads/artifact/:id` | POST | Upload creator artifact | 50MB |
| `/uploads/mission/:id/submission` | POST | Upload mission file | 50MB |
| `/uploads/culture/story/:id` | POST | Upload story image | 50MB |
| `/uploads/batch` | POST | Batch upload (max 10) | 50MB each |
| `/uploads/stats` | GET | Get upload statistics | - |
| `/uploads/:filename` | DELETE | Delete file | - |

---

## 🛡️ Security Features

- ✅ JWT authentication required
- ✅ File size validation (50MB max)
- ✅ MIME type validation (server-side)
- ✅ Unique filename generation (no overwrites)
- ✅ User ID tracking (from JWT token)
- ✅ Isolated storage directory

---

## 📁 Supported File Types

**Avatars**: JPG, PNG, WebP, GIF  
**Artifacts**: Images, videos (MP4, WebM), PDF, ZIP  
**Missions**: Images, PDF, Word (DOC, DOCX)  
**Stories**: JPG, PNG, WebP  
**Batch**: Any document type

---

## 🔧 Integration Examples

### In Profile Page
```tsx
// app/profile/page.tsx
import { AvatarUploader } from '@/components/uploads';

export default function ProfilePage() {
  const handleAvatarUpdate = async (url: string) => {
    // Update user in database
    await updateUserProfile({ avatar: url });
  };

  return (
    <div>
      <h1>My Profile</h1>
      <AvatarUploader 
        currentAvatar={user.avatar}
        onUploadSuccess={handleAvatarUpdate}
      />
    </div>
  );
}
```

### In Mission Submission Form
```tsx
// components/MissionForm.tsx
import { FileUploader } from '@/components/uploads';
import { uploadMissionSubmission } from '@/lib/api/uploads';

export default function MissionForm({ missionId }) {
  const handleSubmit = async (files: File[]) => {
    const response = await uploadMissionSubmission(missionId, files[0]);
    // Save submission with file URL
    await createSubmission({
      missionId,
      fileUrl: response.url,
      fileName: response.originalName
    });
  };

  return (
    <FileUploader
      accept="image/*,.pdf"
      onUpload={handleSubmit}
      uploadButtonText="Submit Mission"
    />
  );
}
```

### In Creator Dashboard
```tsx
// app/creators/new-artifact/page.tsx
import { FileUploader } from '@/components/uploads';
import { uploadArtifact } from '@/lib/api/uploads';

export default function NewArtifactPage() {
  const [artifactId, setArtifactId] = useState('');

  const handleUpload = async (files: File[]) => {
    const response = await uploadArtifact(artifactId, files[0]);
    console.log('Artifact uploaded:', response);
  };

  return (
    <div>
      <input 
        value={artifactId} 
        onChange={(e) => setArtifactId(e.target.value)}
        placeholder="Artifact ID"
      />
      <FileUploader
        accept="image/*,video/*,.pdf,.zip"
        onUpload={handleUpload}
      />
    </div>
  );
}
```

---

## 🎨 Component Customization

### FileUploader Props
```tsx
interface FileUploaderProps {
  accept?: string;              // MIME types (default: '*/*')
  maxSize?: number;             // Bytes (default: 50MB)
  multiple?: boolean;           // Allow multiple files (default: false)
  onUpload: (files: File[]) => Promise<void>;
  uploadButtonText?: string;    // Custom button text
  dropzoneText?: string;        // Custom dropzone text
  disabled?: boolean;           // Disable uploads
}
```

### AvatarUploader Props
```tsx
interface AvatarUploaderProps {
  currentAvatar?: string | null;  // Current avatar URL
  onUploadSuccess?: (url: string) => void;
  size?: 'sm' | 'md' | 'lg';      // Avatar size
}
```

---

## 🐛 Troubleshooting

**Issue: "Not authenticated" error**  
Solution: Ensure user is logged in and token is in localStorage

**Issue: Files not showing up**  
Solution: Check backend `uploads/` directory exists and is writable

**Issue: "File too large" error**  
Solution: Reduce file size or increase backend limit in `uploads.module.ts`

**Issue: Upload button doesn't work**  
Solution: Check browser console for errors, verify API URL in `.env.local`

**Issue: CORS error**  
Solution: Ensure backend has `app.enableCors()` in `main.ts` (already added)

---

## 📝 Next Steps

1. **Test the system**: Visit `/uploads` page
2. **Integrate into your pages**: Add AvatarUploader to profile, FileUploader to forms
3. **Customize styling**: Update Tailwind classes to match your design
4. **Add file preview**: Extend FileUploader with image/video preview
5. **Add progress bars**: Implement upload progress tracking

---

## 📚 Documentation

- **Full Technical Docs**: `docs/technical/UPLOADS_SYSTEM.md`
- **API Reference**: http://localhost:4000/api-docs (Swagger)
- **Backend Code**: `backend/src/uploads/`
- **Frontend Code**: `frontend/src/components/uploads/`

---

**🔥 The Upload System is Complete and Ready! 📤**


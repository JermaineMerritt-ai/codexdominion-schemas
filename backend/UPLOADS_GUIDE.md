# 📤 Upload System - Complete Guide

## Overview

The CodexDominion upload system provides secure file upload functionality with type validation, size limits, and integration with existing modules.

---

## Features

✅ **Multiple Upload Types**
- User avatars (profile pictures)
- Creator artifacts (images, videos, documents)
- Mission submissions (documents, images)
- Cultural story images
- Event materials
- General documents

✅ **Security**
- JWT authentication required
- File type validation (MIME types)
- Size limits (50MB max)
- Unique filename generation

✅ **Storage**
- Local disk storage (`./uploads/` directory)
- Static file serving via `/uploads/` URL
- Easy migration to cloud storage (S3, Azure Blob, etc.)

---

## Endpoints

### 1. Upload Avatar
```http
POST /api/v1/uploads/avatar
Authorization: Bearer {JWT_TOKEN}
Content-Type: multipart/form-data

Body:
- file: image file (JPEG, PNG, WebP, GIF)
```

**Response:**
```json
{
  "id": "upload_1735598400000",
  "userId": "user-uuid",
  "type": "avatar",
  "originalName": "profile.jpg",
  "mimeType": "image/jpeg",
  "size": 102400,
  "path": "file-1735598400000-123456789.jpg",
  "url": "/uploads/file-1735598400000-123456789.jpg",
  "uploadedAt": "2025-12-30T22:00:00.000Z"
}
```

### 2. Upload Creator Artifact
```http
POST /api/v1/uploads/artifact/:artifactId
Authorization: Bearer {JWT_TOKEN}
Content-Type: multipart/form-data

Body:
- file: artifact file (images, videos, PDFs, ZIP)
```

### 3. Upload Mission Submission
```http
POST /api/v1/uploads/mission/:missionId/submission
Authorization: Bearer {JWT_TOKEN}
Content-Type: multipart/form-data

Body:
- file: submission file (images, PDFs, Word docs)
```

### 4. Upload Cultural Story Image
```http
POST /api/v1/uploads/culture/story/:storyId
Authorization: Bearer {JWT_TOKEN}
Content-Type: multipart/form-data

Body:
- file: image file (JPEG, PNG, WebP)
```

### 5. Batch Upload (Multiple Files)
```http
POST /api/v1/uploads/batch
Authorization: Bearer {JWT_TOKEN}
Content-Type: multipart/form-data

Body:
- files: array of files (max 10 files)
```

**Response:**
```json
{
  "count": 3,
  "uploads": [
    { "id": "...", "url": "/uploads/..." },
    { "id": "...", "url": "/uploads/..." },
    { "id": "...", "url": "/uploads/..." }
  ]
}
```

### 6. Get Upload Statistics
```http
GET /api/v1/uploads/stats
Authorization: Bearer {JWT_TOKEN}
```

**Response:**
```json
{
  "totalUploads": 15,
  "totalSize": 5242880,
  "byType": {
    "avatar": 1,
    "artifact": 10,
    "mission_submission": 4
  }
}
```

### 7. Delete File
```http
DELETE /api/v1/uploads/:filename
Authorization: Bearer {JWT_TOKEN}
```

---

## File Type Restrictions

### Avatar
- **Allowed**: `image/jpeg`, `image/png`, `image/webp`, `image/gif`
- **Max Size**: 50MB

### Creator Artifact
- **Allowed**: 
  - Images: `image/jpeg`, `image/png`, `image/webp`, `image/gif`
  - Videos: `video/mp4`, `video/webm`
  - Documents: `application/pdf`, `application/zip`
- **Max Size**: 50MB

### Mission Submission
- **Allowed**:
  - Images: `image/jpeg`, `image/png`, `image/webp`
  - Documents: `application/pdf`, `application/msword`, `application/vnd.openxmlformats-officedocument.wordprocessingml.document`
- **Max Size**: 50MB

### Cultural Story
- **Allowed**: `image/jpeg`, `image/png`, `image/webp`
- **Max Size**: 50MB

### Event Material
- **Allowed**:
  - Images: `image/jpeg`, `image/png`, `image/webp`
  - Videos: `video/mp4`
  - Documents: `application/pdf`
- **Max Size**: 50MB

### General Document
- **Allowed**:
  - PDFs: `application/pdf`
  - Word: `application/msword`, `application/vnd.openxmlformats-officedocument.wordprocessingml.document`
  - Excel: `application/vnd.ms-excel`, `application/vnd.openxmlformats-officedocument.spreadsheetml.sheet`
- **Max Size**: 50MB

---

## Testing with PowerShell

### 1. Upload Avatar
```powershell
# Login first
$credentials = @{ email = "admin@codexdominion.com"; password = "password123" } | ConvertTo-Json
$response = Invoke-RestMethod -Uri "http://localhost:8080/api/v1/auth/login" `
  -Method POST -Body $credentials -ContentType "application/json"
$token = $response.accessToken

# Upload avatar
$headers = @{ Authorization = "Bearer $token" }
$filePath = "C:\path\to\avatar.jpg"
$form = @{
  file = Get-Item -Path $filePath
}

Invoke-RestMethod -Uri "http://localhost:8080/api/v1/uploads/avatar" `
  -Method POST -Headers $headers -Form $form
```

### 2. Upload Artifact
```powershell
$artifactId = "artifact-uuid-here"
$filePath = "C:\path\to\artifact.pdf"
$form = @{
  file = Get-Item -Path $filePath
}

Invoke-RestMethod -Uri "http://localhost:8080/api/v1/uploads/artifact/$artifactId" `
  -Method POST -Headers $headers -Form $form
```

### 3. Batch Upload
```powershell
$files = @(
  Get-Item "C:\path\to\file1.jpg"
  Get-Item "C:\path\to\file2.pdf"
  Get-Item "C:\path\to\file3.docx"
)

$form = @{
  files = $files
}

Invoke-RestMethod -Uri "http://localhost:8080/api/v1/uploads/batch" `
  -Method POST -Headers $headers -Form $form
```

### 4. Get Upload Stats
```powershell
Invoke-RestMethod -Uri "http://localhost:8080/api/v1/uploads/stats" `
  -Method GET -Headers $headers
```

### 5. Delete File
```powershell
$filename = "file-1735598400000-123456789.jpg"
Invoke-RestMethod -Uri "http://localhost:8080/api/v1/uploads/$filename" `
  -Method DELETE -Headers $headers
```

---

## Testing with cURL

### Upload Avatar
```bash
curl -X POST http://localhost:8080/api/v1/uploads/avatar \
  -H "Authorization: Bearer YOUR_JWT_TOKEN" \
  -F "file=@/path/to/avatar.jpg"
```

### Upload Artifact
```bash
curl -X POST http://localhost:8080/api/v1/uploads/artifact/ARTIFACT_ID \
  -H "Authorization: Bearer YOUR_JWT_TOKEN" \
  -F "file=@/path/to/artifact.pdf"
```

### Batch Upload
```bash
curl -X POST http://localhost:8080/api/v1/uploads/batch \
  -H "Authorization: Bearer YOUR_JWT_TOKEN" \
  -F "files=@/path/to/file1.jpg" \
  -F "files=@/path/to/file2.pdf" \
  -F "files=@/path/to/file3.docx"
```

---

## Integration with Existing Modules

### User Profile (Avatar)
When avatar is uploaded, the user's profile is automatically updated:
```typescript
await prisma.profile.update({
  where: { userId },
  data: { avatar: uploadUrl }
});
```

### Creator Artifacts
Artifact file URL is automatically saved:
```typescript
await prisma.artifact.update({
  where: { id: artifactId },
  data: { fileUrl: uploadUrl }
});
```

### Cultural Stories
Story image URL is automatically saved:
```typescript
await prisma.culturalStory.update({
  where: { id: storyId },
  data: { imageUrl: uploadUrl }
});
```

---

## Cloud Storage Migration (Future)

The service is designed for easy cloud migration:

### AWS S3
```typescript
import { S3 } from 'aws-sdk';

const s3 = new S3({
  accessKeyId: process.env.AWS_ACCESS_KEY_ID,
  secretAccessKey: process.env.AWS_SECRET_ACCESS_KEY,
  region: process.env.AWS_REGION,
});

await s3.upload({
  Bucket: 'codexdominion-uploads',
  Key: filename,
  Body: file.buffer,
  ACL: 'public-read',
}).promise();
```

### Azure Blob Storage
```typescript
import { BlobServiceClient } from '@azure/storage-blob';

const blobServiceClient = BlobServiceClient.fromConnectionString(
  process.env.AZURE_STORAGE_CONNECTION_STRING
);
const containerClient = blobServiceClient.getContainerClient('uploads');
const blockBlobClient = containerClient.getBlockBlobClient(filename);
await blockBlobClient.uploadData(file.buffer);
```

---

## Error Handling

### File Too Large
```json
{
  "statusCode": 400,
  "message": "File size exceeds maximum allowed size of 50MB",
  "error": "Bad Request"
}
```

### Invalid File Type
```json
{
  "statusCode": 400,
  "message": "File type video/avi is not allowed for avatar. Allowed types: image/jpeg, image/png, image/webp, image/gif",
  "error": "Bad Request"
}
```

### No File Uploaded
```json
{
  "statusCode": 400,
  "message": "No file uploaded",
  "error": "Bad Request"
}
```

### Unauthorized
```json
{
  "statusCode": 401,
  "message": "Unauthorized",
  "error": "Unauthorized"
}
```

---

## Security Best Practices

1. **Always Validate JWT Token** - All upload endpoints require authentication
2. **Check File Types** - Only allowed MIME types are accepted
3. **Enforce Size Limits** - 50MB maximum per file
4. **Unique Filenames** - Prevents overwrites with timestamp + random suffix
5. **User Association** - All uploads are linked to authenticated user

---

## Next Steps

1. ✅ **Rebuild Backend**: `npm run build`
2. ✅ **Restart Server**: `node dist/main.js`
3. ✅ **Test Uploads**: Use PowerShell or cURL examples above
4. ✅ **Check Swagger**: http://localhost:8080/api-docs (see Uploads section)
5. 🔄 **Add Database Tracking**: Store upload metadata in Prisma (optional)
6. 🔄 **Migrate to Cloud**: Configure S3/Azure for production (optional)

---

**🔥 The Upload System is Ready! 👑**

All upload endpoints are secured, validated, and ready for production use.

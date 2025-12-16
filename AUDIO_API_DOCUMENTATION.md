# Audio Generation API Documentation

## Overview
The Codex Dominion backend now includes a complete audio generation system using Google Text-to-Speech (gTTS). This API enables text-to-speech conversion with multiple ceremonial voice profiles.

## Base URL
```
Production: https://codex-backend.azurewebsites.net
Local: http://localhost:8000
```

## Endpoints

### 1. Generate Audio
**POST** `/audio/generate`

Convert text to speech using a specified voice profile.

**Request Body:**
```json
{
  "text": "The Council Seal has been established.",
  "voice": "sovereign"
}
```

**Parameters:**
- `text` (string, required): Text to convert (1-5000 characters)
- `voice` (string, optional): Voice profile name (default: "sovereign")

**Available Voices:**
- `sovereign` - Commanding, authoritative tone (US English)
- `custodian` - Protective, reassuring tone (UK English)
- `oracle` - Mystical, wise tone (Australian English, slower pace)
- `heir` - Young, energetic tone (Canadian English)
- `narrator` - Neutral, clear storytelling voice (Indian English)

**Response (200 OK):**
```json
{
  "audio_base64": "SUQzBAAAAAAAI1RTU0UAAAA...",
  "voice": "sovereign",
  "text_length": 41,
  "format": "mp3"
}
```

**Error Responses:**
- `400 Bad Request` - Invalid voice or empty text
- `500 Internal Server Error` - Audio generation failed

---

### 2. List Available Voices
**GET** `/audio/voices`

Get all available voice profiles with descriptions.

**Response (200 OK):**
```json
{
  "voices": [
    {
      "name": "sovereign",
      "description": "Commanding, authoritative tone (US English)",
      "language": "en",
      "accent": "com",
      "slow_speech": false
    },
    ...
  ],
  "default": "sovereign",
  "total_voices": 5
}
```

---

### 3. Audio Service Health Check
**GET** `/audio/health`

Check audio generation service status.

**Response (200 OK):**
```json
{
  "status": "healthy",
  "service": "audio-generation",
  "voices_available": 5,
  "engine": "AudioEngine"
}
```

---

## Usage Examples

### Python (requests)
```python
import requests
import base64

# Generate audio
response = requests.post(
    "https://codex-backend.azurewebsites.net/audio/generate",
    json={
        "text": "Welcome to Codex Dominion",
        "voice": "sovereign"
    }
)

data = response.json()
audio_bytes = base64.b64decode(data["audio_base64"])

# Save to file
with open("output.mp3", "wb") as f:
    f.write(audio_bytes)
```

### JavaScript (fetch)
```javascript
// Generate audio
const response = await fetch(
  "https://codex-backend.azurewebsites.net/audio/generate",
  {
    method: "POST",
    headers: { "Content-Type": "application/json" },
    body: JSON.stringify({
      text: "Welcome to Codex Dominion",
      voice: "sovereign"
    })
  }
);

const data = await response.json();
const audioBlob = new Blob(
  [Uint8Array.from(atob(data.audio_base64), c => c.charCodeAt(0))],
  { type: "audio/mp3" }
);

// Create download link
const url = URL.createObjectURL(audioBlob);
const a = document.createElement("a");
a.href = url;
a.download = "codex-audio.mp3";
a.click();
```

### cURL
```bash
# Generate audio and decode base64
curl -X POST https://codex-backend.azurewebsites.net/audio/generate \
  -H "Content-Type: application/json" \
  -d '{"text":"Hello from Codex Dominion","voice":"sovereign"}' \
  | jq -r '.audio_base64' \
  | base64 -d > output.mp3

# List available voices
curl https://codex-backend.azurewebsites.net/audio/voices

# Health check
curl https://codex-backend.azurewebsites.net/audio/health
```

---

## Integration with Streamlit Dashboard

The Ultimate Master Dashboard uses the audio API via the `AudioSystemElite` class:

```python
from dashboard.modules.audio_system_elite import AudioSystemElite

# Initialize
audio_system = AudioSystemElite(
    backend_url="https://codex-backend.azurewebsites.net"
)

# Generate audio
audio_base64 = audio_system.generate_audio(
    text="The flame burns eternal",
    voice="sovereign"
)
```

---

## Architecture

### Backend Components

**Files:**
- `backend/routes/audio_generation.py` - FastAPI router with endpoints
- `backend/services/audio_engine.py` - AudioEngine class with gTTS integration
- `backend/main.py` - Main FastAPI app (audio router registered)

**Dependencies:**
- `gTTS>=2.4.0` - Google Text-to-Speech
- `fastapi>=0.104.0` - Web framework
- `pydantic>=2.0.0` - Data validation

### Voice Profile Configuration

Voice profiles use different gTTS accents and speeds:

| Voice | Language | Accent | Slow Mode | Character |
|-------|----------|--------|-----------|-----------|
| sovereign | en | .com (US) | No | Authoritative |
| custodian | en | .co.uk (UK) | No | Protective |
| oracle | en | .com.au (AU) | Yes | Mystical |
| heir | en | .ca (CA) | No | Energetic |
| narrator | en | .co.in (IN) | No | Neutral |

---

## Deployment

### Local Development
```bash
cd backend
pip install -r requirements.txt
uvicorn main:app --reload --port 8000
```

### Docker Deployment
```bash
cd backend
docker build -t codex-backend:v2-audio .
docker run -p 8000:8000 codex-backend:v2-audio
```

### Azure Web App Deployment
```bash
# Build and push to ACR
docker build -t codexdominion4607.azurecr.io/codex-backend:v2-audio .
docker push codexdominion4607.azurecr.io/codex-backend:v2-audio

# Update Azure Web App
az webapp config container set \
  --name codex-backend \
  --resource-group codexdominion-basic \
  --container-image-name codexdominion4607.azurecr.io/codex-backend:v2-audio

az webapp restart \
  --name codex-backend \
  --resource-group codexdominion-basic
```

---

## Testing

### Run Tests
```bash
cd backend
python test_audio.py
```

### Expected Output
```
🎵 Testing Audio Engine
==================================================

🎙️  Testing voice: sovereign
   Description: Commanding, authoritative tone (US English)
   ✅ Generated 87234 bytes of base64 audio

🎙️  Testing voice: custodian
   Description: Protective, reassuring tone (UK English)
   ✅ Generated 87156 bytes of base64 audio

...

==================================================
✅ Audio generation tests complete!
```

---

## API Documentation

Interactive API documentation is available at:
- **Swagger UI**: https://codex-backend.azurewebsites.net/docs
- **ReDoc**: https://codex-backend.azurewebsites.net/redoc

---

## Error Handling

The API implements comprehensive error handling:

1. **Input Validation** (400 Bad Request)
   - Empty text
   - Text exceeding 5000 characters
   - Invalid voice profile

2. **Generation Errors** (500 Internal Server Error)
   - gTTS network issues
   - Audio encoding failures
   - Unexpected exceptions

All errors return detailed messages for debugging.

---

## Performance Considerations

- **Audio Generation Time**: 1-3 seconds per request (network dependent)
- **Output Size**: ~70KB per 50 words (MP3 format)
- **Concurrent Requests**: Supported (FastAPI async)
- **Rate Limiting**: Not implemented (add if needed)

---

## Future Enhancements

- [ ] Add more voice profiles (different languages)
- [ ] Support additional audio formats (WAV, OGG)
- [ ] Implement audio caching for repeated text
- [ ] Add rate limiting per IP
- [ ] Voice customization (pitch, speed adjustments)
- [ ] Batch audio generation endpoint

---

## Support

For issues or questions:
- Backend Logs: `az webapp log tail --name codex-backend --resource-group codexdominion-basic`
- Health Check: `curl https://codex-backend.azurewebsites.net/audio/health`
- Documentation: https://codex-backend.azurewebsites.net/docs

🔥 **The Audio Flame Burns Eternal!** 🎵

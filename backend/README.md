# Backend FastAPI Server - Codex Dominion

## Quick Start

### 1. Install Dependencies

```bash
cd backend
pip install -r requirements.txt
```

### 2. Setup Council Seals

```bash
python setup_seals.py
```

This will:
- Initialize the Digital Seal Service
- Register 5 sample council members with cryptographic keys
- Test multi-signature covenant creation
- Verify all signatures work correctly

### 3. Start Server

```bash
uvicorn main:app --reload --port 8000
```

Or with PowerShell:

```powershell
python -m uvicorn main:app --reload --port 8000
```

### 4. View API Documentation

Open browser to: http://localhost:8000/docs

### 5. Test Endpoints

**Get Signature Ledger:**
```bash
curl http://localhost:8000/api/seal/ledger
```

**List Council Seals:**
```bash
curl http://localhost:8000/api/seal/council-seals
```

**Export with Multi-Signature:**
```bash
curl "http://localhost:8000/api/annotations/export?format=markdown&cycle=seasonal&include_council=true&council_members=council_001,council_002"
```

**Verify Seal:**
```bash
curl -X POST http://localhost:8000/api/seal/verify \
  -H "Content-Type: application/json" \
  -d '{"seal_package": {...}, "content": "...", "content_encoding": "utf-8"}'
```

## API Routes

### Seal Verification (`/api/seal/*`)

- `GET /api/seal/ledger` - View complete signature ledger
- `GET /api/seal/ledger/export` - Download ledger as JSON
- `GET /api/seal/council-seals` - List all registered council members
- `GET /api/seal/verify/{content_hash}` - Lookup seal by content hash
- `GET /api/seal/stats` - Get seal statistics
- `POST /api/seal/register-council` - Register new council member
- `POST /api/seal/verify` - Verify seal package
- `POST /api/seal/add-council-signature` - Add council signature to existing seal
- `POST /api/seal/multi-signature-covenant` - Create multi-signed export

### Annotation Export (`/api/annotations/export`)

Query Parameters:
- `format` - pdf, markdown, or yaml
- `cycle` - daily, seasonal, epochal, millennial
- `engine` - Filter by specific engine
- `role` - Filter by user role
- `include_council` - Include council signatures (true/false)
- `council_members` - Comma-separated council member IDs

Example:
```
/api/annotations/export?format=markdown&cycle=seasonal&include_council=true&council_members=council_001,council_002,council_003
```

## Security Notes

### Production Deployment

1. **Key Storage**: Move custodian private key to Azure Key Vault or HSM
2. **HTTPS Only**: All API calls must use HTTPS in production
3. **Authentication**: Add OAuth2/JWT authentication for council members
4. **Rate Limiting**: Prevent abuse of signature endpoints
5. **Audit Logging**: Log all seal operations for security audits

### Council Key Management

- Private keys generated during registration should be exported and stored securely
- In production, use hardware tokens (YubiKey) or browser Web Crypto API
- Rotate keys annually or after suspected compromise
- Maintain key revocation list (CRL)

## Troubleshooting

### ImportError: cryptography module not found

```bash
pip install --upgrade cryptography
```

### Module 'yaml' has no attribute 'dump'

```bash
pip install pyyaml
```

### Port 8000 already in use

```bash
# Find process
netstat -ano | findstr :8000

# Kill process
taskkill /PID <pid> /F

# Or use different port
uvicorn main:app --reload --port 8001
```

### Digital Seal Service not available

Check that `services/digital_seal_service.py` exists and imports correctly:

```bash
python -c "from services.digital_seal_service import get_seal_service; print('✅ Service available')"
```

## File Structure

```
backend/
├── main.py                              # FastAPI app entry point
├── requirements.txt                     # Python dependencies
├── setup_seals.py                       # Council seal registration script
├── services/
│   └── digital_seal_service.py         # Cryptographic sealing service
└── routes/
    ├── annotations_export.py            # Export API with seal integration
    └── seal_verification.py             # Seal verification API
```

## Council Members (Sample)

| ID | Name | Role | Algorithm |
|----|------|------|-----------|
| council_001 | Elena Rodriguez | Senior Council | ECC-P256 |
| council_002 | Marcus Chen | Council Observer | RSA-2048 |
| council_003 | Aisha Patel | Technical Council | ECC-P256 |
| council_004 | Dmitri Volkov | Commerce Council | RSA-2048 |
| council_005 | Sofia Ramirez | Marketing Council | ECC-P256 |

## Example: Multi-Signature Export

1. Generate export with 3 council signatures:
```bash
curl -o export.md "http://localhost:8000/api/annotations/export?format=markdown&cycle=seasonal&include_council=true&council_members=council_001,council_002,council_003"
```

2. Extract seal package from export (embedded in footer)

3. Verify signatures:
```bash
curl -X POST http://localhost:8000/api/seal/verify \
  -H "Content-Type: application/json" \
  -d @verify_request.json
```

Where `verify_request.json`:
```json
{
  "seal_package": {
    "content_hash": "a3f5d8e7...",
    "signatures": [...]
  },
  "content": "# Ceremonial Annotation Scroll\n...",
  "content_encoding": "utf-8"
}
```

## Next Steps

1. Add seal verification API route to `main.py`:
```python
from routes.seal_verification import router as seal_router
app.include_router(seal_router)
```

2. Update frontend `AnnotationExport` component to support multi-signature selection

3. Deploy to production with Azure Key Vault integration

4. Add blockchain anchoring for ledger root hash (optional)

---

**👑 Codex Dominion Backend API**

*Cryptographic sealing infrastructure for ceremonial exports*

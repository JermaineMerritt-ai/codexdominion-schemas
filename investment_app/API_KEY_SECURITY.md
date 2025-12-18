# API Key Security Guide 🔐

## ⚠️ CRITICAL: Never Commit API Keys to GitHub!

### Why This Matters
- API keys in public repos are scraped by bots within minutes
- Your account will be charged for unauthorized usage
- OpenAI/Anthropic will suspend accounts for key exposure
- Security breaches can cost thousands of dollars

### ✅ Safe Storage Methods

#### 1. Environment Variables (Recommended)

**Windows PowerShell:**
```powershell
$env:OPENAI_API_KEY = "sk-proj-YOUR-KEY-HERE"
python app.py
```

**Linux/Mac:**
```bash
export OPENAI_API_KEY="sk-proj-YOUR-KEY-HERE"
python app.py
```

**Permanent (add to system environment):**
- Windows: System Properties → Environment Variables
- Linux/Mac: Add to `~/.bashrc` or `~/.zshrc`

#### 2. .env File (Local Development)

Create `investment_app/.env`:
```env
OPENAI_API_KEY=sk-proj-YOUR-KEY-HERE
AI_PROVIDER=openai
AI_MODEL=gpt-4o-mini
```

**VERIFY .gitignore includes .env:**
```
.env
.env.local
.env.*.local
```

#### 3. GitHub Secrets (CI/CD)

For GitHub Actions workflows:

1. Repository → **Settings** → **Secrets and variables** → **Actions**
2. **New repository secret**
3. Name: `OPENAI_API_KEY`
4. Value: Your actual key
5. Use in workflows:

```yaml
name: Test
on: [push]
jobs:
  test:
    runs-on: ubuntu-latest
    steps:
      - uses: actions/checkout@v3
      - name: Run tests
        env:
          OPENAI_API_KEY: ${{ secrets.OPENAI_API_KEY }}
        run: pytest
```

#### 4. Cloud Platform Secrets

**Azure:**
```bash
az webapp config appsettings set \
  --name your-app \
  --resource-group your-rg \
  --settings OPENAI_API_KEY=sk-proj-...
```

**Heroku:**
```bash
heroku config:set OPENAI_API_KEY=sk-proj-...
```

**AWS:**
- Use AWS Secrets Manager or Parameter Store
- Reference in Lambda/ECS environment variables

### ❌ NEVER Do This

```python
# ❌ DON'T hardcode in source files
OPENAI_API_KEY = "sk-proj-abc123..."

# ❌ DON'T commit .env files
git add .env  # DANGER!

# ❌ DON'T put in config.py with actual values
API_KEY = "sk-proj-real-key"  # DANGER!

# ❌ DON'T put in README or documentation
"Use this key: sk-proj-abc123..."  # DANGER!
```

### ✅ Safe Patterns

```python
# ✅ Load from environment
import os
API_KEY = os.environ.get('OPENAI_API_KEY')

# ✅ Use python-dotenv for .env files
from dotenv import load_dotenv
load_dotenv()
API_KEY = os.getenv('OPENAI_API_KEY')

# ✅ Validate without exposing
if not API_KEY:
    raise ValueError("OPENAI_API_KEY not set")
print(f"API key configured: {API_KEY[:7]}...{API_KEY[-4:]}")
# Output: "API key configured: sk-proj...X7zQ"
```

### 🔍 Check If Keys Are Exposed

**Before committing:**
```bash
# Check what's being committed
git status
git diff

# Search for potential keys in staged files
git diff --cached | grep -i "sk-proj"
git diff --cached | grep -i "sk-ant"
```

**If you accidentally committed a key:**

1. **Rotate the key immediately** (delete old, create new)
   - OpenAI: https://platform.openai.com/api-keys
   - Anthropic: https://console.anthropic.com/settings/keys

2. **Remove from git history:**
```bash
# Use BFG Repo-Cleaner or git filter-branch
git filter-branch --force --index-filter \
  "git rm --cached --ignore-unmatch investment_app/.env" \
  --prune-empty --tag-name-filter cat -- --all

# Force push (be careful!)
git push --force --all
```

3. **Report to platform** (OpenAI/Anthropic can monitor for abuse)

### 📦 Files Already Protected in .gitignore

```
.env
.env.local
.env.*.local
.env.production
.env.development
```

These are automatically excluded from git commits.

### 🧪 Test Your Setup

```python
# investment_app/test_security.py
import os
from ai_services import get_ai_status

# Should return configuration status WITHOUT exposing keys
status = get_ai_status()
print(status)
# {'configured': True, 'provider': 'openai', 'model': 'gpt-4o-mini',
#  'openai_key_set': True, 'anthropic_key_set': False}

# Should work without hardcoded keys
assert os.getenv('OPENAI_API_KEY'), "API key must be in environment"
```

### 🚨 Emergency: Key Exposed

1. **Revoke immediately**: Delete key in OpenAI/Anthropic dashboard
2. **Create new key**: Generate replacement
3. **Update everywhere**: Environment variables, cloud configs, local .env
4. **Monitor usage**: Check for unauthorized API calls
5. **Report if needed**: Contact support if charges incurred

### 📚 Additional Resources

- [OpenAI API Key Safety](https://platform.openai.com/docs/api-reference/authentication)
- [GitHub Secrets Documentation](https://docs.github.com/en/actions/security-guides/encrypted-secrets)
- [OWASP Secrets Management](https://cheatsheetseries.owasp.org/cheatsheets/Secrets_Management_Cheat_Sheet.html)

---

**Remember**: Treat API keys like passwords. If it's in the code, it's in GitHub. If it's in GitHub, it's public.

# AI Development Studio - Running Instructions

## Issue: PyArrow Dependency
The Streamlit application cannot run currently because `pyarrow` requires C++ build tools (Visual Studio Build Tools) to compile on Windows.

## Solutions:

### Option 1: Install Visual Studio Build Tools (Recommended)
1. Download Visual Studio Build Tools: https://visualstudio.microsoft.com/downloads/
2. Install with "Desktop development with C++" workload
3. Then run:
   ```powershell
   & C:/Users/JMerr/OneDrive/Documents/.vscode/codex-dominion/.venv/Scripts/Activate.ps1
   pip install streamlit
   streamlit run ai_development_studio_lite.py --server.port 8502
   ```

### Option 2: Use Conda (Alternative)
Conda provides pre-compiled binaries:
```powershell
conda create -n streamlit-env python=3.11
conda activate streamlit-env
conda install -c conda-forge streamlit pyarrow
streamlit run ai_development_studio_lite.py --server.port 8502
```

### Option 3: Use Docker (Easiest)
Create a `Dockerfile`:
```dockerfile
FROM python:3.11-slim

WORKDIR /app
COPY ai_development_studio_lite.py .
COPY requirements.txt .

RUN pip install --no-cache-dir streamlit pandas numpy pillow pydeck altair

EXPOSE 8502

CMD ["streamlit", "run", "ai_development_studio_lite.py", "--server.port=8502"]
```

Then run:
```powershell
docker build -t ai-dev-studio .
docker run -p 8502:8502 ai-dev-studio
```

### Option 4: Use Online Streamlit Cloud
1. Push code to GitHub
2. Go to https://streamlit.io/cloud
3. Connect your repository
4. Deploy for free

## Application Features
Once running, the AI Development Studio provides:
- 🚀 Quick Project Builder
- 🧠 AI Development Assistant (Chat Interface)
- 📦 Project Templates
- 🚢 Deployment Configuration

The chat interface you're looking for is in the "🧠 AI Development Assistant" tab.

## Current Python Environment Status
- Python 3.14 installed ✅
- Virtual environment active ✅
- Streamlit NOT installed (requires pyarrow compilation) ❌
- Core dependencies (numpy, pandas, pillow) installed ✅

## Quick Alternative: View Code
To see what the chat interface does without running it:
```powershell
code ai_development_studio_lite.py
```

Look for the `render_ai_assistant()` function around line 137.

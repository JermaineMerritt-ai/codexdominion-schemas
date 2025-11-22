from fastapi import FastAPI
from codex_signals.api import app as signals_app

app = FastAPI()
app.mount("/signals", signals_app)
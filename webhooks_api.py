"""
Codex Dominion - Webhooks API
Webhook endpoints for automated trading picks delivery and integration
"""

from fastapi import FastAPI, HTTPException, Header, BackgroundTasks
from fastapi.middleware.cors import CORSMiddleware
from typing import Optional, List, Dict, Any
from datetime import datetime
import json
import hashlib
import hmac

app = FastAPI(
    title="Codex Dominion Webhooks API",
    description="Automated webhook endpoints for trading picks and portfolio notifications",
    version="1.0.0"
)

# CORS middleware
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Configuration
WEBHOOK_SECRET = "codex-sovereign-flame-2025"  # Change this in production
TRADING_PICKS_FILE = "trading_picks.json"
NEWSLETTER_FILE = "newsletter_subscribers.json"

def verify_webhook_signature(payload: str, signature: str) -> bool:
    """Verify webhook signature for security"""
    expected = hmac.new(
        WEBHOOK_SECRET.encode(),
        payload.encode(),
        hashlib.sha256
    ).hexdigest()
    return hmac.compare_digest(signature, expected)

def load_json(filepath: str) -> Dict[str, Any]:
    """Load JSON file"""
    try:
        with open(filepath, 'r') as f:
            return json.load(f)
    except FileNotFoundError:
        return {}

def save_json(filepath: str, data: Dict[str, Any]) -> None:
    """Save JSON file"""
    with open(filepath, 'w') as f:
        json.dump(data, f, indent=2)

def get_subscribers_for_segment(segment: str) -> List[str]:
    """Get email list for a segment"""
    data = load_json(NEWSLETTER_FILE)
    subscribers = data.get("subscribers", [])

    emails = []
    for sub in subscribers:
        if sub.get("status") == "active" and segment in sub.get("segments", []):
            emails.append(sub["email"])

    return emails

def add_trading_pick(pick_data: Dict[str, Any]) -> Dict[str, Any]:
    """Add new trading pick to ledger"""
    data = load_json(TRADING_PICKS_FILE)

    if "picks" not in data:
        data["picks"] = []

    # Generate ID
    pick_id = len(data["picks"]) + 1

    # Create pick record
    pick = {
        "id": pick_id,
        "date": datetime.utcnow().isoformat() + "Z",
        "ticker": pick_data.get("ticker", "").upper(),
        "reason": pick_data.get("reason", ""),
        "pick_type": pick_data.get("pick_type", "day"),
        "entry_price": pick_data.get("entry_price"),
        "target_price": pick_data.get("target_price"),
        "stop_loss": pick_data.get("stop_loss"),
        "confidence": pick_data.get("confidence", "medium"),
        "status": "active",
        "result": None,
        "created_at": datetime.utcnow().isoformat() + "Z",
        "updated_at": datetime.utcnow().isoformat() + "Z"
    }

    data["picks"].append(pick)

    # Update metadata
    data["meta"] = data.get("meta", {})
    data["meta"]["last_updated"] = datetime.utcnow().isoformat() + "Z"
    data["meta"]["total_picks"] = len(data["picks"])

    save_json(TRADING_PICKS_FILE, data)

    return pick

async def send_pick_notification(pick: Dict[str, Any], emails: List[str]):
    """Simulate sending email notification (placeholder for actual email service)"""
    # In production, integrate with SendGrid, AWS SES, or other email service
    print(f"📧 Sending pick notification to {len(emails)} subscribers")
    print(f"🎯 Pick: {pick['ticker']} - {pick['reason']}")
    print(f"💰 Entry: ${pick['entry_price']:.2f} | Target: ${pick['target_price']:.2f}")
    print(f"🛡️ Stop Loss: ${pick['stop_loss']:.2f} | Confidence: {pick['confidence']}")
    print(f"📬 Recipients: {', '.join(emails)}")

@app.get("/")
async def root():
    """API root"""
    return {
        "name": "Codex Dominion Webhooks API",
        "status": "operational",
        "endpoints": [
            "POST /webhooks/daily-picks - Receive and distribute daily trading picks",
            "POST /webhooks/pick-update - Update pick status (hit target, stopped out)",
            "GET /webhooks/health - Health check"
        ]
    }

@app.get("/webhooks/health")
async def health_check():
    """Health check endpoint"""
    return {
        "status": "healthy",
        "timestamp": datetime.utcnow().isoformat() + "Z",
        "service": "webhooks-api"
    }

@app.post("/webhooks/daily-picks")
async def receive_daily_picks(
    picks: List[Dict[str, Any]],
    background_tasks: BackgroundTasks,
    x_webhook_signature: Optional[str] = Header(None)
):
    """
    Receive daily trading picks and distribute to subscribers

    Expected payload:
    [
        {
            "ticker": "AAPL",
            "reason": "Bullish breakout above resistance",
            "pick_type": "day",
            "entry_price": 185.50,
            "target_price": 192.00,
            "stop_loss": 182.00,
            "confidence": "high"
        }
    ]
    """

    # Verify signature (optional, for production)
    # if x_webhook_signature:
    #     payload_str = json.dumps(picks)
    #     if not verify_webhook_signature(payload_str, x_webhook_signature):
    #         raise HTTPException(status_code=401, detail="Invalid webhook signature")

    if not picks or len(picks) == 0:
        raise HTTPException(status_code=400, detail="No picks provided")

    # Validate each pick
    required_fields = ["ticker", "entry_price", "target_price", "stop_loss"]
    for pick in picks:
        for field in required_fields:
            if field not in pick:
                raise HTTPException(
                    status_code=400,
                    detail=f"Missing required field: {field}"
                )

    # Add picks to ledger
    added_picks = []
    for pick_data in picks:
        try:
            pick = add_trading_pick(pick_data)
            added_picks.append(pick)
        except Exception as e:
            raise HTTPException(
                status_code=500,
                detail=f"Failed to add pick for {pick_data.get('ticker')}: {str(e)}"
            )

    # Get subscribers for daily picks
    subscribers = get_subscribers_for_segment("daily_picks")

    # Send notifications in background
    for pick in added_picks:
        background_tasks.add_task(send_pick_notification, pick, subscribers)

    return {
        "status": "success",
        "message": f"Received and processed {len(added_picks)} picks",
        "picks_added": added_picks,
        "notifications_queued": len(subscribers),
        "timestamp": datetime.utcnow().isoformat() + "Z"
    }

@app.post("/webhooks/pick-update")
async def update_pick_status(
    ticker: str,
    status: str,
    result: Optional[Dict[str, Any]] = None,
    x_webhook_signature: Optional[str] = Header(None)
):
    """
    Update pick status (hit target, stopped out, expired)

    Parameters:
    - ticker: Stock ticker
    - status: new status (hit_target, stopped_out, expired)
    - result: optional result details (exit_price, gain_loss_pct)
    """

    valid_statuses = ["active", "hit_target", "stopped_out", "expired"]
    if status not in valid_statuses:
        raise HTTPException(
            status_code=400,
            detail=f"Invalid status. Must be one of: {', '.join(valid_statuses)}"
        )

    # Load picks
    data = load_json(TRADING_PICKS_FILE)
    picks = data.get("picks", [])

    # Find and update most recent active pick for ticker
    updated = False
    for pick in reversed(picks):
        if pick["ticker"] == ticker.upper() and pick["status"] == "active":
            pick["status"] = status
            pick["updated_at"] = datetime.utcnow().isoformat() + "Z"
            if result:
                pick["result"] = result
            updated = True
            break

    if not updated:
        raise HTTPException(
            status_code=404,
            detail=f"No active pick found for {ticker}"
        )

    # Update metadata
    data["meta"]["last_updated"] = datetime.utcnow().isoformat() + "Z"
    save_json(TRADING_PICKS_FILE, data)

    return {
        "status": "success",
        "message": f"Updated {ticker} to {status}",
        "timestamp": datetime.utcnow().isoformat() + "Z"
    }

@app.get("/webhooks/subscribers/{segment}")
async def get_segment_subscribers(segment: str):
    """Get subscriber count for a segment"""

    valid_segments = ["daily_picks", "weekly_portfolio", "market_insights", "earnings_alerts"]
    if segment not in valid_segments:
        raise HTTPException(
            status_code=400,
            detail=f"Invalid segment. Must be one of: {', '.join(valid_segments)}"
        )

    subscribers = get_subscribers_for_segment(segment)

    return {
        "segment": segment,
        "subscriber_count": len(subscribers),
        "subscribers": subscribers,
        "timestamp": datetime.utcnow().isoformat() + "Z"
    }

if __name__ == "__main__":
    import uvicorn
    print("🔥 Starting Codex Dominion Webhooks API 🔥")
    print("📡 Webhook endpoints ready for trading picks automation")
    uvicorn.run(app, host="0.0.0.0", port=8097)

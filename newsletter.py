"""
Newsletter & Subscription Management System
"""
import json
from datetime import datetime

SUBSCRIBERS_LEDGER = "newsletter_subscribers.json"

def load_subscribers():
    """Load newsletter subscribers ledger"""
    try:
        with open(SUBSCRIBERS_LEDGER, "r") as f:
            return json.load(f)
    except FileNotFoundError:
        return {
            "meta": {
                "version": "1.0.0",
                "last_updated": datetime.utcnow().isoformat() + "Z",
                "custodian_authority": "Jermaine Merritt",
                "ledger_type": "NEWSLETTER_SUBSCRIBERS_LEDGER"
            },
            "subscribers": [],
            "segments": {
                "daily_picks": {
                    "name": "Daily Trading Picks",
                    "description": "Daily stock picks and trading opportunities",
                    "frequency": "daily"
                },
                "weekly_portfolio": {
                    "name": "Weekly Portfolio Review",
                    "description": "Weekly portfolio analysis and recommendations",
                    "frequency": "weekly"
                },
                "market_insights": {
                    "name": "Market Insights",
                    "description": "Market analysis and sector insights",
                    "frequency": "weekly"
                },
                "earnings_alerts": {
                    "name": "Earnings Alerts",
                    "description": "Upcoming earnings and key events",
                    "frequency": "as_needed"
                }
            }
        }

def save_subscribers(data):
    """Save newsletter subscribers ledger"""
    data["meta"]["last_updated"] = datetime.utcnow().isoformat() + "Z"
    with open(SUBSCRIBERS_LEDGER, "w") as f:
        json.dump(data, f, indent=2)

def subscribe(email, risk_profile, segments, preferences=None):
    """Subscribe user to newsletter segments"""
    data = load_subscribers()

    # Check if already subscribed
    existing_idx = None
    for i, sub in enumerate(data["subscribers"]):
        if sub["email"] == email:
            existing_idx = i
            break

    subscriber = {
        "id": len(data["subscribers"]) + 1 if existing_idx is None else data["subscribers"][existing_idx]["id"],
        "email": email,
        "risk_profile": risk_profile,
        "segments": segments,
        "preferences": preferences or {
            "frequency": "daily",
            "format": "html",
            "timezone": "UTC"
        },
        "status": "active",
        "subscribed_at": datetime.utcnow().isoformat() + "Z" if existing_idx is None else data["subscribers"][existing_idx]["subscribed_at"],
        "updated_at": datetime.utcnow().isoformat() + "Z"
    }

    if existing_idx is not None:
        data["subscribers"][existing_idx] = subscriber
        print(f"📝 Updated subscription for {email}")
    else:
        data["subscribers"].append(subscriber)
        print(f"✅ Subscribed {email}")

    save_subscribers(data)
    return subscriber

def unsubscribe(email):
    """Unsubscribe user from all newsletters"""
    data = load_subscribers()

    for i, sub in enumerate(data["subscribers"]):
        if sub["email"] == email:
            sub["status"] = "unsubscribed"
            sub["unsubscribed_at"] = datetime.utcnow().isoformat() + "Z"
            data["subscribers"][i] = sub
            save_subscribers(data)
            print(f"✅ Unsubscribed {email}")
            return sub

    print(f"⚠️  {email} not found")
    return None

def get_subscribers_by_segment(segment_name):
    """Get all active subscribers for a specific segment"""
    data = load_subscribers()

    subscribers = [
        sub for sub in data["subscribers"]
        if sub["status"] == "active" and segment_name in sub["segments"]
    ]

    return subscribers

def get_subscribers_by_risk_profile(risk_profile):
    """Get all active subscribers with specific risk profile"""
    data = load_subscribers()

    subscribers = [
        sub for sub in data["subscribers"]
        if sub["status"] == "active" and sub["risk_profile"] == risk_profile
    ]

    return subscribers

def display_subscriber(email):
    """Display subscriber details"""
    data = load_subscribers()

    subscriber = None
    for sub in data["subscribers"]:
        if sub["email"] == email:
            subscriber = sub
            break

    if not subscriber:
        print(f"⚠️  Subscriber {email} not found")
        return None

    print("\n" + "="*60)
    print(f"📧 SUBSCRIBER: {email} 👑")
    print("="*60)
    print(f"\nStatus: {subscriber['status'].upper()}")
    print(f"Risk Profile: {subscriber['risk_profile'].upper()}")
    print(f"\nSubscribed Segments:")
    for segment in subscriber["segments"]:
        segment_info = data["segments"].get(segment, {})
        print(f"  ✅ {segment_info.get('name', segment)}")
        print(f"     {segment_info.get('description', 'N/A')}")

    print(f"\nPreferences:")
    prefs = subscriber.get("preferences", {})
    print(f"  Frequency: {prefs.get('frequency', 'N/A')}")
    print(f"  Format: {prefs.get('format', 'N/A')}")
    print(f"  Timezone: {prefs.get('timezone', 'N/A')}")

    print(f"\nSubscribed: {subscriber['subscribed_at']}")
    print(f"Updated: {subscriber['updated_at']}")

    print("\n" + "="*60 + "\n")
    return subscriber

def display_all_subscribers():
    """Display all subscribers"""
    data = load_subscribers()

    active = [s for s in data["subscribers"] if s["status"] == "active"]

    if not active:
        print("⚠️  No active subscribers")
        return

    print("\n" + "="*60)
    print("📧 ALL SUBSCRIBERS 👑")
    print("="*60)
    print(f"\nTotal Active: {len(active)}")

    # Group by risk profile
    risk_groups = {}
    for sub in active:
        risk = sub["risk_profile"]
        if risk not in risk_groups:
            risk_groups[risk] = []
        risk_groups[risk].append(sub)

    for risk, subs in risk_groups.items():
        print(f"\n{risk.upper()} ({len(subs)} subscribers):")
        for sub in subs:
            segments_str = ", ".join(sub["segments"])
            print(f"  • {sub['email']} - {segments_str}")

    print("\n" + "="*60 + "\n")

def display_segment_stats():
    """Display subscriber statistics by segment"""
    data = load_subscribers()

    active = [s for s in data["subscribers"] if s["status"] == "active"]

    print("\n" + "="*60)
    print("📊 NEWSLETTER SEGMENTS STATISTICS 👑")
    print("="*60)

    for segment_key, segment_info in data["segments"].items():
        count = len([s for s in active if segment_key in s["segments"]])
        print(f"\n{segment_info['name']} ({segment_info['frequency']})")
        print(f"  Subscribers: {count}")
        print(f"  {segment_info['description']}")

    print(f"\n\nTotal Active Subscribers: {len(active)}")
    print("\n" + "="*60 + "\n")

def generate_email_list(segment_name):
    """Generate email list for a segment"""
    subscribers = get_subscribers_by_segment(segment_name)

    if not subscribers:
        print(f"⚠️  No subscribers for segment: {segment_name}")
        return []

    emails = [sub["email"] for sub in subscribers]

    print(f"\n📧 Email List for '{segment_name}' ({len(emails)} recipients)")
    print("="*60)
    for email in emails:
        print(f"  {email}")
    print("\n" + "="*60 + "\n")

    return emails

if __name__ == "__main__":
    import sys

    if len(sys.argv) > 1:
        command = sys.argv[1].lower()

        if command == "subscribe":
            # python newsletter.py subscribe user@example.com moderate daily_picks,weekly_portfolio
            email = sys.argv[2]
            risk_profile = sys.argv[3]
            segments = sys.argv[4].split(",")

            subscribe(email, risk_profile, segments)
            display_subscriber(email)

        elif command == "unsubscribe":
            # python newsletter.py unsubscribe user@example.com
            email = sys.argv[2]
            unsubscribe(email)

        elif command == "view":
            # python newsletter.py view user@example.com
            email = sys.argv[2]
            display_subscriber(email)

        elif command == "list":
            # python newsletter.py list
            display_all_subscribers()

        elif command == "stats":
            # python newsletter.py stats
            display_segment_stats()

        elif command == "emails":
            # python newsletter.py emails daily_picks
            segment = sys.argv[2]
            generate_email_list(segment)

        else:
            print("Usage:")
            print("  python newsletter.py subscribe <email> <risk_profile> <segments>")
            print("  python newsletter.py unsubscribe <email>")
            print("  python newsletter.py view <email>")
            print("  python newsletter.py list")
            print("  python newsletter.py stats")
            print("  python newsletter.py emails <segment>")
    else:
        # Default: Subscribe example user
        print("\n🔥 Newsletter Subscription System 👑\n")

        email = "user@example.com"
        risk_profile = "moderate"
        segments = ["daily_picks", "weekly_portfolio"]

        subscribe(email, risk_profile, segments)

        print("\n" + "="*60)
        display_subscriber(email)
        display_segment_stats()

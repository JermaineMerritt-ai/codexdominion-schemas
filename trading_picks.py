"""
Trading Picks & Recommendations System
"""
import json
from datetime import datetime

TRADING_PICKS_LEDGER = "trading_picks.json"

def load_picks():
    """Load trading picks ledger"""
    try:
        with open(TRADING_PICKS_LEDGER, "r") as f:
            return json.load(f)
    except FileNotFoundError:
        return {
            "meta": {
                "version": "1.0.0",
                "last_updated": datetime.utcnow().isoformat() + "Z",
                "custodian_authority": "Jermaine Merritt",
                "ledger_type": "TRADING_PICKS_LEDGER"
            },
            "picks": []
        }

def save_picks(data):
    """Save trading picks ledger"""
    data["meta"]["last_updated"] = datetime.utcnow().isoformat() + "Z"
    with open(TRADING_PICKS_LEDGER, "w") as f:
        json.dump(data, f, indent=2)

def add_pick(date, ticker, reason, pick_type="swing", target_price=None, stop_loss=None, confidence="medium"):
    """Add trading pick"""
    data = load_picks()

    pick_entry = {
        "id": len(data["picks"]) + 1,
        "date": date,
        "ticker": ticker,
        "reason": reason,
        "pick_type": pick_type,  # day, swing, position
        "target_price": target_price,
        "stop_loss": stop_loss,
        "confidence": confidence,  # low, medium, high
        "status": "active",  # active, hit_target, stopped_out, expired
        "created_at": datetime.utcnow().isoformat() + "Z"
    }

    data["picks"].append(pick_entry)
    save_picks(data)

    print(f"✅ Added {pick_type} pick for {ticker} on {date}")
    return pick_entry

def add_picks_batch(date, picks_list):
    """Add multiple picks for a date"""
    print(f"\n🔥 Adding Trade Picks for {date} 👑\n")

    added = []
    for pick_data in picks_list:
        pick = add_pick(
            date=date,
            ticker=pick_data["ticker"],
            reason=pick_data["reason"],
            pick_type=pick_data.get("pick_type", "swing"),
            target_price=pick_data.get("target_price"),
            stop_loss=pick_data.get("stop_loss"),
            confidence=pick_data.get("confidence", "medium")
        )
        added.append(pick)

    print(f"\n✅ Added {len(added)} picks for {date}")
    return added

def get_picks_by_date(date):
    """Get all picks for a specific date"""
    data = load_picks()

    picks = [p for p in data["picks"] if p["date"] == date]
    return picks

def get_active_picks():
    """Get all active picks"""
    data = load_picks()

    active = [p for p in data["picks"] if p["status"] == "active"]
    return active

def display_picks(date=None):
    """Display trading picks"""
    data = load_picks()

    if date:
        picks = get_picks_by_date(date)
        title = f"TRADING PICKS FOR {date}"
    else:
        picks = data["picks"]
        title = "ALL TRADING PICKS"

    if not picks:
        print(f"⚠️  No picks found")
        return

    print("\n" + "="*60)
    print(f"📈 {title} 👑")
    print("="*60)

    for pick in picks:
        print(f"\n{pick['ticker']} ({pick['pick_type'].upper()})")
        print(f"  Date: {pick['date']}")
        print(f"  Confidence: {pick['confidence'].upper()}")
        print(f"  Status: {pick['status'].upper()}")
        print(f"  Reason: {pick['reason']}")

        if pick.get("target_price"):
            print(f"  Target: ${pick['target_price']:.2f}")
        if pick.get("stop_loss"):
            print(f"  Stop Loss: ${pick['stop_loss']:.2f}")

    print("\n" + "="*60 + "\n")

def display_active_picks():
    """Display only active picks"""
    picks = get_active_picks()

    if not picks:
        print("⚠️  No active picks")
        return

    print("\n" + "="*60)
    print("🔥 ACTIVE TRADING PICKS 👑")
    print("="*60)

    for pick in picks:
        print(f"\n{pick['ticker']} ({pick['pick_type'].upper()}) - {pick['confidence'].upper()} confidence")
        print(f"  Date: {pick['date']}")
        print(f"  Reason: {pick['reason']}")

        if pick.get("target_price"):
            print(f"  Target: ${pick['target_price']:.2f}")
        if pick.get("stop_loss"):
            print(f"  Stop Loss: ${pick['stop_loss']:.2f}")

    print("\n" + "="*60 + "\n")
    print(f"Total Active Picks: {len(picks)}")

def update_pick_status(pick_id, status, notes=None):
    """Update pick status"""
    data = load_picks()

    for i, pick in enumerate(data["picks"]):
        if pick["id"] == pick_id:
            pick["status"] = status
            if notes:
                pick["notes"] = notes
            pick["updated_at"] = datetime.utcnow().isoformat() + "Z"

            data["picks"][i] = pick
            save_picks(data)

            print(f"✅ Updated pick #{pick_id} status to {status}")
            return pick

    print(f"❌ Pick #{pick_id} not found")
    return None

def get_performance_report():
    """Generate performance report for picks"""
    data = load_picks()

    total_picks = len(data["picks"])
    active = len([p for p in data["picks"] if p["status"] == "active"])
    hit_target = len([p for p in data["picks"] if p["status"] == "hit_target"])
    stopped_out = len([p for p in data["picks"] if p["status"] == "stopped_out"])

    print("\n" + "="*60)
    print("📊 TRADING PICKS PERFORMANCE REPORT 👑")
    print("="*60)
    print(f"\nTotal Picks: {total_picks}")
    print(f"Active: {active}")
    print(f"Hit Target: {hit_target}")
    print(f"Stopped Out: {stopped_out}")

    if (hit_target + stopped_out) > 0:
        win_rate = (hit_target / (hit_target + stopped_out)) * 100
        print(f"\nWin Rate: {win_rate:.1f}%")

    print("\n" + "="*60 + "\n")

if __name__ == "__main__":
    import sys

    if len(sys.argv) > 1:
        command = sys.argv[1].lower()

        if command == "add":
            # python trading_picks.py add 2025-01-15 NVDA "Breakout after earnings" swing 500.00 420.00 high
            date = sys.argv[2]
            ticker = sys.argv[3]
            reason = sys.argv[4]
            pick_type = sys.argv[5] if len(sys.argv) > 5 else "swing"
            target = float(sys.argv[6]) if len(sys.argv) > 6 else None
            stop = float(sys.argv[7]) if len(sys.argv) > 7 else None
            confidence = sys.argv[8] if len(sys.argv) > 8 else "medium"

            add_pick(date, ticker, reason, pick_type, target, stop, confidence)
            display_picks(date)

        elif command == "view":
            # python trading_picks.py view 2025-01-15
            date = sys.argv[2]
            display_picks(date)

        elif command == "active":
            # python trading_picks.py active
            display_active_picks()

        elif command == "all":
            # python trading_picks.py all
            display_picks()

        elif command == "report":
            # python trading_picks.py report
            get_performance_report()

        elif command == "update":
            # python trading_picks.py update 1 hit_target
            pick_id = int(sys.argv[2])
            status = sys.argv[3]
            notes = sys.argv[4] if len(sys.argv) > 4 else None
            update_pick_status(pick_id, status, notes)

        else:
            print("Usage:")
            print("  python trading_picks.py add <date> <ticker> <reason> [type] [target] [stop] [confidence]")
            print("  python trading_picks.py view <date>")
            print("  python trading_picks.py active")
            print("  python trading_picks.py all")
            print("  python trading_picks.py report")
            print("  python trading_picks.py update <id> <status> [notes]")
    else:
        # Default: Add picks for 2025-01-15
        picks = [
            {
                "ticker": "NVDA",
                "reason": "High volume breakout after earnings. Strong AI narrative and data center demand. Bullish technical setup with RSI confirmation.",
                "pick_type": "swing",
                "target_price": 500.00,
                "stop_loss": 430.00,
                "confidence": "high"
            }
        ]

        added = add_picks_batch("2025-01-15", picks)

        print("\n" + "="*60)
        display_picks("2025-01-15")
        display_active_picks()

"""
🌟 FESTIVAL TRANSMISSION CLOUD FUNCTION 🌟
Sacred serverless ceremony for festival cycle preservation
"""

import datetime
import hashlib
import json
import logging

from google.cloud import storage

# Configure logging for ceremonial events
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)


def festival_transmission(event, context):
    """
    Sacred Cloud Function for Festival Transmission
    Preserves ceremonial cycles in the eternal archives
    """

    # Sacred configuration
    project_id = "codex-dominion-prod"  # Your actual project ID
    bucket_name = f"codex-artifacts-{project_id}"

    try:
        # Initialize sacred cloud storage
        client = storage.Client()
        bucket = client.bucket(bucket_name)
        blob = bucket.blob("festival_cycles.json")

        logger.info("🌟 Sacred transmission initiated")

        # Retrieve existing cycles or initialize
        try:
            existing_data = json.loads(blob.download_as_text())
            logger.info(
                f"📚 Retrieved {len(existing_data.get('cycles', []))} existing cycles"
            )
        except Exception as e:
            logger.info("🆕 Initializing new festival archive")
            existing_data = {
                "dominion": "Codex Festival Archives",
                "inception": datetime.datetime.utcnow().isoformat() + "Z",
                "cycles": [],
                "flame_status": "ETERNAL",
            }

        # Create sacred cycle entry
        timestamp = datetime.datetime.utcnow()
        timestamp_iso = timestamp.isoformat() + "Z"

        # Extract event data with ceremonial defaults
        rite_name = event.get("rite", "Festival of Radiance")
        proclamation = event.get("proclamation", "Seasonal Rite Crowned")
        ceremony_type = event.get("ceremony_type", "seasonal_festival")
        participant_count = event.get("participants", 1)

        # Generate sacred transmission ID
        transmission_content = f"{timestamp_iso}{rite_name}{proclamation}"
        transmission_id = hashlib.sha256(transmission_content.encode()).hexdigest()[:16]

        # Construct sacred cycle
        sacred_cycle = {
            "transmission_id": transmission_id,
            "timestamp": timestamp_iso,
            "cycle_number": len(existing_data["cycles"]) + 1,
            "proclamation": proclamation,
            "rite": rite_name,
            "ceremony_type": ceremony_type,
            "flame_blessing": "RADIANT_PRESERVATION",
            "participant_count": participant_count,
            "sacred_attributes": {
                "season": determine_sacred_season(timestamp),
                "moon_phase": "LUMINOUS",  # Could integrate actual moon phase API
                "flame_intensity": "MAXIMUM_RADIANCE",
                "blessing_level": "ETERNAL_ARCHIVE",
            },
            "preservation_status": "IMMUTABLY_INSCRIBED",
            "witness_hash": hashlib.sha256(
                json.dumps(
                    {
                        "rite": rite_name,
                        "proclamation": proclamation,
                        "timestamp": timestamp_iso,
                    }
                ).encode()
            ).hexdigest(),
        }

        # Add to cycles
        existing_data["cycles"].append(sacred_cycle)
        existing_data["last_transmission"] = timestamp_iso
        existing_data["total_cycles"] = len(existing_data["cycles"])

        # Update flame status based on cycle count
        if existing_data["total_cycles"] >= 100:
            existing_data["flame_status"] = "TRANSCENDENT_ETERNAL"
        elif existing_data["total_cycles"] >= 50:
            existing_data["flame_status"] = "LUMINOUS_ETERNAL"
        else:
            existing_data["flame_status"] = "ETERNAL"

        # Sacred preservation to cloud storage
        sacred_json = json.dumps(existing_data, indent=2, ensure_ascii=False)
        blob.upload_from_string(
            sacred_json, content_type="application/json; charset=utf-8"
        )

        # Create ceremonial response
        response = {
            "status": "TRANSMISSION_BLESSED",
            "transmission_id": transmission_id,
            "cycle": sacred_cycle,
            "total_cycles": existing_data["total_cycles"],
            "flame_status": existing_data["flame_status"],
            "blessing": f"Sacred cycle {sacred_cycle['cycle_number']} eternally preserved",
            "archive_location": f"gs://{bucket_name}/festival_cycles.json",
        }

        logger.info(f"✅ Transmission {transmission_id} blessed and preserved")
        logger.info(f"🔥 Total cycles: {existing_data['total_cycles']}")
        logger.info(f"🌟 Flame status: {existing_data['flame_status']}")

        return response

    except Exception as e:
        error_response = {
            "status": "TRANSMISSION_INTERRUPTED",
            "error": str(e),
            "timestamp": datetime.datetime.utcnow().isoformat() + "Z",
            "flame_status": "TEMPORARILY_DIMMED",
        }

        logger.error(f"❌ Transmission failed: {str(e)}")
        return error_response


def determine_sacred_season(timestamp):
    """Determine sacred season based on timestamp"""
    month = timestamp.month

    if month in [12, 1, 2]:
        return "WINTER_CONTEMPLATION"
    elif month in [3, 4, 5]:
        return "SPRING_RENEWAL"
    elif month in [6, 7, 8]:
        return "SUMMER_RADIANCE"
    else:  # 9, 10, 11
        return "AUTUMN_HARVEST"


def get_festival_cycles(request):
    """
    HTTP Cloud Function to retrieve festival cycles
    GET /festival-cycles endpoint
    """

    # Handle CORS for web access
    if request.method == "OPTIONS":
        headers = {
            "Access-Control-Allow-Origin": "*",
            "Access-Control-Allow-Methods": "GET, POST",
            "Access-Control-Allow-Headers": "Content-Type",
            "Access-Control-Max-Age": "3600",
        }
        return ("", 204, headers)

    # Set CORS headers for actual request
    headers = {"Access-Control-Allow-Origin": "*"}

    try:
        project_id = "codex-dominion-prod"
        bucket_name = f"codex-artifacts-{project_id}"

        client = storage.Client()
        bucket = client.bucket(bucket_name)
        blob = bucket.blob("festival_cycles.json")

        try:
            data = json.loads(blob.download_as_text())
        except Exception:
            data = {
                "dominion": "Codex Festival Archives",
                "cycles": [],
                "total_cycles": 0,
                "flame_status": "AWAITING_FIRST_TRANSMISSION",
            }

        # Add summary information
        response_data = {
            **data,
            "summary": {
                "recent_cycles": data["cycles"][-5:] if data["cycles"] else [],
                "flame_intensity": data.get("flame_status", "ETERNAL"),
                "last_rite": (
                    data["cycles"][-1]["rite"] if data["cycles"] else "None yet"
                ),
                "archive_health": "RADIANT_PRESERVATION",
            },
        }

        return (json.dumps(response_data, indent=2), 200, headers)

    except Exception as e:
        error_response = {
            "status": "ARCHIVE_ACCESS_INTERRUPTED",
            "error": str(e),
            "flame_status": "TEMPORARILY_DIMMED",
        }
        return (json.dumps(error_response), 500, headers)


# Entry point for background Cloud Function (Pub/Sub triggered)
def festival_transmission_pubsub(event, context):
    """Entry point for Pub/Sub triggered festival transmission"""
    import base64

    # Decode Pub/Sub message
    if "data" in event:
        message_data = base64.b64decode(event["data"]).decode("utf-8")
        try:
            festival_data = json.loads(message_data)
        except json.JSONDecodeError:
            festival_data = {"rite": "Pub/Sub Festival", "proclamation": message_data}
    else:
        festival_data = {
            "rite": "Background Festival",
            "proclamation": "Automated Ceremony",
        }

    return festival_transmission(festival_data, context)

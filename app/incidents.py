import psycopg2, datetime, os
import json
import logging

# Set up fallback logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

# Database connection with error handling
try:
    DB = psycopg2.connect(os.getenv("DATABASE_URL")) if os.getenv("DATABASE_URL") else None
except Exception as e:
    logger.warning(f"Database connection failed: {e}")
    DB = None

def log_incident(source: str, message: str, severity: str = "warning"):
    """
    Log incident to database with fallback to file logging
    
    Args:
        source: System component (e.g., 'affiliate_api', 'amm_node', 'market_data')
        message: Incident description
        severity: 'info', 'warning', 'error', or 'critical'
    """
    incident_data = {
        "timestamp": datetime.datetime.utcnow().isoformat(),
        "source": source,
        "message": message,
        "severity": severity
    }
    
    # Try database first
    if DB:
        try:
            cur = DB.cursor()
            cur.execute("""
                INSERT INTO incidents (source, message, severity, created_at)
                VALUES (%s, %s, %s, %s)
            """, (source, message, severity, datetime.datetime.utcnow()))
            DB.commit()
            cur.close()
            logger.info(f"Incident logged to DB: {source} - {severity}")
            return True
        except Exception as e:
            logger.error(f"Failed to log incident to database: {e}")
    
    # Fallback to file logging
    try:
        with open("incidents.jsonl", "a", encoding="utf-8") as f:
            f.write(json.dumps(incident_data) + "\n")
        logger.info(f"Incident logged to file: {source} - {severity}")
        return True
    except Exception as e:
        logger.error(f"Failed to log incident to file: {e}")
        return False

def get_recent_incidents(hours: int = 24, severity: str = None):
    """
    Get recent incidents from database or file fallback
    
    Args:
        hours: Number of hours to look back
        severity: Filter by severity level (optional)
    
    Returns:
        List of incident records
    """
    cutoff_time = datetime.datetime.utcnow() - datetime.timedelta(hours=hours)
    
    # Try database first
    if DB:
        try:
            cur = DB.cursor()
            query = """
                SELECT source, message, severity, created_at 
                FROM incidents 
                WHERE created_at >= %s
            """
            params = [cutoff_time]
            
            if severity:
                query += " AND severity = %s"
                params.append(severity)
            
            query += " ORDER BY created_at DESC"
            
            cur.execute(query, params)
            results = cur.fetchall()
            cur.close()
            
            return [
                {
                    "source": row[0], 
                    "message": row[1], 
                    "severity": row[2], 
                    "created_at": row[3].isoformat()
                }
                for row in results
            ]
        except Exception as e:
            logger.error(f"Failed to query incidents from database: {e}")
    
    # Fallback to file reading
    try:
        incidents = []
        if os.path.exists("incidents.jsonl"):
            with open("incidents.jsonl", "r", encoding="utf-8") as f:
                for line in f:
                    incident = json.loads(line.strip())
                    incident_time = datetime.datetime.fromisoformat(incident["timestamp"])
                    if incident_time >= cutoff_time:
                        if not severity or incident["severity"] == severity:
                            incidents.append(incident)
        
        return sorted(incidents, key=lambda x: x["timestamp"], reverse=True)
    except Exception as e:
        logger.error(f"Failed to read incidents from file: {e}")
        return []
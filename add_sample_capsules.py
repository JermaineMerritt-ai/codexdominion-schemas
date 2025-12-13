"""
Add sample capsules to PostgreSQL database
"""
import psycopg2
from datetime import datetime

# Database connection
conn_params = {
    'host': 'codex-pg-centralus2.postgres.database.azure.com',
    'database': 'codexdb',
    'user': 'pgadmin',
    'password': 'Dominion2025!',
    'sslmode': 'require'
}

try:
    conn = psycopg2.connect(**conn_params)
    cur = conn.cursor()

    # Production capsules for Codex Dominion
    capsules = [
        ('daily-signal-001', 'Daily Sovereign Signal', 'dispatch', 'recurring',
         'gpt-4o-mini', 'heir', 'Dawn breaks. Sovereignty restored. Continue the watch.'),
        ('sovereignty-bulletin', 'Sovereignty Council Bulletin', 'decree', 'scheduled',
         'gpt-4o', 'council', 'Council convenes. Decisions sealed. Eternal flame burns.'),
        ('treasury-report', 'Treasury Audit Report', 'analysis', 'periodic',
         'gpt-4', 'custodian', 'Financial review complete. All accounts balanced.'),
        ('dawn-dispatch', 'Dawn Dispatch Capsule', 'notification', 'recurring',
         'gpt-4o-mini', 'heir', 'Morning briefing: All systems operational. Archive integrity confirmed.'),
        ('education-matrix', 'Educational Matrix Capsule', 'knowledge', 'scheduled',
         'gpt-4o', 'observer', 'Knowledge compilation: Historical data indexed and cross-referenced.'),
        ('signals-daily', 'Daily Signals Aggregation', 'analysis', 'recurring',
         'gpt-4o-mini', 'heir', 'Signal analysis complete. Patterns identified across all channels.'),
        ('council-deliberation', 'Council Deliberation Record', 'decree', 'scheduled',
         'gpt-4o', 'council', 'Council session archived. All motions recorded with full provenance.'),
        ('flame-eternal', 'Eternal Flame Keeper', 'ceremonial', 'perpetual',
         'gpt-4o', 'custodian', 'Flame burns eternal. Covenant sealed. Archives protected across all cycles.'),
        ('sovereignty-audit', 'Sovereignty Integrity Audit', 'verification', 'periodic',
         'gpt-4', 'custodian', 'Integrity verification complete. All seals validated. No anomalies detected.'),
        ('heir-proclamation', 'Heir Proclamation Archive', 'decree', 'scheduled',
         'gpt-4o', 'heir', 'Proclamation recorded: Sovereignty acknowledged. Stewardship accepted.')
    ]

    for capsule in capsules:
        try:
            cur.execute("""
                INSERT INTO capsules (slug, title, kind, mode, engine, user_role, content, created_at)
                VALUES (%s, %s, %s, %s, %s, %s, %s, NOW())
                ON CONFLICT (slug) DO NOTHING
                RETURNING slug, title
            """, capsule)

            result = cur.fetchone()
            if result:
                print(f"✓ Inserted: {result[0]} - {result[1]}")
            else:
                print(f"• Already exists: {capsule[0]}")
        except Exception as e:
            print(f"✗ Error with {capsule[0]}: {e}")

    conn.commit()

    # Verify count
    cur.execute("SELECT COUNT(*) FROM capsules")
    count = cur.fetchone()[0]
    print(f"\n✓ Total capsules in database: {count}")

    cur.close()
    conn.close()
    print("✓ Connection closed")

except Exception as e:
    print(f"✗ Database connection error: {e}")

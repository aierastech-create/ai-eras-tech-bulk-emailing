import sqlite3
import os
from datetime import datetime

class Database:
    def __init__(self, db_path="data/mailforge.db"):
        self.db_path = db_path
        os.makedirs(os.path.dirname(self.db_path), exist_ok=True)
        self.init_db()

    def get_connection(self):
        conn = sqlite3.connect(self.db_path)
        conn.row_factory = sqlite3.Row
        return conn

    def init_db(self):
        with self.get_connection() as conn:
            conn.execute("""
                CREATE TABLE IF NOT EXISTS campaigns (
                    id INTEGER PRIMARY KEY AUTOINCREMENT,
                    name TEXT,
                    subject TEXT,
                    subject_b TEXT,
                    status TEXT DEFAULT 'running',
                    scheduled_at DATETIME,
                    csv_path TEXT,
                    template_str TEXT,
                    created_at DATETIME DEFAULT CURRENT_TIMESTAMP
                )
            """)
            
            # Migration: Ensure columns exist (for older DB versions)
            cursor = conn.cursor()
            
            # Campaigns migrations
            cursor.execute("PRAGMA table_info(campaigns)")
            current_campaign_cols = [row[1] for row in cursor.fetchall()]
            
            campaign_migrations = [
                ("status", "TEXT DEFAULT 'running'"),
                ("subject_b", "TEXT"),
                ("scheduled_at", "DATETIME"),
                ("csv_path", "TEXT"),
                ("template_str", "TEXT")
            ]
            
            for col_name, col_type in campaign_migrations:
                if col_name not in current_campaign_cols:
                    try:
                        conn.execute(f"ALTER TABLE campaigns ADD COLUMN {col_name} {col_type}")
                        logger.info(f"Added column {col_name} to campaigns table")
                    except Exception as e:
                        logger.error(f"Failed to add column {col_name} to campaigns: {e}")

            # Ensure tables exist
            conn.execute("""
                CREATE TABLE IF NOT EXISTS recipients (
                    id TEXT PRIMARY KEY,
                    campaign_id INTEGER,
                    email TEXT,
                    status TEXT DEFAULT 'pending', 
                    sent_at DATETIME,
                    subject_used TEXT,
                    FOREIGN KEY(campaign_id) REFERENCES campaigns(id)
                )
            """)

            # Recipients migrations
            cursor.execute("PRAGMA table_info(recipients)")
            current_recipient_cols = [row[1] for row in cursor.fetchall()]
            
            recipient_migrations = [
                ("status", "TEXT DEFAULT 'pending'"),
                ("sent_at", "DATETIME"),
                ("subject_used", "TEXT")
            ]
            
            for col_name, col_type in recipient_migrations:
                if col_name not in current_recipient_cols:
                    try:
                        conn.execute(f"ALTER TABLE recipients ADD COLUMN {col_name} {col_type}")
                        logger.info(f"Added column {col_name} to recipients table")
                    except Exception as e:
                        logger.error(f"Failed to add column {col_name} to recipients: {e}")

            conn.execute("""
                CREATE TABLE IF NOT EXISTS events (
                    id INTEGER PRIMARY KEY AUTOINCREMENT,
                    recipient_id TEXT,
                    event_type TEXT, 
                    url TEXT,
                    ip_address TEXT,
                    user_agent TEXT,
                    timestamp DATETIME DEFAULT CURRENT_TIMESTAMP,
                    FOREIGN KEY(recipient_id) REFERENCES recipients(id)
                )
            """)
            conn.commit()

    def create_campaign(self, name, subject, subject_b=None, status='running', scheduled_at=None, csv_path=None, template_str=None):
        with self.get_connection() as conn:
            cursor = conn.cursor()
            cursor.execute(
                "INSERT INTO campaigns (name, subject, subject_b, status, scheduled_at, csv_path, template_str) VALUES (?, ?, ?, ?, ?, ?, ?)",
                (name, subject, subject_b, status, scheduled_at, csv_path, template_str)
            )
            conn.commit()
            return cursor.lastrowid

    def update_campaign_status(self, campaign_id, status):
        with self.get_connection() as conn:
            conn.execute("UPDATE campaigns SET status = ? WHERE id = ?", (status, campaign_id))
            conn.commit()

    def get_due_campaigns(self):
        with self.get_connection() as conn:
            cursor = conn.cursor()
            now = datetime.now().isoformat()
            cursor.execute(
                "SELECT * FROM campaigns WHERE status = 'scheduled' AND scheduled_at <= ?",
                (now,)
            )
            return cursor.fetchall()

    def add_recipient(self, recipient_id, campaign_id, email, subject_used=None):
        with self.get_connection() as conn:
            conn.execute(
                "INSERT INTO recipients (id, campaign_id, email, subject_used) VALUES (?, ?, ?, ?)",
                (recipient_id, campaign_id, email, subject_used)
            )
            conn.commit()

    def update_recipient_status(self, recipient_id, status, sent_at=None):
        with self.get_connection() as conn:
            if sent_at:
                conn.execute(
                    "UPDATE recipients SET status = ?, sent_at = ? WHERE id = ?",
                    (status, sent_at, recipient_id)
                )
            else:
                conn.execute(
                    "UPDATE recipients SET status = ? WHERE id = ?",
                    (status, recipient_id)
                )
            conn.commit()

    def log_event(self, recipient_id, event_type, url=None, ip=None, ua=None):
        with self.get_connection() as conn:
            conn.execute(
                "INSERT INTO events (recipient_id, event_type, url, ip_address, user_agent) VALUES (?, ?, ?, ?, ?)",
                (recipient_id, event_type, url, ip, ua)
            )
            conn.execute(
                "UPDATE recipients SET status = ? WHERE id = ? AND status != 'clicked'",
                ('clicked' if event_type == 'click' else 'opened', recipient_id)
            )
            conn.commit()

    def get_campaign_stats(self, campaign_id):
        with self.get_connection() as conn:
            cursor = conn.cursor()
            
            cursor.execute("SELECT COUNT(*) FROM recipients WHERE campaign_id = ? AND status != 'pending'", (campaign_id,))
            sent = cursor.fetchone()[0]
            
            cursor.execute("""
                SELECT COUNT(DISTINCT recipient_id) FROM events 
                WHERE event_type = 'open' AND recipient_id IN (SELECT id FROM recipients WHERE campaign_id = ?)
            """, (campaign_id,))
            opens = cursor.fetchone()[0]
            
            cursor.execute("""
                SELECT COUNT(DISTINCT recipient_id) FROM events 
                WHERE event_type = 'click' AND recipient_id IN (SELECT id FROM recipients WHERE campaign_id = ?)
            """, (campaign_id,))
            clicks = cursor.fetchone()[0]
            
            return {
                "sent": sent,
                "opens": opens,
                "clicks": clicks,
                "open_rate": round((opens / sent * 100), 2) if sent > 0 else 0,
                "click_rate": round((clicks / sent * 100), 2) if sent > 0 else 0
            }

    def get_ab_stats(self, campaign_id):
        with self.get_connection() as conn:
            cursor = conn.cursor()
            # This query joins recipients with unique events
            cursor.execute("""
                SELECT subject_used, 
                       COUNT(id) as sent,
                       (SELECT COUNT(DISTINCT recipient_id) FROM events e WHERE e.event_type = 'open' AND e.recipient_id IN (SELECT id FROM recipients r2 WHERE r2.campaign_id = ? AND r2.subject_used = recipients.subject_used)) as opens
                FROM recipients
                WHERE campaign_id = ?
                GROUP BY subject_used
            """, (campaign_id, campaign_id))
            return [dict(row) for row in cursor.fetchall()]

    def get_latest_campaign(self):
        with self.get_connection() as conn:
            cursor = conn.cursor()
            cursor.execute("SELECT * FROM campaigns ORDER BY created_at DESC LIMIT 1")
            return cursor.fetchone()

db = Database()

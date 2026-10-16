import sqlite3
import secrets
import os

DB_PATH = "saas_engine.db"

def init_db():
    conn = sqlite3.connect(DB_PATH)
    cursor = conn.cursor()
    
    # 1. Users Table
    cursor.execute("""
    CREATE TABLE IF NOT EXISTS users (
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        email TEXT UNIQUE NOT NULL,
        tier TEXT NOT NULL DEFAULT 'starter',
        scans_used INTEGER DEFAULT 0,
        api_key TEXT UNIQUE,
        created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
    )
    """)
    conn.commit()
    conn.close()

def create_user(email: str, tier: str = "starter"):
    conn = sqlite3.connect(DB_PATH)
    cursor = conn.cursor()
    api_key = f"sk_live_{secrets.token_hex(16)}" if tier == "enterprise" else None
    try:
        cursor.execute("INSERT INTO users (email, tier, api_key) VALUES (?, ?, ?)", (email, tier, api_key))
        conn.commit()
        return {"status": "success", "email": email, "tier": tier, "api_key": api_key}
    except sqlite3.IntegrityError:
        return {"status": "error", "message": "User already exists."}
    finally:
        conn.close()

def check_user_scan_quota(email: str) -> dict:
    conn = sqlite3.connect(DB_PATH)
    cursor = conn.cursor()
    cursor.execute("SELECT tier, scans_used, api_key FROM users WHERE email = ?", (email,))
    row = cursor.fetchone()
    conn.close()

    if not row:
        return {"allowed": False, "reason": "User not found."}

    tier, scans_used, api_key = row
    
    if tier == "starter" and scans_used >= 200:
        return {"allowed": False, "reason": "Monthly 200-scan limit exhausted. Upgrade to Pro."}

    # Increment scan count
    conn = sqlite3.connect(DB_PATH)
    cursor = conn.cursor()
    cursor.execute("UPDATE users SET scans_used = scans_used + 1 WHERE email = ?", (email,))
    conn.commit()
    conn.close()

    return {"allowed": True, "tier": tier, "scans_used": scans_used + 1, "api_key": api_key}

if __name__ == "__main__":
    init_db()
    print("[+] Database initialized successfully.")
    res = create_user("agency_owner@test.com", "starter")
    print("[+] Seed User:", res)
    quota = check_user_scan_quota("agency_owner@test.com")
    print("[+] Quota Check:", quota)

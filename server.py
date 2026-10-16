import json
import sqlite3
from flask import Flask, request, jsonify, render_template
from core.scanner import AuditScanner
from tiers.manager import TierManager
from core.db import check_user_scan_quota, create_user, init_db, DB_PATH

init_db()

app = Flask(__name__)

@app.route("/", methods=["GET"])
def render_dashboard():
    return render_template("index.html")

@app.route("/api/v1/users/register", methods=["POST"])
def register_user():
    data = request.get_json(silent=True) or {}
    email = data.get("email")
    tier = data.get("tier", "starter").lower()
    if not email:
        return jsonify({"error": "Email is required."}), 400
    res = create_user(email, tier)
    return jsonify(res)

# Payment Webhook: Upgrades user plan when money is received
@app.route("/api/v1/webhook/payment", methods=["POST"])
def payment_webhook():
    payload = request.get_json(silent=True) or {}
    email = payload.get("email")
    new_tier = payload.get("tier", "agency_pro").lower()

    if not email:
        return jsonify({"error": "Missing customer email"}), 400

    conn = sqlite3.connect(DB_PATH)
    cursor = conn.cursor()
    cursor.execute("UPDATE users SET tier = ?, scans_used = 0 WHERE email = ?", (new_tier, email))
    conn.commit()
    conn.close()

    return jsonify({"status": "SUCCESS", "message": f"User {email} successfully upgraded to {new_tier}!"}), 200

@app.route("/api/v1/audit", methods=["POST"])
def run_telemetry_audit():
    body = request.get_json(silent=True) or {}
    target = body.get("target")
    email = body.get("user_email", "agency_owner@test.com")
    
    if not target:
        return jsonify({"error": "Target domain/URL is required."}), 400

    quota_info = check_user_scan_quota(email)
    if not quota_info.get("allowed"):
        return jsonify({"error": quota_info.get("reason")}), 429

    user_tier = quota_info.get("tier", "starter")

    if user_tier == "enterprise":
        auth_header = request.headers.get("Authorization", "")
        if not auth_header.startswith("Bearer "):
            return jsonify({"error": "Enterprise tier requires a valid Bearer API Key."}), 401

    try:
        scanner = AuditScanner(target)
        raw_scan = scanner.run_full_audit()

        branding = {
            "agency_name": body.get("agency_name", "AuditOps B2B"),
            "contact_email": body.get("contact_email", email),
            "logo_text": body.get("logo_text", "AUDITOPS")
        }
        mgr = TierManager(tier_name=user_tier, agency_branding=branding)
        structured_response = mgr.format_output(raw_scan)
        
        structured_response["quota"] = {
            "user": email,
            "tier": user_tier,
            "scans_used": quota_info.get("scans_used"),
            "limit": 200 if user_tier == "starter" else "Unlimited"
        }

        return jsonify(structured_response), 200

    except Exception as e:
        return jsonify({"error": f"Internal Engine Error: {str(e)}"}), 500

if __name__ == "__main__":
    app.run(host="0.0.0.0", port=5000, debug=False)

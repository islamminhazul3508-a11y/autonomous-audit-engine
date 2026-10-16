class TierManager:
    TIERS = {
        "starter": {
            "name": "Starter",
            "price_usd": 29,
            "scan_limit": 200,
            "whitelabel": False,
            "auto_pitch": False,
            "api_access": False
        },
        "agency_pro": {
            "name": "Agency Pro",
            "price_usd": 99,
            "scan_limit": None,  # Unlimited
            "whitelabel": True,
            "auto_pitch": True,
            "api_access": False
        },
        "enterprise": {
            "name": "Enterprise",
            "price_usd": 299,
            "scan_limit": None,  # Unlimited
            "whitelabel": True,
            "auto_pitch": True,
            "api_access": True
        }
    }

    def __init__(self, tier_name: str = "starter", agency_branding: dict = None):
        tier_key = tier_name.lower()
        if tier_key not in self.TIERS:
            raise ValueError(f"Unknown tier: {tier_name}. Choose from starter, agency_pro, enterprise.")
        
        self.tier_key = tier_key
        self.config = self.TIERS[tier_key]
        self.usage_count = 0
        self.agency_branding = agency_branding or {
            "agency_name": "AuditOps Enterprise",
            "contact_email": "ops@auditops.io",
            "logo_text": "[AuditOps Telemetry]"
        }

    def can_scan(self) -> bool:
        limit = self.config["scan_limit"]
        if limit is None:
            return True
        return self.usage_count < limit

    def record_scan(self):
        self.usage_count += 1

    def format_output(self, scan_data: dict) -> dict:
        self.record_scan()
        
        # 1. Base response
        response = {
            "tier": self.config["name"],
            "scan_id": self.usage_count,
            "data": scan_data,
            "branding": "Powered by AuditEngine Core"
        }

        # 2. Agency Pro Feature: White-labeling
        if self.config["whitelabel"]:
            response["branding"] = f"Audited by {self.agency_branding['agency_name']} ({self.agency_branding['logo_text']})"
        
        # 3. Agency Pro Feature: Automated Client Acquisition Pitch
        if self.config["auto_pitch"]:
            target = scan_data.get("target", "Target Site")
            latency = scan_data.get("latency_ms", 0)
            missing_headers = [
                h for h, val in scan_data.get("security_headers", {}).items() 
                if val.get("status") == "MISSING"
            ]
            
            pitch = (
                f"Subject: Executive Security & Telemetry Audit: {target}\n\n"
                f"Hi Leadership Team,\n\n"
                f"Our passive audit engine flagged potential vulnerabilities on {target}:\n"
                f"1. Baseline Latency: {latency} ms\n"
                f"2. Unprotected Headers: {', '.join(missing_headers) if missing_headers else 'None'}\n"
                f"3. SSL Status: {scan_data.get('ssl', {}).get('status', 'Operational')}\n\n"
                f"Would you like our agency ({self.agency_branding['agency_name']}) to patch these configurations?\n"
                f"Contact: {self.agency_branding['contact_email']}"
            )
            response["client_pitch"] = pitch

        # 4. Enterprise Feature: High-throughput API metadata
        if self.config["api_access"]:
            response["api_engine"] = {
                "format": "REST_JSON_STRICT",
                "bulk_ready": True,
                "status": 200
            }

        return response

if __name__ == "__main__":
    print("Testing Tier Manager...")
    mgr = TierManager(tier_name="agency_pro", agency_branding={"agency_name": "Apex Digital", "contact_email": "ceo@apexdigital.com", "logo_text": "APEX_SHIELD"})
    mock_data = {
        "target": "example.com",
        "latency_ms": 120.5,
        "ssl": {"status": "VALID"},
        "security_headers": {
            "Strict-Transport-Security": {"status": "MISSING"},
            "Content-Security-Policy": {"status": "MISSING"}
        }
    }
    output = mgr.format_output(mock_data)
    print("Tier:", output["tier"])
    print("Branding:", output["branding"])
    print("Pitch Attached:", "client_pitch" in output)

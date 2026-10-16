import json
from rich.console import Console
from rich.table import Table
from rich.panel import Panel

console = Console()

class ReportGenerator:
    def __init__(self, audit_response: dict):
        self.response = audit_response
        self.data = audit_response.get("data", {})
        self.tier = audit_response.get("tier", "Starter")
        self.branding = audit_response.get("branding", "AuditEngine Core")

    def display_terminal_summary(self):
        target = self.data.get("target", "Target")
        latency = self.data.get("latency_ms", "N/A")
        ssl_info = self.data.get("ssl", {})
        
        console.print(Panel(f"[bold cyan]TELEMETRY AUDIT REPORT: {target}[/bold cyan]\n[yellow]{self.branding}[/yellow] | Tier: [green]{self.tier}[/green]"))
        
        # Meta Table
        meta_table = Table(title="1. Infrastructure Baseline", header_style="bold magenta")
        meta_table.add_column("Parameter", style="dim")
        meta_table.add_column("Value")
        meta_table.add_row("Latency", f"{latency} ms")
        meta_table.add_row("SSL Status", f"[green]{ssl_info.get('status')}[/green]")
        meta_table.add_row("SSL Issuer", ssl_info.get("issuer", "Unknown"))
        meta_table.add_row("SSL Expiry", ssl_info.get("expires", "Unknown"))
        console.print(meta_table)

        # Headers Table
        header_table = Table(title="2. Defensive Header Posture", header_style="bold blue")
        header_table.add_column("Security Header")
        header_table.add_column("Status")
        header_table.add_column("Risk Flag")
        
        for h, info in self.data.get("security_headers", {}).items():
            st = info.get("status")
            st_styled = "[green]SECURED[/green]" if st == "SECURED" else "[red]MISSING[/red]"
            header_table.add_row(h, st_styled, info.get("risk", "None"))
        console.print(header_table)

        # Client Pitch (if Pro/Enterprise)
        if "client_pitch" in self.response:
            console.print(Panel(self.response["client_pitch"], title="[bold green]Automated VIP Client Acquisition Pitch[/bold green]", border_style="green"))

    def export_markdown(self, filename: str = "audit_report.md") -> str:
        target = self.data.get("target", "Target")
        latency = self.data.get("latency_ms", "N/A")
        ssl_info = self.data.get("ssl", {})

        md = []
        md.append(f"# Infrastructure & Security Telemetry: {target}\n")
        md.append(f"> **Audited By:** {self.branding}  \n")
        md.append(f"> **Engine Tier:** {self.tier}\n\n")
        
        md.append("## 1. Baseline Performance\n")
        md.append(f"- **Server Latency:** {latency} ms\n")
        md.append(f"- **SSL Certificate:** {ssl_info.get('status')} ({ssl_info.get('issuer')})\n")
        md.append(f"- **Certificate Expiry:** {ssl_info.get('expires')}\n\n")

        md.append("## 2. Defensive Security Posture\n")
        md.append("| Header | Status | Risk Assessment |\n")
        md.append("| :--- | :--- | :--- |\n")
        for h, info in self.data.get("security_headers", {}).items():
            md.append(f"| `{h}` | {info.get('status')} | {info.get('risk')} |\n")
        md.append("\n")

        if "client_pitch" in self.response:
            md.append("## 3. Executive Outbound Pitch\n")
            md.append("```text\n")
            md.append(self.response["client_pitch"] + "\n")
            md.append("```\n")

        with open(filename, "w", encoding="utf-8") as f:
            f.write("".join(md))
        
        return filename

if __name__ == "__main__":
    from core.scanner import AuditScanner
    from tiers.manager import TierManager

    scanner = AuditScanner("example.com")
    raw_data = scanner.run_full_audit()

    mgr = TierManager(tier_name="agency_pro", agency_branding={"agency_name": "AuditOps B2B", "contact_email": "hello@auditops.io", "logo_text": "AUDITOPS"})
    structured_data = mgr.format_output(raw_data)

    rep = ReportGenerator(structured_data)
    rep.display_terminal_summary()
    saved_file = rep.export_markdown("test_report.md")
    print(f"\n[+] Full Executive Markdown Report exported to: {saved_file}")

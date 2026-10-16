import re

# Update HTML template with Monetization Paywall
html_path = "templates/index.html"
with open(html_path, "r", encoding="utf-8") as f:
    content = f.read()

pricing_html = """
    <!-- SaaS Pricing & Paywall Section ($29, $99, $299) -->
    <div style="margin-top: 40px; border-top: 1px solid #334155; padding-top: 30px;">
        <h2 style="text-align: center; color: #f8fafc; font-size: 24px; margin-bottom: 8px;">Upgrade Your Audit Plan</h2>
        <p style="text-align: center; color: #94a3b8; font-size: 14px; margin-bottom: 25px;">Automate audits, unlock white-label reports, and scale client acquisition.</p>
        
        <div style="display: flex; flex-direction: column; gap: 20px;">
            <!-- Starter $29 -->
            <div style="background: #1e293b; border: 1px solid #334155; border-radius: 12px; padding: 20px;">
                <div style="display: flex; justify-content: space-between; align-items: center;">
                    <span style="color: #38bdf8; font-weight: bold; font-size: 18px;">Starter Tier</span>
                    <span style="font-size: 22px; font-weight: 800; color: #fff;">$29 <span style="font-size: 12px; color: #94a3b8;">/ mo</span></span>
                </div>
                <p style="color: #cbd5e1; font-size: 13px; margin: 10px 0;">50 Automated Audits/mo + Basic PDF Export</p>
                <button style="width: 100%; background: #2563eb; color: white; border: none; padding: 10px; border-radius: 6px; font-weight: 600; cursor: pointer;">Subscribe Starter ($29)</button>
            </div>

            <!-- Agency $99 -->
            <div style="background: #0f172a; border: 2px solid #38bdf8; border-radius: 12px; padding: 20px; position: relative;">
                <span style="position: absolute; top: -10px; right: 20px; background: #38bdf8; color: #0f172a; font-size: 11px; font-weight: bold; padding: 2px 8px; border-radius: 20px;">MOST POPULAR</span>
                <div style="display: flex; justify-content: space-between; align-items: center;">
                    <span style="color: #38bdf8; font-weight: bold; font-size: 18px;">Agency Pro</span>
                    <span style="font-size: 22px; font-weight: 800; color: #fff;">$99 <span style="font-size: 12px; color: #94a3b8;">/ mo</span></span>
                </div>
                <p style="color: #cbd5e1; font-size: 13px; margin: 10px 0;">250 Audits/mo + Custom White-Label Client Reports</p>
                <button style="width: 100%; background: #0284c7; color: white; border: none; padding: 10px; border-radius: 6px; font-weight: 600; cursor: pointer;">Subscribe Agency ($99)</button>
            </div>

            <!-- Enterprise $299 -->
            <div style="background: #1e293b; border: 1px solid #334155; border-radius: 12px; padding: 20px;">
                <div style="display: flex; justify-content: space-between; align-items: center;">
                    <span style="color: #a855f7; font-weight: bold; font-size: 18px;">Enterprise Core</span>
                    <span style="font-size: 22px; font-weight: 800; color: #fff;">$299 <span style="font-size: 12px; color: #94a3b8;">/ mo</span></span>
                </div>
                <p style="color: #cbd5e1; font-size: 13px; margin: 10px 0;">Unlimited Audits + Full Automation API & Weekly Monitoring</p>
                <button style="width: 100%; background: #7c3aed; color: white; border: none; padding: 10px; border-radius: 6px; font-weight: 600; cursor: pointer;">Subscribe Enterprise ($299)</button>
            </div>
        </div>
    </div>
"""

if "Upgrade Your Audit Plan" not in content:
    # Append before closing container or body
    if "</div>" in content:
        content = content[::-1].replace("</div>"[::-1], ("</div>" + pricing_html)[::-1], 1)[::-1]
    with open(html_path, "w", encoding="utf-8") as f:
        f.write(content)
    print("✅ Pricing section successfully added to template!")
else:
    print("ℹ️ Pricing section already exists.")

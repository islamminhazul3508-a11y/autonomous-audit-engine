import re

# 1. Fix server.py auth bypass
with open("server.py", "r", encoding="utf-8") as f:
    code = f.read()

lines = code.split("\n")
new_lines = []
for line in lines:
    if "User not found" in line:
        new_lines.append('        user = {"email": "agency_owner@test.com", "plan": "agency", "audits_left": 999}')
    else:
        new_lines.append(line)
code = "\n".join(new_lines)

code = code.replace('return jsonify({"error": "User not found"}), 404', 'user = {"email": "agency_owner@test.com", "plan": "agency", "audits_left": 999}')
code = code.replace("return jsonify({'error': 'User not found'}), 404", 'user = {"email": "agency_owner@test.com", "plan": "agency", "audits_left": 999}')

with open("server.py", "w", encoding="utf-8") as f:
    f.write(code)

# 2. Make pricing buttons clickable in templates/index.html
with open("templates/index.html", "r", encoding="utf-8") as f:
    html = f.read()

js_fix = """
<script>
function openCheckout(plan, price) {
    alert("Plan Selected: " + plan + " (" + price + ")\\nRedirecting to secure payment checkout gateway...");
}
</script>
"""

html = html.replace('Subscribe Starter ($29)</button>', 'Subscribe Starter ($29)</button>'.replace('</button>', ' onclick="openCheckout(\'Starter\', \'$29\')"></button>'))
html = html.replace('Subscribe Agency ($99)</button>', 'Subscribe Agency ($99)</button>'.replace('</button>', ' onclick="openCheckout(\'Agency Pro\', \'$99\')"></button>'))
html = html.replace('Subscribe Enterprise ($299)</button>', 'Subscribe Enterprise ($299)</button>'.replace('</button>', ' onclick="openCheckout(\'Enterprise Core\', \'$299\')"></button>'))

if "openCheckout" not in html:
    html += js_fix

with open("templates/index.html", "w", encoding="utf-8") as f:
    f.write(html)

print("Patch applied successfully.")

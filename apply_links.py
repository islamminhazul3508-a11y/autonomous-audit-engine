with open("templates/index.html", "r", encoding="utf-8") as f:
    content = f.read()

# Replace or add direct Razorpay links
content = content.replace('href="#"', 'href="https://rzp.io/l/Tod4qzqB58bGoM"', 1)

# Adding the exact links to pricing buttons
p1 = "https://rzp.io/l/Tod4qzqB58bGoM"
p2 = "https://rzp.io/l/Tod6W2weZ9yMjC"
p3 = "https://rzp.io/l/Tod6yS26jni5dz"

import re
# Replace button onclick/href or wrap in links
content = re.sub(r'(<button[^>]*>.*?29.*?</button>)', rf'<a href="{p1}" target="_blank" style="text-decoration:none;">\1</a>', content)
content = re.sub(r'(<button[^>]*>.*?99.*?</button>)', rf'<a href="{p2}" target="_blank" style="text-decoration:none;">\1</a>', content)
content = re.sub(r'(<button[^>]*>.*?299.*?</button>)', rf'<a href="{p3}" target="_blank" style="text-decoration:none;">\1</a>', content)

with open("templates/index.html", "w", encoding="utf-8") as f:
    f.write(content)

print("Razorpay Links successfully linked to buttons!")

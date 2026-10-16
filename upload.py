import subprocess

token = input("\n👉 Apna Token yahan Paste karein aur Enter dabayein: ").strip()
url = f"https://islamminhazul3508-a11y:{token}@github.com/islamminhazul3508-a11y/autonomous-audit-engine.git"
subprocess.run(["git", "remote", "set-url", "origin", url])
print("\n⏳ Uploading to GitHub...")
res = subprocess.run(["git", "push", "-u", "origin", "main"])
if res.returncode == 0:
    print("\n🎉 SUCCESS! Code GitHub par upload ho gaya!")
else:
    print("\n❌ Token me galti hai ya permission nahi hai.")

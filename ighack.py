import time
import sys
import os
import random
from itertools import cycle
import re

try:
    import instaloader
    HAS_INSTALOADER = True
except ImportError:
    HAS_INSTALOADER = False

# ===== Colors =====
GREEN  = "\033[92m"
RED    = "\033[91m"
WHITE  = "\033[97m"
PINK   = "\033[95m"
BLUE   = "\033[94m"
RESET  = "\033[0m"
BOLD   = "\033[1m"

COLORS = [GREEN, RED, WHITE, PINK, BLUE]

# ===== IG Banner =====
BANNER = f"""{RED}
██╗███╗   ██╗███████╗████████╗ █████╗      ██╗  ██╗ █████╗  ██████╗██╗  ██╗
██║████╗  ██║██╔════╝╚══██╔══╝██╔══██╗     ██║  ██║██╔══██╗██╔════╝██║ ██╔╝
██║██╔██╗ ██║███████╗   ██║   ███████║     ███████║███████║██║     █████╔╝ 
██║██║╚██╗██║╚════██║   ██║   ██╔══██║     ██╔══██║██╔══██║██║     ██╔═██╗ 
██║██║ ╚████║███████║   ██║   ██║  ██║     ██║  ██║██║  ██║╚██████╗██║  ██╗
╚═╝╚═╝  ╚═══╝╚══════╝   ╚═╝   ╚═╝  ╚═╝     ╚═╝  ╚═╝╚═╝  ╚═╝ ╚═════╝╚═╝  ╚═╝
{RESET}"""
# ===== Fake Hacker Logs =====
LOGS = [
    "Breaking password hashes...",
    "Bypassing 2FA challenge...",
    "Spoofing OTP validation...",
    "Extracting session cookies...",
    "Escalating admin privileges...",
    "Installing stealth backdoor...",
    "Finalizing root access...",
]

def slow_print(text, delay=0.02, color=GREEN):
    for c in text:
        sys.stdout.write(color + c + RESET)
        sys.stdout.flush()
        time.sleep(delay)
    print()

def spin_step(label, steps=25, step_delay=0.04, color=BLUE):
    """Spinner for pro hacker effect"""
    sp = cycle("|/-\\")
    for _ in range(steps):
        sys.stdout.write(f"\r{color}[*] {label:<40} {next(sp)}{RESET}")
        sys.stdout.flush()
        time.sleep(step_delay)
    sys.stdout.write("\r" + " " * (len(label) + 20) + "\r")
    sys.stdout.flush()

def progress_bar(task="Processing", length=50, duration=5, color=RED):
    for i in range(length + 1):
        bar = "#" * i + "-" * (length - i)
        pct = int((i / length) * 100)
        sys.stdout.write(f"\r{color}{task:<20}: [{bar}] {pct:3d}%{RESET}")
        sys.stdout.flush()
        time.sleep(duration / length)
    print()

def extract_other_account(bio_text):
    """Check if bio contains another IG handle"""
    match = re.findall(r"@([A-Za-z0-9_.]+)", bio_text)
    return match[0] if match else None

def get_profile_info(username):
    """Fetch real IG profile info"""
    if not HAS_INSTALOADER:
        return None
    try:
        loader = instaloader.Instaloader()
        profile = instaloader.Profile.from_username(loader.context, username)
        other_acc = extract_other_account(profile.biography)
        return {
            "username": profile.username,
            "full_name": profile.full_name,
            "followers": profile.followers,
            "following": profile.followees,
            "posts": profile.mediacount,
            "other_acc": other_acc
        }
    except Exception:
        return None

# ===== RUN =====
os.system("clear")
print(BANNER)

username = input(GREEN + "[+] Enter Instagram username: " + RESET)

# === Show Public Profile Info ===
profile = get_profile_info(username)
if profile:
    print(BLUE + f"\n[*] Extracted Public Profile Data for @{username}" + RESET)
    print(PINK  + f"    Full Name : {profile['full_name']}" + RESET)
    print(WHITE + f"    Followers : {profile['followers']}" + RESET)
    print(GREEN + f"    Following : {profile['following']}" + RESET)
    print(RED   + f"    Posts     : {profile['posts']}" + RESET)
    if profile["other_acc"]:
        print(BLUE + f"    Other Acc : @{profile['other_acc']}" + RESET)
else:
    print(RED + "[!] Could not fetch profile data (maybe private or instaloader not installed)" + RESET)

time.sleep(2)
print()

# === Fake Hacker Simulation ===
for log in LOGS:
    color = random.choice(COLORS)
    spin_step(log, steps=18, step_delay=0.05, color=color)
    slow_print(f"[*] {log} [OK]", delay=0.002, color=color)

progress_bar("Executing exploit", length=50, duration=5, color=RED)

time.sleep(1)
print("\n" + GREEN + BOLD + ">>> Valla Panikkum Poda..." + RESET + "\n")

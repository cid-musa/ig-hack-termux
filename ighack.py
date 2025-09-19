#!/usr/bin/env python3
"""
Termux-ready IG HACK reel script with the user-provided ASCII "INSTA HACK" title.
Visual mock only. Optional: `pip install instaloader` to fetch public profile stats.
"""

import os
import sys
import time
import random
import shutil
import re
from itertools import cycle

# Optional instaloader
try:
    import instaloader
    HAS_INSTALOADER = True
except Exception:
    HAS_INSTALOADER = False

# ===== Colors =====
GREEN = "\033[92m"
RED   = "\033[91m"
WHITE = "\033[97m"
PINK  = "\033[95m"
BLUE  = "\033[94m"
BOLD  = "\033[1m"
RESET = "\033[0m"
COLORS = [GREEN, RED, WHITE, PINK, BLUE]

# ===== Utilities =====
def term_size():
    try:
        s = shutil.get_terminal_size()
        return s.columns, s.lines
    except Exception:
        return 80, 24

def strip_ansi(s):
    return re.sub(r'\033\[[0-9;]*m', '', s)

def center_line(s, width):
    plain = strip_ansi(s)
    pad = max((width - len(plain)) // 2, 0)
    return " " * pad + s

def clear():
    os.system("clear" if os.name != "nt" else "cls")

def slow_print(text, delay=0.02, color=GREEN):
    for ch in text:
        sys.stdout.write(color + ch + RESET)
        sys.stdout.flush()
        time.sleep(delay)
    print()

def tprint(text, color=WHITE):
    sys.stdout.write(color + text + RESET + "\n")
    sys.stdout.flush()

# ===== User ASCII TITLE (cleaned & aligned) =====
TITLE_LINES = [
"▗▄▄▄▖ ▗▄▄▖    ▗▖ ▗▖ ▗▄▖  ▗▄▄▖▗▖ ▗▖",
"  █  ▐▌       ▐▌ ▐▌▐▌ ▐▌▐▌   ▐▌▗▞▘",
"  █  ▐▌▝▜▌    ▐▛▀▜▌▐▛▀▜▌▐▌   ▐▛▚▖ ",
"▗▄█▄▖▝▚▄▞▘    ▐▌ ▐▌▐▌ ▐▌▝▚▄▄▖▐▌ ▐▌",
"                                      ",
"                                      "
]

# ===== Fake cracking data =====
COMMON = ["password","123456","qwerty","insta2025","letmein","admin","passw0rd"]

def fake_crack(duration=3, width=40):
    start = time.time()
    sp = cycle("|/-\\")
    while time.time() - start < duration:
        pwd = random.choice(COMMON) + random.choice(["", "!", "123", "@2025", "#$"])
        left = f"[crack] trying: {pwd}"
        sys.stdout.write("\r" + BLUE + left.ljust(width) + " " + next(sp) + RESET)
        sys.stdout.flush()
        time.sleep(0.06 + random.random() * 0.03)
    found = "*" * random.randint(8, 12)
    sys.stdout.write("\r" + GREEN + f"[crack] FOUND: {found}".ljust(width) + "   " + RESET + "\n")
    sys.stdout.flush()
    time.sleep(0.6)

def spinner_label(label, steps=20, delay=0.04, color=BLUE):
    sp = cycle("|/-\\")
    for _ in range(steps):
        sys.stdout.write("\r" + color + f"[*] {label:<40} {next(sp)}" + RESET)
        sys.stdout.flush()
        time.sleep(delay)
    sys.stdout.write("\r" + " " * 100 + "\r")
    sys.stdout.flush()

def progress_bar(task="Processing", total=30, color=RED):
    cols, _ = term_size()
    bar_w = max(min(cols - 30, 40), 20)
    for i in range(total + 1):
        filled = int((i / total) * bar_w)
        bar = "#" * filled + "-" * (bar_w - filled)
        pct = int((i / total) * 100)
        sys.stdout.write(f"\r{color}{task:<12}: [{bar}] {pct:3d}%{RESET}")
        sys.stdout.flush()
        time.sleep(0.06)
    print()

# ===== instaloader helper (optional) =====
def extract_other_account(bio):
    m = re.findall(r"@([A-Za-z0-9_.]+)", bio or "")
    return m[0] if m else None

def get_profile_info(username):
    if not HAS_INSTALOADER:
        return None
    try:
        L = instaloader.Instaloader()
        profile = instaloader.Profile.from_username(L.context, username)
        other = extract_other_account(profile.biography)
        return {
            "username": profile.username,
            "full_name": profile.full_name,
            "followers": profile.followers,
            "following": profile.followees,
            "posts": profile.mediacount,
            "other_acc": other
        }
    except Exception:
        return None

# ===== Render title centered + colored lines =====
def render_title(width):
    out = []
    # shrink or pad lines to fit width roughly (we just center)
    for i, ln in enumerate(TITLE_LINES):
        color = COLORS[i % len(COLORS)]
        out.append(center_line(color + ln + RESET, width))
    # a small IG square under title for branding
    ig_square = center_line(PINK + "╔════╗  IG HACK" + RESET, width)
    out.append(ig_square)
    return "\n".join(out)

# ===== Main =====
def main():
    clear()
    cols, _ = term_size()
    print("\n" + render_title(cols) + "\n")

    sys.stdout.write(GREEN + "[+] Enter Instagram username: " + RESET)
    sys.stdout.flush()
    try:
        username = input().strip()
    except KeyboardInterrupt:
        print("\n" + RED + "Aborted." + RESET)
        return

    if not username:
        print(RED + "No username provided. Exiting." + RESET)
        return

    # Attempt public fetch (optional)
    profile = get_profile_info(username)
    if profile:
        tprint("\n" + BLUE + f"[*] Extracted Public Profile Data for @{username}" + RESET)
        tprint(PINK  + f"    Full Name : {profile.get('full_name','-')}" + RESET)
        tprint(WHITE + f"    Followers : {profile.get('followers','-')}" + RESET)
        tprint(GREEN + f"    Following : {profile.get('following','-')}" + RESET)
        tprint(RED   + f"    Posts     : {profile.get('posts','-')}" + RESET)
        if profile.get("other_acc"):
            tprint(BLUE + f"    Other Acc : @{profile['other_acc']}" + RESET)
    else:
        tprint("\n" + RED + "[!] Could not fetch profile data (instaloader missing or profile private)" + RESET)

    time.sleep(0.7)
    tprint("\n" + PINK + "[*] Initiating reconnaissance..." + RESET)
    spinner_label("Scanning public endpoints", steps=16, delay=0.04, color=WHITE)

    tprint("\n" + BLUE + "[*] Breaking password hashes..." + RESET)
    fake_crack(duration=2.5, width=cols - 10)

    spinner_label("Bypassing 2FA challenge", steps=14, delay=0.06, color=RED)
    slow_print("[*] Spoofing OTP validation...", delay=0.005, color=RED)
    time.sleep(0.4)
    slow_print("[*] Injecting session token...", delay=0.005, color=GREEN)
    time.sleep(0.3)

    steps = [
        "Extracting session cookies...",
        "Escalating admin privileges...",
        "Installing stealth backdoor..."
    ]
    for s in steps:
        spinner_label(s, steps=12, delay=0.05, color=random.choice(COLORS))
        slow_print(f"[*] {s} [OK]", delay=0.002, color=random.choice(COLORS))

    progress_bar("Executing exploit", total=28, color=RED)

    time.sleep(0.8)
    # Final exact line per request (medium/plain green)
    print("\n" + GREEN + "Valla Panikkum Poda..." + RESET + "\n")

if __name__ == "__main__":
    main()

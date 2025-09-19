#!/usr/bin/env python3
"""
Termux-ready IG HACK reel script
- Single big centered bold title "INSTA HACK" with color fade effect
- Subtitle: [Instagram - Xyberkruze]
- Final message "Valla Panikkum Poda..." scrolling down infinitely with color/font variations
- Optional: `pip install instaloader` to enable public profile fetch (visual only)
"""

import os
import sys
import time
import random
import shutil
import re
from itertools import cycle

try:
    import instaloader
    HAS_INSTALOADER = True
except Exception:
    HAS_INSTALOADER = False

# ===== Colors =====
GREEN  = "\033[92m"
RED    = "\033[91m"
WHITE  = "\033[97m"
PINK   = "\033[95m"
BLUE   = "\033[94m"
YELLOW = "\033[93m"
BOLD   = "\033[1m"
RESET  = "\033[0m"
PALETTE = [GREEN, RED, WHITE, PINK, BLUE, YELLOW]

# ===== Utilities =====
def term_size():
    try:
        s = shutil.get_terminal_size()
        return s.columns, s.lines
    except:
        return 80, 24

def strip_ansi(s):
    return re.sub(r'\033\[[0-9;]*m', '', s)

def center(text, width):
    plain = strip_ansi(text)
    pad = max((width - len(plain)) // 2, 0)
    return " " * pad + text

def clear():
    os.system("clear" if os.name != "nt" else "cls")

def tprint(text, color=WHITE):
    sys.stdout.write(color + text + RESET + "\n")
    sys.stdout.flush()

def slow_print(text, delay=0.01, color=GREEN):
    for ch in text:
        sys.stdout.write(color + ch + RESET)
        sys.stdout.flush()
        time.sleep(delay)
    print()

# ===== Fake cracking helpers =====
COMMON = ["password","123456","qwerty","insta2025","letmein","admin","passw0rd"]

def fake_crack(duration=2.5, width=40):
    start = time.time()
    sp = cycle("|/-\\")
    while time.time() - start < duration:
        pwd = random.choice(COMMON) + random.choice(["", "!", "123", "@2025", "#$"])
        left = f"[crack] trying: {pwd}"
        sys.stdout.write("\r" + BLUE + left.ljust(width) + " " + next(sp) + RESET)
        sys.stdout.flush()
        time.sleep(0.05 + random.random() * 0.03)
    found = "*" * random.randint(8, 12)
    sys.stdout.write("\r" + GREEN + f"[crack] FOUND: {found}".ljust(width) + "   " + RESET + "\n")
    sys.stdout.flush()
    time.sleep(0.5)

def spinner(label, steps=18, delay=0.04, color=WHITE):
    sp = cycle("|/-\\")
    for _ in range(steps):
        sys.stdout.write("\r" + color + f"[*] {label:<36} {next(sp)}" + RESET)
        sys.stdout.flush()
        time.sleep(delay)
    sys.stdout.write("\r" + " " * 80 + "\r")
    sys.stdout.flush()

def progress_bar(task="Processing", total=28, color=RED):
    cols, _ = term_size()
    bar_w = max(min(cols - 30, 44), 20)
    for i in range(total + 1):
        filled = int((i / total) * bar_w)
        bar = "#" * filled + "-" * (bar_w - filled)
        pct = int((i / total) * 100)
        sys.stdout.write(f"\r{color}{task:<14}: [{bar}] {pct:3d}%{RESET}")
        sys.stdout.flush()
        time.sleep(0.06)
    print()

# ===== Instaloader helpers (optional) =====
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
            "other": other
        }
    except Exception:
        return None

# ===== Title =====
def render_title(width):
    title = "INSTA HACK"
    subtitle = "[Instagram - Xyberkruze]"
    return center(BOLD + RED + title + RESET, width) + "\n" + center(WHITE + subtitle + RESET, width)

# ===== Final scrolling message =====
def final_message_loop(cols):
    final_msg = "Valla Panikkum Poda..."
    styles = [(GREEN, True), (PINK, True), (BLUE, True), (YELLOW, True), (WHITE, False)]
    try:
        idx = 0
        while True:
            color, bold = styles[idx % len(styles)]
            txt = (BOLD if bold else "") + color + final_msg + RESET
            print(center(txt, cols))
            idx += 1
            time.sleep(0.6)
    except KeyboardInterrupt:
        print("\n" + RED + "Exiting..." + RESET)
        return

# ===== Main =====
def main():
    clear()
    cols, rows = term_size()

    # Title fade effect
    for _ in range(2):
        for color in [RED, PINK, GREEN]:
            clear()
            print(center(BOLD + color + "INSTA HACK" + RESET, cols))
            print(center(WHITE + "[Instagram - Xyberkruze]" + RESET, cols))
            time.sleep(0.5)

    # Prompt username
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

    # Optional public profile fetch
    profile = get_profile_info(username)
    if profile:
        tprint("\n" + BLUE + f"[*] Public data for @{username}" + RESET)
        tprint(PINK  + f"    Name     : {profile.get('full_name','-')}" + RESET)
        tprint(WHITE + f"    Followers: {profile.get('followers','-')}" + RESET)
        tprint(GREEN + f"    Following: {profile.get('following','-')}" + RESET)
        tprint(RED   + f"    Posts    : {profile.get('posts','-')}" + RESET)
        if profile.get('other'):
            tprint(BLUE + f"    Other Acc: @{profile['other']}" + RESET)
    else:
        tprint("\n" + RED + "[!] Could not fetch profile data (instaloader missing or profile private)" + RESET)

    time.sleep(0.6)
    tprint("\n" + PINK + "[*] Initiating reconnaissance..." + RESET)
    spinner("Scanning public endpoints", steps=16, delay=0.04, color=WHITE)

    tprint("\n" + BLUE + "[*] Breaking password hashes..." + RESET)
    fake_crack(duration=2.5, width=cols - 8)

    spinner("Bypassing 2FA challenge", steps=14, delay=0.06, color=RED)
    slow_print("[*] Spoofing OTP validation...", delay=0.004, color=RED)
    time.sleep(0.3)
    slow_print("[*] Injecting session token...", delay=0.004, color=GREEN)
    time.sleep(0.25)

    for s in ["Extracting session cookies...", "Escalating privileges...", "Installing stealth module..."]:
        spinner(s, steps=12, delay=0.05, color=random.choice(PALETTE))
        slow_print(f"[*] {s} [OK]", delay=0.003, color=random.choice(PALETTE))

    progress_bar("Executing exploit", total=28, color=RED)
    time.sleep(0.6)

    # Show final scrolling message infinitely
    final_message_loop(cols)

if __name__ == "__main__":
    main()







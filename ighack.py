#!/usr/bin/env python3
"""
Termux-friendly IG HACK reel (visual mock only).

- Uses big, clean "normal" looking titles by converting text to fullwidth Unicode.
- Optional: `pip install instaloader` to fetch public profile stats.
- Final big green message will remain on-screen (blinking) until you press Ctrl+C.
"""

import os
import sys
import time
import random
import shutil
import re
from itertools import cycle

# Optional instaloader import (public info only)
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
BOLD   = "\033[1m"
RESET  = "\033[0m"
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

def center(text, width):
    plain = strip_ansi(text)
    pad = max((width - len(plain)) // 2, 0)
    return " " * pad + text

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

# ===== Fullwidth conversion to make "normal" text look big =====
# converts ASCII chars (33..126) to their fullwidth Unicode equivalents
def to_fullwidth(s):
    out = []
    for ch in s:
        code = ord(ch)
        if 33 <= code <= 126:
            out.append(chr(code + 0xFEE0))
        elif ch == " ":
            out.append("　")  # fullwidth space
        else:
            out.append(ch)
    return "".join(out)

# ===== Fake cracking helpers =====
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
    time.sleep(0.5)

def spinner(label, steps=20, delay=0.04, color=WHITE):
    sp = cycle("|/-\\")
    for _ in range(steps):
        sys.stdout.write("\r" + color + f"[*] {label:<36} {next(sp)}" + RESET)
        sys.stdout.flush()
        time.sleep(delay)
    sys.stdout.write("\r" + " " * 80 + "\r")
    sys.stdout.flush()

def progress_bar(task="Processing", total=30, color=RED):
    cols, _ = term_size()
    bar_w = max(min(cols - 30, 40), 20)
    for i in range(total+1):
        filled = int((i/total) * bar_w)
        bar = "#" * filled + "-" * (bar_w - filled)
        pct = int((i/total) * 100)
        sys.stdout.write(f"\r{color}{task:<12}: [{bar}] {pct:3d}%{RESET}")
        sys.stdout.flush()
        time.sleep(0.06)
    print()

# ===== Optional instaloader helpers (public data only) =====
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

# ===== Main flow =====
def main():
    clear()
    cols, rows = term_size()

    # Title text (big, normal-looking via fullwidth)
    title_text = "INSTA HACK"
    big_title = to_fullwidth(title_text)  # fullwidth "big" text
    title_line = BOLD + RED + big_title + RESET

    # subtitle small IG tag
    ig_tag = PINK + "[ instagram · visual mock ]" + RESET

    # print centered big title (maybe multiple lines for emphasis)
    print("\n")
    print(center(title_line, cols))
    # small gap and subtitle
    print(center(ig_tag, cols))
    print("\n")

    # prompt for username
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

    # show public info if possible
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

    # more fake steps
    for s in ["Extracting session cookies...", "Escalating privileges...", "Installing stealth module..."]:
        spinner(s, steps=12, delay=0.05, color=random.choice(COLORS))
        slow_print(f"[*] {s} [OK]", delay=0.003, color=random.choice(COLORS))

    progress_bar("Executing exploit", total=28, color=RED)
    time.sleep(0.6)

    # Final message — big and green (fullwidth), medium-sized
    final_text = "Valla Panikkum Poda..."
    big_final = to_fullwidth(final_text)
    final_line = GREEN + big_final + RESET

    # Print final centered and then keep it on-screen (blinking) until Ctrl+C
    print("\n" + center(final_line, cols) + "\n")
    print(center(WHITE + "(Press Ctrl+C to exit)" + RESET, cols))
    try:
        show = True
        while True:
            # blink: show/hide the big final line (keeps program running)
            if show:
                sys.stdout.write("\r" + center(final_line, cols))
            else:
                sys.stdout.write("\r" + " " * cols)
            sys.stdout.flush()
            show = not show
            time.sleep(0.8)
    except KeyboardInterrupt:
        # don't be noisy on exit; keep Ctrl+C behaviour natural
        print("\n" + RED + "Exiting..." + RESET)
        return

if __name__ == "__main__":
    main()

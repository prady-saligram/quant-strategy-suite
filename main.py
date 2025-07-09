#!/usr/bin/env python3
import os
import random
import time
import subprocess
from datetime import datetime, date
from tqdm import tqdm  # pip install tqdm

# ─── CONFIG ──────────────────────────────────────────────────────────────────

# Base mean interval (seconds)
BASE_MEAN_INTERVAL = 3600.0

# Clamp factor so we never wait beyond mean * MAX_MULTIPLIER
MAX_MULTIPLIER = 4

# Files to tweak
FILES = [
    "README.md",
    "src/qss/data/download.py",
    "src/qss/backtest/backtest.py",
    "src/qss/live/live.py",
]

# Commit message templates
MSG_TEMPLATES = [
    "docs: polish docs in {}",
    "refactor: tidy up {}",
    "fix: handle edge case in {}",
    "test: add minimal test for {}",
    "chore: formatting update in {}",
    "feat: sketch new helper in {}",
]

# ─── STATE ───────────────────────────────────────────────────────────────────

current_week = None
weekly_mean = BASE_MEAN_INTERVAL
current_day = None
daily_mean = BASE_MEAN_INTERVAL

# ─── HELPERS ─────────────────────────────────────────────────────────────────

def resample_weekly():
    """Resample a weekly mean interval around BASE_MEAN_INTERVAL."""
    return max(600, random.gauss(BASE_MEAN_INTERVAL, BASE_MEAN_INTERVAL * 0.2))

def resample_daily(weekly_mean):
    """Resample a daily mean interval around the weekly mean."""
    return max(300, random.gauss(weekly_mean, weekly_mean * 0.3))

def draw_delay(mean):
    """Draw from an exponential distribution, clamped to prevent huge waits."""
    delay = random.expovariate(1.0 / mean)
    return min(delay, mean * MAX_MULTIPLIER)

def countdown(delay):
    """Display a tqdm countdown for 'delay' seconds."""
    with tqdm(total=delay,
              desc="Next edit in",
              unit="s",
              dynamic_ncols=True,
              leave=False,
              mininterval=0.5) as pbar:
        start = time.time()
        while True:
            elapsed = time.time() - start
            to_advance = elapsed - pbar.n
            if to_advance > 0:
                pbar.update(to_advance)
            if elapsed >= delay:
                break
            time.sleep(0.3)

def tweak_file(path):
    """Append a subtle timestamp note to the chosen file."""
    timestamp = datetime.utcnow().strftime("%Y-%m-%d %H:%M UTC")
    if path.endswith(".md"):
        note = f"\n> Last touched: {timestamp}\n"
    else:
        note = f"\n# Touched at {timestamp}\n"
    with open(path, "a", encoding="utf-8") as f:
        f.write(note)

# ─── MAIN LOOP ───────────────────────────────────────────────────────────────

if __name__ == "__main__":
    # Ensure correct git identity
    subprocess.run(["git", "config", "user.name",  "Prady Saligram"], check=True)
    subprocess.run(["git", "config", "user.email", "saligram@stanford.edu"], check=True)

    # Change to script's directory
    os.chdir(os.path.dirname(__file__))

    while True:
        now = datetime.utcnow()
        week = now.isocalendar()[1]
        today = date.today()

        # If a new week, resample the weekly mean
        if week != current_week:
            weekly_mean = resample_weekly()
            current_week = week

        # If a new day, resample the daily mean based on weekly_mean
        if today != current_day:
            daily_mean = resample_daily(weekly_mean)
            current_day = today

        # Draw actual delay from exponential using today's mean
        delay = draw_delay(daily_mean)

        # Show countdown
        countdown(delay)

        # Perform a subtle tweak
        file_to_edit = random.choice(FILES)
        tweak_file(file_to_edit)

        # Stage, commit, push
        subprocess.run(["git", "add", file_to_edit], check=True)
        msg = random.choice(MSG_TEMPLATES).format(file_to_edit)
        msg += f" ({now.strftime('%a %H:%M')})"
        subprocess.run(["git", "commit", "-m", msg], check=True)
        subprocess.run(["git", "push", "origin", "main"], check=True)

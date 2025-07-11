#!/usr/bin/env python3
import os
import random
import time
import subprocess
import argparse
from datetime import datetime, date, timezone
from tqdm import tqdm  # pip install tqdm

# ─── CONFIG ──────────────────────────────────────────────────────────────────

# Parse command line arguments
parser = argparse.ArgumentParser(description='Automated git commits with configurable frequency')
parser.add_argument('--times-per-hour', '-t', type=float, default=1.0,
                   help='Number of commits per hour (default: 1.0)')
args = parser.parse_args()

# Calculate base mean interval based on times per hour
BASE_MEAN_INTERVAL = 3600.0 / args.times_per_hour  # Convert to seconds

# For very high frequencies, use a minimum delay to prevent issues
MIN_DELAY = 10  # Minimum 10 seconds between commits
if BASE_MEAN_INTERVAL < MIN_DELAY:
    BASE_MEAN_INTERVAL = MIN_DELAY
    print(f"Warning: Adjusted to minimum {MIN_DELAY}s delay for high frequency")

# Clamp factor so we never wait beyond mean * MAX_MULTIPLIER
MAX_MULTIPLIER = 4

# Files to tweak
FILES = [
    "README.md",
    "CONTRIBUTING.md", 
    "CHANGELOG.md",
    "docs/getting_started.md",
    "docs/advanced_usage.md",
    "src/qss/data/download.py",
    "src/qss/data/process.py",
    "src/qss/data/validate.py",
    "src/qss/backtest/backtest.py",
    "src/qss/backtest/metrics.py",
    "src/qss/backtest/plotting.py",
    "src/qss/live/live.py",
    "src/qss/live/monitor.py",
    "src/qss/live/alerts.py",
    "tests/test_data.py",
    "tests/test_backtest.py",
    "tests/test_live.py",
    "examples/basic_strategy.py",
    "examples/advanced_strategy.py",
]

# Commit message templates
MSG_TEMPLATES = [
    "docs: polish docs in {}",
    "docs: improve examples in {}",
    "docs: clarify usage in {}",
    "refactor: tidy up {}",
    "refactor: simplify logic in {}",
    "refactor: improve naming in {}",
    "fix: handle edge case in {}",
    "fix: resolve issue with {}",
    "fix: patch bug in {}",
    "test: add minimal test for {}",
    "test: expand coverage for {}",
    "test: add integration test in {}",
    "chore: formatting update in {}",
    "chore: clean up comments in {}",
    "chore: update dependencies in {}",
    "feat: sketch new helper in {}",
    "feat: implement new utility in {}",
    "feat: add support for new feature in {}",
    "perf: optimize performance in {}",
    "style: improve code style in {}"
]

# ─── STATE ───────────────────────────────────────────────────────────────────

current_week = None
weekly_mean = BASE_MEAN_INTERVAL
current_day = None
daily_mean = BASE_MEAN_INTERVAL

# ─── HELPERS ─────────────────────────────────────────────────────────────────

def resample_weekly():
    """Resample a weekly mean interval around BASE_MEAN_INTERVAL."""
    return max(MIN_DELAY, random.gauss(BASE_MEAN_INTERVAL, BASE_MEAN_INTERVAL * 0.2))

def resample_daily(weekly_mean):
    """Resample a daily mean interval around the weekly mean."""
    return max(MIN_DELAY, random.gauss(weekly_mean, weekly_mean * 0.3))

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

def ensure_file_exists(path):
    """Create the file and its directory structure if it doesn't exist."""
    import os
    # Create directory if it doesn't exist
    directory = os.path.dirname(path)
    if directory and not os.path.exists(directory):
        os.makedirs(directory, exist_ok=True)
    
    # Create file if it doesn't exist
    if not os.path.exists(path):
        # Create appropriate content based on file type
        if path.endswith('.py'):
            content = f'''# {os.path.basename(path)}
"""
{os.path.basename(path).replace('.py', '').replace('_', ' ').title()}
"""

def main():
    """Main function."""
    pass

if __name__ == "__main__":
    main()
'''
        elif path.endswith('.md'):
            content = f'''# {os.path.basename(path).replace('.md', '').replace('_', ' ').title()}

## Overview

This file contains documentation for {os.path.basename(path).replace('.md', '').replace('_', ' ').lower()}.

## Usage

Add usage instructions here.
'''
        else:
            content = f"# {os.path.basename(path)}\n\nContent for {path}\n"
        
        with open(path, "w", encoding="utf-8") as f:
            f.write(content)

def tweak_file(path):
    """Append a subtle timestamp note to the chosen file."""
    # Ensure the file exists
    ensure_file_exists(path)
    
    timestamp = datetime.now(timezone.utc).strftime("%Y-%m-%d %H:%M UTC")
    if path.endswith(".md"):
        note = f"\n> Last touched: {timestamp}\n"
    else:
        note = f"\n# Touched at {timestamp}\n"
    with open(path, "a", encoding="utf-8") as f:
        f.write(note)

def get_effective_delay():
    """Get the effective delay based on frequency and timing logic."""
    # For very high frequencies (more than 10 per hour), use direct timing
    if args.times_per_hour > 10:
        return max(MIN_DELAY, random.expovariate(1.0 / BASE_MEAN_INTERVAL))
    
    # For normal frequencies, use the weekly/daily resampling logic
    now = datetime.now(timezone.utc)
    week = now.isocalendar()[1]
    today = date.today()
    
    global current_week, weekly_mean, current_day, daily_mean
    
    # If a new week, resample the weekly mean
    if week != current_week:
        weekly_mean = resample_weekly()
        current_week = week

    # If a new day, resample the daily mean based on weekly_mean
    if today != current_day:
        daily_mean = resample_daily(weekly_mean)
        current_day = today

    # Draw actual delay from exponential using today's mean
    return draw_delay(daily_mean)

# ─── MAIN LOOP ───────────────────────────────────────────────────────────────

if __name__ == "__main__":
    print(f"Starting with {args.times_per_hour} commits per hour (mean interval: {BASE_MEAN_INTERVAL:.1f}s)")
    
    # Ensure correct git identity
    subprocess.run(["git", "config", "user.name",  "Prady Saligram"], check=True)
    subprocess.run(["git", "config", "user.email", "psaligram@stanford.edu"], check=True)

    # Change to script's directory
    os.chdir(os.path.dirname(__file__))

    while True:
        # Get the effective delay based on frequency settings
        delay = get_effective_delay()

        # Show countdown
        countdown(delay)

        # Perform a subtle tweak
        file_to_edit = random.choice(FILES)
        tweak_file(file_to_edit)

        # Stage, commit, push
        subprocess.run(["git", "add", file_to_edit], check=True)
        msg = random.choice(MSG_TEMPLATES).format(file_to_edit)
        subprocess.run(["git", "commit", "-m", msg], check=True)
        subprocess.run(["git", "push", "origin", "main"], check=True)
#!/usr/bin/env python3
import os
import random
import time
import subprocess
import argparse
from datetime import datetime, date, timezone
from tqdm import tqdm  # pip install tqdm

# ─── CONFIG ──────────────────────────────────────────────────────────────────

# Parse command line arguments
parser = argparse.ArgumentParser(description='Automated git commits with configurable frequency')
parser.add_argument('--times-per-hour', '-t', type=float, default=1.0,
                   help='Number of commits per hour (default: 1.0)')
args = parser.parse_args()

# Calculate base mean interval based on times per hour
BASE_MEAN_INTERVAL = 3600.0 / args.times_per_hour  # Convert to seconds

# Clamp factor so we never wait beyond mean * MAX_MULTIPLIER
MAX_MULTIPLIER = 4

# Files to tweak
FILES = [
    "README.md",
    "CONTRIBUTING.md", 
    "CHANGELOG.md",
    "docs/getting_started.md",
    "docs/advanced_usage.md",
    "src/qss/data/download.py",
    "src/qss/data/process.py",
    "src/qss/data/validate.py",
    "src/qss/backtest/backtest.py",
    "src/qss/backtest/metrics.py",
    "src/qss/backtest/plotting.py",
    "src/qss/live/live.py",
    "src/qss/live/monitor.py",
    "src/qss/live/alerts.py",
    "tests/test_data.py",
    "tests/test_backtest.py",
    "tests/test_live.py",
    "examples/basic_strategy.py",
    "examples/advanced_strategy.py",
]

# Commit message templates
MSG_TEMPLATES = [
    "docs: polish docs in {}",
    "docs: improve examples in {}",
    "docs: clarify usage in {}",
    "refactor: tidy up {}",
    "refactor: simplify logic in {}",
    "refactor: improve naming in {}",
    "fix: handle edge case in {}",
    "fix: resolve issue with {}",
    "fix: patch bug in {}",
    "test: add minimal test for {}",
    "test: expand coverage for {}",
    "test: add integration test in {}",
    "chore: formatting update in {}",
    "chore: clean up comments in {}",
    "chore: update dependencies in {}",
    "feat: sketch new helper in {}",
    "feat: implement new utility in {}",
    "feat: add support for new feature in {}",
    "perf: optimize performance in {}",
    "style: improve code style in {}"
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

def ensure_file_exists(path):
    """Create the file and its directory structure if it doesn't exist."""
    import os
    # Create directory if it doesn't exist
    directory = os.path.dirname(path)
    if directory and not os.path.exists(directory):
        os.makedirs(directory, exist_ok=True)
    
    # Create file if it doesn't exist
    if not os.path.exists(path):
        # Create appropriate content based on file type
        if path.endswith('.py'):
            content = f'''# {os.path.basename(path)}
"""
{os.path.basename(path).replace('.py', '').replace('_', ' ').title()}
"""

def main():
    """Main function."""
    pass

if __name__ == "__main__":
    main()
'''
        elif path.endswith('.md'):
            content = f'''# {os.path.basename(path).replace('.md', '').replace('_', ' ').title()}

## Overview

This file contains documentation for {os.path.basename(path).replace('.md', '').replace('_', ' ').lower()}.

## Usage

Add usage instructions here.
'''
        else:
            content = f"# {os.path.basename(path)}\n\nContent for {path}\n"
        
        with open(path, "w", encoding="utf-8") as f:
            f.write(content)

def tweak_file(path):
    """Append a subtle timestamp note to the chosen file."""
    # Ensure the file exists
    ensure_file_exists(path)
    
    timestamp = datetime.now(timezone.utc).strftime("%Y-%m-%d %H:%M UTC")
    if path.endswith(".md"):
        note = f"\n> Last touched: {timestamp}\n"
    else:
        note = f"\n# Touched at {timestamp}\n"
    with open(path, "a", encoding="utf-8") as f:
        f.write(note)

# ─── MAIN LOOP ───────────────────────────────────────────────────────────────

if __name__ == "__main__":
    print(f"Starting with {args.times_per_hour} commits per hour (mean interval: {BASE_MEAN_INTERVAL:.1f}s)")
    
    # Ensure correct git identity
    subprocess.run(["git", "config", "user.name",  "Prady Saligram"], check=True)
    subprocess.run(["git", "config", "user.email", "psaligram@stanford.edu"], check=True)

    # Change to script's directory
    os.chdir(os.path.dirname(__file__))

    while True:
        now = datetime.now(timezone.utc)
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
        subprocess.run(["git", "commit", "-m", msg], check=True)
        subprocess.run(["git", "push", "origin", "main"], check=True)

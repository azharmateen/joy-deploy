"""Terminal animations: ASCII art sequences for deploy progress, success, and failure."""

import sys
import time
import random
import shutil

from joy_deploy.messages import get_progress_message


def get_terminal_width() -> int:
    """Get terminal width, default to 80."""
    try:
        return shutil.get_terminal_size().columns
    except (ValueError, OSError):
        return 80


def animate_rocket_launch(duration: float = 2.0):
    """Animate a rocket launch sequence."""
    frames = [
        [
            "     |     ",
            "    / \\    ",
            "   / . \\   ",
            "  |  .  |  ",
            "  |     |  ",
            "  |     |  ",
            " /|     |\\ ",
            "/_|_____|_\\",
        ],
        [
            "     |     ",
            "    / \\    ",
            "   / . \\   ",
            "  |  .  |  ",
            "  |     |  ",
            "  |     |  ",
            " /|     |\\ ",
            "/_|_____|_\\",
            "    |||    ",
            "    |||    ",
        ],
        [
            "     |     ",
            "    / \\    ",
            "   / . \\   ",
            "  |  .  |  ",
            "  |     |  ",
            "  |     |  ",
            " /|     |\\ ",
            "/_|_____|_\\",
            "   |||||   ",
            "  |||||||  ",
            "   |||||   ",
        ],
        [
            "     |     ",
            "    / \\    ",
            "   / . \\   ",
            "  |  .  |  ",
            "  |     |  ",
            "  |     |  ",
            " /|     |\\ ",
            "/_|_____|_\\",
            "  |||||||  ",
            " ||||||||| ",
            "  |||||||  ",
            "   |||||   ",
        ],
    ]

    for frame in frames:
        _clear_lines(len(frame) + 1)
        for line in frame:
            sys.stdout.write(f"  {line}\n")
        sys.stdout.flush()
        time.sleep(duration / len(frames))


def animate_progress_bar(duration: float = 3.0, width: int = 40):
    """Animate a progress bar with personality."""
    steps = width
    msg = get_progress_message()

    sys.stdout.write(f"\n  {msg}\n\n")
    sys.stdout.flush()

    for i in range(steps + 1):
        pct = i / steps * 100
        filled = "#" * i
        empty = "-" * (steps - i)
        bar = f"  [{filled}{empty}] {pct:5.1f}%"
        sys.stdout.write(f"\r{bar}")
        sys.stdout.flush()

        # Variable speed for drama
        if pct < 20:
            time.sleep(duration / steps * 0.5)
        elif pct > 80 and pct < 95:
            time.sleep(duration / steps * 2.0)  # Slow down for suspense
        elif pct >= 95:
            time.sleep(duration / steps * 0.3)  # Quick finish
        else:
            time.sleep(duration / steps)

    sys.stdout.write("\n\n")
    sys.stdout.flush()


def animate_success():
    """Display success celebration with ASCII fireworks."""
    fireworks = r"""
     *  .  *    .   *   .  *
  .    *    .  *   .  *   .    *
    .   *  .    .  *    .   *
  *   .   *  .    *    .   *  .
    _____ _    _  _____ _____ ______ _____ _____
   / ____| |  | |/ ____/ ____|  ____/ ____/ ____|
  | (___ | |  | | |   | |    | |__ | (__ | (___
   \___ \| |  | | |   | |    |  __| \___ \ \___ \
   ____) | |__| | |___| |____| |____ ___) |___) |
  |_____/ \____/ \_____\_____|______|_____/_____/

     *  .  *    .   *   .  *
  .    *    .  *   .  *   .    *
"""
    sys.stdout.write(fireworks)
    sys.stdout.flush()


def animate_failure():
    """Display failure commiseration with sad robot."""
    sad_robot = r"""
       ___
      |   |
      |___|
     /|   |\
    /_| X |_\
      |___|
      /   \
     /     \
    /       \

    Deploy failed... but you've got this!
"""
    sys.stdout.write(sad_robot)
    sys.stdout.flush()


def animate_spinner(duration: float = 2.0, message: str = "Deploying"):
    """Show a spinning animation."""
    spinner_chars = ["|", "/", "-", "\\"]
    start = time.time()
    i = 0

    while time.time() - start < duration:
        char = spinner_chars[i % len(spinner_chars)]
        sys.stdout.write(f"\r  {char} {message}...")
        sys.stdout.flush()
        time.sleep(0.1)
        i += 1

    sys.stdout.write(f"\r  * {message}... done!\n")
    sys.stdout.flush()


def animate_dots(message: str = "Working", duration: float = 1.5):
    """Animate expanding dots."""
    for i in range(int(duration / 0.3)):
        dots = "." * ((i % 4) + 1)
        sys.stdout.write(f"\r  {message}{dots:<4}")
        sys.stdout.flush()
        time.sleep(0.3)
    sys.stdout.write("\n")
    sys.stdout.flush()


def animate_matrix_rain(duration: float = 1.5, width: int = None):
    """Brief matrix-style rain effect."""
    if width is None:
        width = min(get_terminal_width(), 60)

    chars = "01"
    lines = 8
    frame_data = [[" "] * width for _ in range(lines)]
    drops = [random.randint(0, lines - 1) for _ in range(width)]

    start = time.time()
    while time.time() - start < duration:
        for col in range(width):
            row = drops[col]
            if row < lines:
                frame_data[row][col] = random.choice(chars)
                drops[col] += 1
                if drops[col] >= lines:
                    drops[col] = 0

            # Fade
            for r in range(lines):
                if r != row and frame_data[r][col] != " ":
                    if random.random() > 0.7:
                        frame_data[r][col] = " "

        # Print frame
        _clear_lines(lines)
        for row_data in frame_data:
            sys.stdout.write("  " + "".join(row_data) + "\n")
        sys.stdout.flush()
        time.sleep(0.08)


def animate_countdown(seconds: int = 3):
    """Countdown before deploy."""
    for i in range(seconds, 0, -1):
        sys.stdout.write(f"\r  Launching in {i}...")
        sys.stdout.flush()
        time.sleep(1)
    sys.stdout.write(f"\r  LIFTOFF!          \n")
    sys.stdout.flush()


def _clear_lines(count: int):
    """Clear N lines above cursor."""
    for _ in range(count):
        sys.stdout.write("\033[A\033[2K")

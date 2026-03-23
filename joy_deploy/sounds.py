"""Terminal bell integration: victory bell on success, alert on failure."""

import sys


def play_success_sound():
    """Play a success sound using terminal bell."""
    # Triple bell for celebration
    sys.stdout.write("\a")
    sys.stdout.flush()


def play_failure_sound():
    """Play a failure sound using terminal bell."""
    # Single bell for alert
    sys.stdout.write("\a")
    sys.stdout.flush()


def bell(count: int = 1):
    """Ring the terminal bell N times."""
    for _ in range(count):
        sys.stdout.write("\a")
    sys.stdout.flush()

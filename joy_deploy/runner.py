"""Command runner: wraps deploy commands, captures output, tracks timing."""

import os
import subprocess
import sys
import time
from datetime import datetime
from dataclasses import dataclass
from typing import Optional

from joy_deploy.animator import (
    animate_countdown, animate_progress_bar, animate_rocket_launch,
    animate_success, animate_failure, animate_spinner, animate_matrix_rain,
)
from joy_deploy.messages import get_success_message, get_failure_message, get_progress_message
from joy_deploy.sounds import play_success_sound, play_failure_sound
from joy_deploy.history import record_deploy


@dataclass
class DeployResult:
    """Result of a deployment."""
    command: str
    success: bool
    exit_code: int
    stdout: str
    stderr: str
    duration_seconds: float
    started_at: str
    ended_at: str


def run_deploy(
    command: str,
    animate: bool = True,
    sound: bool = False,
    show_output: bool = True,
    quiet: bool = False,
) -> DeployResult:
    """Run a deploy command with animation and celebration.

    Args:
        command: The shell command to run
        animate: Show terminal animations
        sound: Play terminal bell sounds
        show_output: Show command stdout/stderr
        quiet: Minimal output mode
    """
    started_at = datetime.now()

    if not quiet:
        print()
        print("  " + "=" * 50)
        print(f"  JOY DEPLOY")
        print("  " + "=" * 50)
        print(f"  Command: {command}")
        print(f"  Started: {started_at.strftime('%Y-%m-%d %H:%M:%S')}")
        print()

    # Pre-deploy animation
    if animate and not quiet:
        animate_countdown(3)
        animate_matrix_rain(duration=1.0)

    # Progress message
    if not quiet:
        progress_msg = get_progress_message()
        print(f"  {progress_msg}")
        print()

    # Run the command
    start_time = time.time()

    try:
        process = subprocess.run(
            command,
            shell=True,
            capture_output=True,
            text=True,
            timeout=600,  # 10 minute timeout
        )
        exit_code = process.returncode
        stdout = process.stdout
        stderr = process.stderr
    except subprocess.TimeoutExpired:
        exit_code = -1
        stdout = ""
        stderr = "Command timed out after 10 minutes"
    except Exception as e:
        exit_code = -1
        stdout = ""
        stderr = str(e)

    duration = time.time() - start_time
    ended_at = datetime.now()
    success = exit_code == 0

    # Show command output
    if show_output and not quiet:
        if stdout.strip():
            print("  --- stdout ---")
            for line in stdout.strip().split("\n"):
                print(f"  {line}")
            print()
        if stderr.strip() and not success:
            print("  --- stderr ---")
            for line in stderr.strip().split("\n"):
                print(f"  {line}")
            print()

    # Post-deploy celebration or commiseration
    if success:
        if animate and not quiet:
            animate_success()

        msg = get_success_message()
        if not quiet:
            print(f"\n  {msg}")
            print(f"  Duration: {_format_duration(duration)}")

        if sound:
            play_success_sound()
    else:
        if animate and not quiet:
            animate_failure()

        msg = get_failure_message()
        if not quiet:
            print(f"\n  {msg}")
            print(f"  Exit code: {exit_code}")
            print(f"  Duration: {_format_duration(duration)}")

        if sound:
            play_failure_sound()

    if not quiet:
        print()

    # Record to history
    result = DeployResult(
        command=command,
        success=success,
        exit_code=exit_code,
        stdout=stdout,
        stderr=stderr,
        duration_seconds=duration,
        started_at=started_at.isoformat(),
        ended_at=ended_at.isoformat(),
    )

    record_deploy(result)

    return result


def _format_duration(seconds: float) -> str:
    """Format duration for display."""
    if seconds < 1:
        return f"{seconds*1000:.0f}ms"
    elif seconds < 60:
        return f"{seconds:.1f}s"
    elif seconds < 3600:
        mins = int(seconds // 60)
        secs = seconds % 60
        return f"{mins}m {secs:.0f}s"
    else:
        hours = int(seconds // 3600)
        mins = int((seconds % 3600) // 60)
        return f"{hours}h {mins}m"

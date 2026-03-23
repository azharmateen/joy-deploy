"""Deploy history: track all deployments with metadata."""

import json
import os
import sqlite3
from datetime import datetime
from pathlib import Path
from typing import Optional


DB_DIR = os.path.join(str(Path.home()), ".joy-deploy")
DB_PATH = os.path.join(DB_DIR, "history.db")


def get_db() -> sqlite3.Connection:
    """Get database connection, creating schema if needed."""
    os.makedirs(DB_DIR, exist_ok=True)
    conn = sqlite3.connect(DB_PATH)
    conn.row_factory = sqlite3.Row
    conn.execute("PRAGMA journal_mode=WAL")
    _create_tables(conn)
    return conn


def _create_tables(conn: sqlite3.Connection):
    """Create tables if they don't exist."""
    conn.executescript("""
        CREATE TABLE IF NOT EXISTS deploys (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            command TEXT NOT NULL,
            success INTEGER NOT NULL,
            exit_code INTEGER DEFAULT 0,
            duration_seconds REAL DEFAULT 0.0,
            started_at TEXT NOT NULL,
            ended_at TEXT,
            cwd TEXT DEFAULT '',
            stdout_preview TEXT DEFAULT '',
            stderr_preview TEXT DEFAULT ''
        );
    """)
    conn.commit()


def record_deploy(result) -> int:
    """Record a deployment result."""
    conn = get_db()
    cursor = conn.execute(
        """INSERT INTO deploys
           (command, success, exit_code, duration_seconds, started_at, ended_at, cwd, stdout_preview, stderr_preview)
           VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?)""",
        (
            result.command,
            1 if result.success else 0,
            result.exit_code,
            result.duration_seconds,
            result.started_at,
            result.ended_at,
            os.getcwd(),
            result.stdout[:500] if result.stdout else "",
            result.stderr[:500] if result.stderr else "",
        )
    )
    conn.commit()
    deploy_id = cursor.lastrowid
    conn.close()
    return deploy_id


def get_history(limit: int = 20) -> list:
    """Get recent deploy history."""
    conn = get_db()
    rows = conn.execute(
        "SELECT * FROM deploys ORDER BY started_at DESC LIMIT ?", (limit,)
    ).fetchall()
    conn.close()
    return [dict(r) for r in rows]


def get_deploy(deploy_id: int) -> Optional[dict]:
    """Get a specific deploy by ID."""
    conn = get_db()
    row = conn.execute("SELECT * FROM deploys WHERE id = ?", (deploy_id,)).fetchone()
    conn.close()
    return dict(row) if row else None


def get_streak() -> dict:
    """Get current deploy success streak."""
    conn = get_db()
    rows = conn.execute(
        "SELECT success FROM deploys ORDER BY started_at DESC LIMIT 100"
    ).fetchall()
    conn.close()

    if not rows:
        return {"current_streak": 0, "streak_type": "none", "total": 0}

    # Count consecutive successes from most recent
    current_streak = 0
    streak_type = "success" if rows[0]["success"] else "failure"

    for row in rows:
        is_success = bool(row["success"])
        if (streak_type == "success" and is_success) or (streak_type == "failure" and not is_success):
            current_streak += 1
        else:
            break

    return {
        "current_streak": current_streak,
        "streak_type": streak_type,
        "total": len(rows),
    }


def get_today_count() -> dict:
    """Get today's deploy counts."""
    conn = get_db()
    today = datetime.now().strftime("%Y-%m-%d")
    rows = conn.execute(
        "SELECT success, COUNT(*) as cnt FROM deploys WHERE started_at LIKE ? GROUP BY success",
        (f"{today}%",)
    ).fetchall()
    conn.close()

    result = {"total": 0, "success": 0, "failure": 0}
    for r in rows:
        if r["success"]:
            result["success"] = r["cnt"]
        else:
            result["failure"] = r["cnt"]
        result["total"] += r["cnt"]
    return result


def format_history(deploys: list) -> str:
    """Format deploy history for terminal output."""
    if not deploys:
        return "  No deployments recorded yet."

    lines = []
    lines.append(f"  {'ID':<5} {'Status':<8} {'Duration':>10} {'Command':<35} {'When'}")
    lines.append("  " + "-" * 78)

    for d in deploys:
        status = "OK" if d["success"] else "FAIL"
        duration = _fmt_dur(d["duration_seconds"])
        cmd = d["command"][:33]
        when = d["started_at"][:16] if d["started_at"] else "?"
        lines.append(f"  {d['id']:<5} {status:<8} {duration:>10} {cmd:<35} {when}")

    return "\n".join(lines)


def _fmt_dur(seconds: float) -> str:
    """Format duration."""
    if seconds < 1:
        return f"{seconds*1000:.0f}ms"
    elif seconds < 60:
        return f"{seconds:.1f}s"
    else:
        mins = int(seconds // 60)
        secs = seconds % 60
        return f"{mins}m {secs:.0f}s"

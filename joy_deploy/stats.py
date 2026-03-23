"""Stats: total deploys, success rate, average duration, fastest deploy, streaks, heatmap."""

from collections import Counter, defaultdict
from datetime import datetime

from joy_deploy.history import get_db


def get_full_stats() -> dict:
    """Get comprehensive deployment statistics."""
    conn = get_db()

    # Total counts
    total_row = conn.execute("SELECT COUNT(*) as total FROM deploys").fetchone()
    total = total_row["total"] if total_row else 0

    if total == 0:
        conn.close()
        return {
            "total_deploys": 0,
            "success_count": 0,
            "failure_count": 0,
            "success_rate": 0.0,
            "avg_duration": 0.0,
            "fastest_deploy": None,
            "slowest_deploy": None,
            "total_time": 0.0,
            "today_count": 0,
            "this_week": 0,
            "this_month": 0,
            "current_streak": 0,
            "best_streak": 0,
            "deploys_by_hour": {},
            "deploys_by_weekday": {},
            "top_commands": [],
        }

    # Success/failure counts
    success_row = conn.execute("SELECT COUNT(*) as cnt FROM deploys WHERE success = 1").fetchone()
    success_count = success_row["cnt"] if success_row else 0
    failure_count = total - success_count

    # Durations
    dur_row = conn.execute(
        "SELECT AVG(duration_seconds) as avg_dur, MIN(duration_seconds) as min_dur, "
        "MAX(duration_seconds) as max_dur, SUM(duration_seconds) as total_dur FROM deploys"
    ).fetchone()

    # Fastest deploy
    fastest = conn.execute(
        "SELECT * FROM deploys WHERE success = 1 ORDER BY duration_seconds ASC LIMIT 1"
    ).fetchone()

    # Slowest deploy
    slowest = conn.execute(
        "SELECT * FROM deploys WHERE success = 1 ORDER BY duration_seconds DESC LIMIT 1"
    ).fetchone()

    # Time-based counts
    now = datetime.now()
    today = now.strftime("%Y-%m-%d")
    today_row = conn.execute(
        "SELECT COUNT(*) as cnt FROM deploys WHERE started_at LIKE ?", (f"{today}%",)
    ).fetchone()

    # This week (last 7 days)
    week_row = conn.execute(
        "SELECT COUNT(*) as cnt FROM deploys WHERE started_at >= date('now', '-7 days')"
    ).fetchone()

    # This month
    month = now.strftime("%Y-%m")
    month_row = conn.execute(
        "SELECT COUNT(*) as cnt FROM deploys WHERE started_at LIKE ?", (f"{month}%",)
    ).fetchone()

    # Deploys by hour
    all_deploys = conn.execute("SELECT started_at, success FROM deploys").fetchall()
    hour_counts = Counter()
    weekday_counts = Counter()
    weekday_names = ["Monday", "Tuesday", "Wednesday", "Thursday", "Friday", "Saturday", "Sunday"]

    for d in all_deploys:
        try:
            dt = datetime.fromisoformat(d["started_at"])
            hour_counts[dt.hour] += 1
            weekday_counts[weekday_names[dt.weekday()]] += 1
        except (ValueError, TypeError):
            pass

    # Top commands
    cmd_counts = conn.execute(
        "SELECT command, COUNT(*) as cnt, SUM(success) as wins FROM deploys GROUP BY command ORDER BY cnt DESC LIMIT 10"
    ).fetchall()

    # Streak calculation
    rows = conn.execute("SELECT success FROM deploys ORDER BY started_at DESC").fetchall()
    current_streak = 0
    best_streak = 0
    temp_streak = 0

    for r in rows:
        if r["success"]:
            if current_streak == temp_streak:
                current_streak += 1
            temp_streak += 1
            best_streak = max(best_streak, temp_streak)
        else:
            if temp_streak == current_streak:
                pass  # Current streak is broken at some point
            temp_streak = 0

    # Recalculate current streak properly
    current_streak = 0
    for r in rows:
        if r["success"]:
            current_streak += 1
        else:
            break

    # Best success streak
    best_streak = 0
    temp = 0
    for r in conn.execute("SELECT success FROM deploys ORDER BY started_at ASC").fetchall():
        if r["success"]:
            temp += 1
            best_streak = max(best_streak, temp)
        else:
            temp = 0

    conn.close()

    return {
        "total_deploys": total,
        "success_count": success_count,
        "failure_count": failure_count,
        "success_rate": (success_count / total * 100) if total > 0 else 0.0,
        "avg_duration": dur_row["avg_dur"] or 0.0,
        "fastest_deploy": dict(fastest) if fastest else None,
        "slowest_deploy": dict(slowest) if slowest else None,
        "total_time": dur_row["total_dur"] or 0.0,
        "today_count": today_row["cnt"] if today_row else 0,
        "this_week": week_row["cnt"] if week_row else 0,
        "this_month": month_row["cnt"] if month_row else 0,
        "current_streak": current_streak,
        "best_streak": best_streak,
        "deploys_by_hour": {h: hour_counts.get(h, 0) for h in range(24)},
        "deploys_by_weekday": {d: weekday_counts.get(d, 0) for d in weekday_names},
        "top_commands": [
            {"command": dict(c)["command"][:40], "count": dict(c)["cnt"], "success": dict(c)["wins"]}
            for c in cmd_counts
        ],
    }


def format_stats(stats: dict) -> str:
    """Format stats for terminal output."""
    lines = []
    lines.append("=" * 55)
    lines.append("  JOY DEPLOY STATS")
    lines.append("=" * 55)

    lines.append(f"\n  Total Deploys:   {stats['total_deploys']}")
    lines.append(f"  Successful:      {stats['success_count']}")
    lines.append(f"  Failed:          {stats['failure_count']}")
    lines.append(f"  Success Rate:    {stats['success_rate']:.1f}%")

    lines.append(f"\n  Avg Duration:    {_fmt(stats['avg_duration'])}")
    if stats["fastest_deploy"]:
        lines.append(f"  Fastest Deploy:  {_fmt(stats['fastest_deploy']['duration_seconds'])}")
    if stats["slowest_deploy"]:
        lines.append(f"  Slowest Deploy:  {_fmt(stats['slowest_deploy']['duration_seconds'])}")
    lines.append(f"  Total Time:      {_fmt(stats['total_time'])}")

    lines.append(f"\n  Today:           {stats['today_count']} deploys")
    lines.append(f"  This Week:       {stats['this_week']} deploys")
    lines.append(f"  This Month:      {stats['this_month']} deploys")

    lines.append(f"\n  Current Streak:  {stats['current_streak']} successful deploys")
    lines.append(f"  Best Streak:     {stats['best_streak']} successful deploys")

    # Deploy heatmap by hour
    if any(v > 0 for v in stats["deploys_by_hour"].values()):
        lines.append(f"\n  Deploys by Hour:")
        max_val = max(stats["deploys_by_hour"].values())
        for h in range(24):
            count = stats["deploys_by_hour"].get(h, 0)
            bar_len = int(count / max(max_val, 1) * 20) if count > 0 else 0
            bar = "#" * bar_len
            lines.append(f"    {h:2d}:00 {bar:<20} {count}")

    # Top commands
    if stats["top_commands"]:
        lines.append(f"\n  Top Commands:")
        for cmd in stats["top_commands"][:5]:
            rate = (cmd["success"] / cmd["count"] * 100) if cmd["count"] > 0 else 0
            lines.append(f"    {cmd['command']:<38} {cmd['count']}x ({rate:.0f}% ok)")

    lines.append("\n" + "=" * 55)
    return "\n".join(lines)


def _fmt(seconds: float) -> str:
    """Format duration."""
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

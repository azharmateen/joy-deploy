"""Joy Deploy CLI - Make deployments delightful."""

import json
import click

from joy_deploy.runner import run_deploy
from joy_deploy.history import get_history, format_history, get_streak, get_today_count
from joy_deploy.stats import get_full_stats, format_stats


@click.group()
@click.version_option(version="1.0.0", prog_name="joy-deploy")
def cli():
    """Joy Deploy - Make deployments delightful.

    Wrap any deploy command with animations, celebrations, and tracking.
    """
    pass


@cli.command()
@click.argument("command", nargs=-1, required=True)
@click.option("--no-animate", is_flag=True, help="Disable animations")
@click.option("--sound", "-s", is_flag=True, help="Enable terminal bell sounds")
@click.option("--quiet", "-q", is_flag=True, help="Minimal output")
@click.option("--no-output", is_flag=True, help="Hide command stdout/stderr")
def run(command, no_animate, sound, quiet, no_output):
    """Run a deploy command with joy!

    Examples:
        joy-deploy run git push origin main
        joy-deploy run npm run deploy
        joy-deploy run ./deploy.sh
        joy-deploy run "docker push myapp:latest"
    """
    cmd_str = " ".join(command)

    result = run_deploy(
        command=cmd_str,
        animate=not no_animate,
        sound=sound,
        show_output=not no_output,
        quiet=quiet,
    )

    # Exit with the same code as the wrapped command
    raise SystemExit(result.exit_code)


@cli.command()
@click.option("--sound", "-s", is_flag=True, default=False, help="Enable terminal bell (default: off)")
@click.option("--no-animate", is_flag=True, default=False, help="Disable animations")
def config(sound, no_animate):
    """Show current configuration."""
    click.echo()
    click.echo("  Joy Deploy Configuration")
    click.echo("  " + "-" * 30)
    click.echo(f"  Animations: {'disabled' if no_animate else 'enabled'}")
    click.echo(f"  Sound: {'enabled' if sound else 'disabled'}")
    click.echo()
    click.echo("  Tip: Use flags with 'run' command:")
    click.echo("    joy-deploy run --sound --no-animate <command>")
    click.echo()


@cli.command()
@click.option("--limit", "-n", default=20, help="Number of entries to show")
def history(limit):
    """Show deployment history."""
    deploys = get_history(limit)

    click.echo()
    click.echo("=" * 55)
    click.echo("  DEPLOY HISTORY")
    click.echo("=" * 55)
    click.echo()

    if not deploys:
        click.echo("  No deployments recorded yet.")
        click.echo("  Run: joy-deploy run <your-deploy-command>")
    else:
        click.echo(format_history(deploys))

        # Streak and today info
        streak = get_streak()
        today = get_today_count()

        click.echo()
        if streak["current_streak"] > 0:
            icon = ">>>" if streak["streak_type"] == "success" else "!!!"
            click.echo(f"  {icon} Current streak: {streak['current_streak']} {streak['streak_type']}(es) in a row")
        if today["total"] > 0:
            click.echo(f"  Today: {today['total']} deploys ({today['success']} ok, {today['failure']} failed)")

    click.echo()


@cli.command()
def stats():
    """Show deployment statistics."""
    full_stats = get_full_stats()
    click.echo(format_stats(full_stats))


@cli.command()
def celebrate():
    """Test the celebration animation!"""
    from joy_deploy.animator import animate_countdown, animate_success, animate_matrix_rain
    from joy_deploy.messages import get_success_message

    click.echo()
    animate_countdown(3)
    animate_matrix_rain(duration=1.0)
    animate_success()
    click.echo(f"\n  {get_success_message()}")
    click.echo()


@cli.command()
def commiserate():
    """Test the failure animation."""
    from joy_deploy.animator import animate_failure
    from joy_deploy.messages import get_failure_message

    click.echo()
    animate_failure()
    click.echo(f"\n  {get_failure_message()}")
    click.echo()


if __name__ == "__main__":
    cli()

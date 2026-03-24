# Joy Deploy

[![Built with Claude Code](https://img.shields.io/badge/Built%20with-Claude%20Code-blue?logo=anthropic&logoColor=white)](https://claude.ai/code)


> Make deployments delightful with animations, celebrations, and tracking.

[![License: MIT](https://img.shields.io/badge/License-MIT-green.svg)](LICENSE)
[![Python 3.9+](https://img.shields.io/badge/python-3.9+-blue.svg)](https://www.python.org/downloads/)

**Deploying should feel like an event.** Joy Deploy wraps your deploy commands with countdown animations, ASCII fireworks on success, encouraging messages on failure, and tracks your deployment history with stats.

## Features

- **Rocket countdown** animation before every deploy
- **Matrix rain** effect during deployment
- **ASCII fireworks** on success with 50+ celebration messages
- **Sad robot** on failure with 30+ encouraging messages
- **Deploy history** with SQLite tracking
- **Statistics** - success rate, streaks, fastest deploy, deploy heatmap
- **Terminal bell** integration (optional)
- **Exit code passthrough** - works in CI/CD pipelines

## Install

```bash
pip install joy-deploy
```

## Usage

```bash
# Wrap any deploy command
joy-deploy run git push origin main
joy-deploy run npm run deploy
joy-deploy run ./deploy.sh
joy-deploy run "docker push myapp:latest"
joy-deploy run "kubectl apply -f deployment.yaml"

# With sound
joy-deploy run --sound git push heroku main

# Quiet mode (minimal output, still tracks)
joy-deploy run --quiet npm run build

# Disable animations (for CI)
joy-deploy run --no-animate ./deploy.sh

# View history
joy-deploy history

# View statistics
joy-deploy stats

# Test celebrations
joy-deploy celebrate
joy-deploy commiserate
```

## Sample Messages

**Success:**
- "Your code just high-fived the server!"
- "Deploy complete! The containers are throwing a party."
- "Shipped faster than a caffeinated squirrel!"

**Failure:**
- "Even rockets crash sometimes. Try again!"
- "The server said no. But persistence beats resistance."
- "Deploy failed. Time to practice rubber duck debugging."

## Stats Dashboard

```
  JOY DEPLOY STATS
  =============================================
  Total Deploys:   142
  Success Rate:    94.4%
  Avg Duration:    12.3s
  Fastest Deploy:  2.1s
  Current Streak:  8 successful deploys
  Best Streak:     23 successful deploys
```

## CI/CD Compatible

Joy Deploy passes through the exit code of your command, so it works seamlessly in CI/CD pipelines. Use `--no-animate --quiet` for clean CI output.

```yaml
# GitHub Actions example
- run: pip install joy-deploy
- run: joy-deploy run --no-animate ./deploy.sh
```

## License

MIT

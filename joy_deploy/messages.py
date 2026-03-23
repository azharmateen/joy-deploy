"""Message database: success, failure, and progress messages."""

import random

SUCCESS_MESSAGES = [
    "Your code just high-fived the server!",
    "Deploy complete! The bits are partying in production.",
    "Ship it! Another masterpiece goes live.",
    "Deployed faster than a caffeinated squirrel!",
    "Production is looking gorgeous today.",
    "The servers are doing a happy dance!",
    "Code delivered. Mission accomplished.",
    "Another successful deploy! You're on fire!",
    "Your code has landed safely in production.",
    "Deploy complete! Pop the champagne!",
    "The cloud just got a little brighter.",
    "Smooth as butter. Perfect deploy.",
    "Your code is now living its best life in production.",
    "Deploy successful! High five yourself.",
    "The deployment gods smile upon you today.",
    "Shipped! Your code is now serving millions... or at least your mom.",
    "Deploy complete! Time for a victory lap.",
    "Your code just teleported to production. Science!",
    "Another day, another flawless deploy.",
    "The server accepted your offering. Deploy complete!",
    "Your code has achieved production enlightenment.",
    "Deploy done! That was smoother than a jazz saxophone solo.",
    "Code deployed. Microservices are micro-celebrating.",
    "Your bits are now living their best life on the server.",
    "Deployment successful! The CI/CD pipeline salutes you.",
    "Ship ship hooray! Deploy complete.",
    "Your code just graduated to production!",
    "Deploy done! The containers are throwing a party.",
    "Successfully deployed. Your future self thanks you.",
    "The deployment train has arrived at Production Station!",
    "Code shipped! Kubernetes is doing cartwheels.",
    "Deploy complete! Even the load balancer is impressed.",
    "Your code is now in production, vibing with the servers.",
    "Flawless deploy! You should put this on your resume.",
    "The pipeline has spoken: DEPLOY COMPLETE!",
    "Another beautiful deploy. You make it look easy.",
    "Your code is live! The internet just got a little better.",
    "Deploy done! The servers are giving you a standing ovation.",
    "Shipped and delivered! Better than same-day Amazon.",
    "Deploy complete! The cloud infrastructure applauds.",
    "Your deployment was smoother than a fresh git rebase.",
    "Code deployed! Even the firewall let it through without questions.",
    "The deploy succeeded! Time to update that uptime counter.",
    "Your masterpiece is live. The world is a better place.",
    "Deploy complete! No rollback needed. What sorcery is this?",
    "Nailed it! Your code stuck the landing in production.",
    "Deploy done! The monitoring dashboards are all green.",
    "Ship it and forget it! (Just kidding, always monitor.)",
    "Deploy successful! Your code is now part of the internet.",
    "The deployment completed faster than your standup meeting.",
]

FAILURE_MESSAGES = [
    "Even rockets crash sometimes. You'll get it next time!",
    "Deploy failed, but your spirit shouldn't.",
    "Oops. The server said 'nah'. Let's try again.",
    "Deploy didn't make it. But hey, that's what rollback is for!",
    "The bits got lost somewhere. Time to debug!",
    "Houston, we have a problem. But we've solved worse.",
    "Deploy failed. Deep breath. Check the logs.",
    "The server rejected our love. It's not you, it's the code.",
    "Deployment stumbled. Even the best devs hit bumps.",
    "The deploy gremlins struck again. We'll get them next time.",
    "Failed deploy. But remember: every bug fixed makes you stronger.",
    "The server threw a tantrum. Let's calm it down.",
    "Deploy didn't stick the landing. Time for attempt #2.",
    "Oops! The deployment took an unexpected vacation.",
    "The pipeline had a hiccup. Nothing a good debug can't fix.",
    "Deploy failed. Plot twist! Time for the debugging montage.",
    "The server said no. But persistence beats resistance.",
    "Your deploy hit a speed bump. Time to smooth it out.",
    "Not today, deployment. But tomorrow is another day!",
    "The build broke, but your determination didn't.",
    "Deploy failed. The logs have secrets. Go find them.",
    "The containers staged a rebellion. Time to negotiate.",
    "Something went sideways. But that's how we learn!",
    "Deploy didn't work. Time to put on your detective hat.",
    "The server is being dramatic. Let's check what's wrong.",
    "Failed! But remember: 'git push --force' is always an option. (Just kidding.)",
    "The deploy took a wrong turn. Recalculating route...",
    "Something broke. But you know what they say: ship happens.",
    "Deploy failed. Time to practice your rubber duck debugging.",
    "The server ghosted us. But we won't give up!",
]

PROGRESS_MESSAGES = [
    "Deploying faster than you can say 'it works on my machine'...",
    "Sending your code to the cloud...",
    "Teaching servers new tricks...",
    "Uploading your masterpiece...",
    "The bits are marching to production...",
    "Convincing the server to cooperate...",
    "Deploying at the speed of light... almost...",
    "Your code is on its way to greatness...",
    "The pipeline is chugging along...",
    "Containers are warming up...",
    "DNS is propagating... (just kidding, this is fast)...",
    "Loading the code cannon...",
    "Preparing for liftoff...",
    "The deployment hamsters are running...",
    "Syncing with the cloud gods...",
    "Your code is stretching before the big race...",
    "Almost there, just dotting the i's and crossing the t's...",
    "The build elves are working overtime...",
    "Negotiating with the firewall...",
    "Your code is boarding the production express...",
]


def get_success_message() -> str:
    """Get a random success message."""
    return random.choice(SUCCESS_MESSAGES)


def get_failure_message() -> str:
    """Get a random failure message."""
    return random.choice(FAILURE_MESSAGES)


def get_progress_message() -> str:
    """Get a random progress message."""
    return random.choice(PROGRESS_MESSAGES)

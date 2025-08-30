import os
import subprocess

GITHUB_TOKEN = os.environ.get("GITHUB_TOKEN")
GITHUB_REPO = os.environ.get("GITHUB_REPO")
GITHUB_BRANCH = os.environ.get("GITHUB_BRANCH", "master")

def commit_seed_to_github():
    if not GITHUB_TOKEN or not GITHUB_REPO:
        print("Github Token missing, skipping commit")
        return
    
    subprocess.run(["git", "config", "--global", "user.email", "seed-bot@example.com"])
    subprocess.run(["git", "config", "--global", "user.name", "Seed Bot"])

    subprocess.run(["git", "add", "seed.json"])
    subprocess.run(["git", "commit", "-m", "Update seed.json auto"], check=False)

    repo_url = f"https://{GITHUB_TOKEN}@github.com/{GITHUB_REPO}.git"
    subprocess.run(["git", "push", repo_url, GITHUB_BRANCH])

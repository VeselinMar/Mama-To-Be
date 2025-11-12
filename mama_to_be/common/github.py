import os
import base64
import requests

GITHUB_TOKEN = os.environ.get("GITHUB_TOKEN")
GITHUB_REPO = os.environ.get("GITHUB_REPO")
GITHUB_BRANCH = os.environ.get("GITHUB_BRANCH", "main")
GITHUB_FILE_PATH = os.environ.get("GITHUB_FILE_PATH", "seed.json")

def commit_seed_to_github():
    """Push seed.json to GitHub using REST API"""
    if not GITHUB_TOKEN or not GITHUB_REPO:
        print("GitHub token or repo not set, skipping commit")
        return

    try:
        with open(GITHUB_FILE_PATH, "rb") as f:
            content = f.read()
        b64_content = base64.b64encode(content).decode("utf-8")

        url = f"https://api.github.com/repos/{GITHUB_REPO}/contents/{GITHUB_FILE_PATH}?ref={GITHUB_BRANCH}"
        headers = {"Authorization": f"token {GITHUB_TOKEN}"}

        resp = requests.get(url, headers=headers)

        if resp.status_code == 200:
            sha = resp.json()["sha"]
            data = {
                "message": "Update seed.json",
                "content": b64_content,
                "sha": sha,
                "branch": GITHUB_BRANCH,
            }
        elif resp.status_code == 404:
            data = {
                "message": "Add seed.json",
                "content": b64_content,
                "branch": GITHUB_BRANCH,
            }
        else:
            print(f"GitHub API error: {resp.status_code} {resp.text}")
            return

        put_resp = requests.put(url, headers=headers, json=data)
        if put_resp.status_code in [200, 201]:
            print("seed.json successfully pushed to GitHub")
        else:
            print(f"Failed to push seed.json: {put_resp.status_code} {put_resp.text}")

    except Exception as e:
        print(f"Error committing seed.json: {e}")

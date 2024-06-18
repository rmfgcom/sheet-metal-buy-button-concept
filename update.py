import os
import requests
import base64

rmfg_key = os.getenv("RMFG_KEY", "")
gh_token = os.getenv("GH_TOKEN", "")
repo_path = os.getenv("GITHUB_WORKSPACE", ".")
readme_path = os.path.join(repo_path, "README.md")
repo_owner = "reasonrobotics"
repo_name = "github-step-button"
branch = "main"


def get_file_content_from_github(filepath):
    url = f"https://api.github.com/repos/{repo_owner}/{repo_name}/contents/{filepath}?ref={branch}"
    headers = {
        "Authorization": f"token {gh_token}",
        "Accept": "application/vnd.github.v3.raw",
    }
    response = requests.get(url, headers=headers)
    response.raise_for_status()
    return base64.b64decode(response.json()["content"])


def get_purchase_link(file_content):
    files = {"file": ("mount.step", file_content)}

    designs_url = "https://api.rmfg.com/designs"
    design_upload_headers = {
        "accept": "application/json",
        "rmfg_key": rmfg_key,
    }
    upload_response = requests.post(
        designs_url, headers=design_upload_headers, files=files
    )
    return upload_response.json().get("purchase_link", "")


def update_readme():
    with open(readme_path, "r") as file:
        content = file.read()

    updated_content = content
    step_files = [f for f in os.listdir(repo_path) if f.endswith(".step")]

    for step_file in step_files:
        file_content = get_file_content_from_github(step_file)
        purchase_link = get_purchase_link(file_content)
        if purchase_link:  # Only add the button if the link is not empty
            button_markdown = f"[![Purchase](https://img.shields.io/badge/Purchase-STEP%20file-green)]({purchase_link})"
            updated_content += f"\n\n{step_file}\n\n{button_markdown}"

    with open(readme_path, "w") as file:
        file.write(updated_content)


if __name__ == "__main__":
    update_readme()

import os
import requests


rmfg_key = os.getenv("RMFG_KEY", "")
repo_path = os.getenv("GITHUB_WORKSPACE", ".")
readme_path = os.path.join(repo_path, "README.md")
github_token = os.getenv("GH_TOKEN", "")


def get_purchase_link(file_url):
    print(file_url)

    headers = {
        "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/58.0.3029.110 Safari/537.3",
        "Authorization": f"token {github_token}",
    }

    try:
        # Download the file content from the URL
        response = requests.get(file_url, headers=headers)
        response.raise_for_status()  # Ensure the request was successful
    except requests.exceptions.HTTPError as e:
        print(f"Failed to download {file_url}: {e}")
        return ""

    file_content = response.content
    files = {"file": ("mount.step", file_content)}

    designs_url = "https://api.rmfg.com/designs"
    design_upload_headers = {
        "accept": "application/json",
        "rmfg_key": rmfg_key,
    }
    upload_response = requests.post(
        designs_url, headers=design_upload_headers, files=files
    )
    response_json = upload_response.json()
    print(response_json)

    # Construct the purchase link using the 'id' from the response JSON
    if "id" in response_json:
        purchase_link = f"https://rmfg.com/quote/sheet/{response_json['id']}"
        return purchase_link

    return ""


def update_readme():
    with open(readme_path, "r") as file:
        content = file.read()

    updated_content = content
    step_files = [f for f in os.listdir(repo_path) if f.endswith(".step")]

    for step_file in step_files:
        file_url = f"https://{github_token}@raw.githubusercontent.com/reasonrobotics/github-step-button/main/{step_file}"
        purchase_link = get_purchase_link(file_url)
        if purchase_link:  # Only add the button if the link is not empty
            button_markdown = f"[![Purchase](https://img.shields.io/badge/Purchase-STEP%20file-green?logo=PHN2ZyB3aWR0aD0iMjM3IiBoZWlnaHQ9IjY0IiB2aWV3Qm94PSIwIDAgMjM3IDY0IiBmaWxsPSJub25lIiB4bWxucz0iaHR0cDovL3d3dy53My5vcmcvMjAwMC9zdmciPgo8cGF0aCBkPSJNMjYuMDQ1IDEuNjVDMzAuMjM4MyAxLjY1IDMzLjkyMTcgMi4zODY2NiAzNy4wOTUgMy44NkM0MC4zMjUgNS4yNzY2NiA0Mi44NDY3IDcuMzczMzMgNDQuNjYgMTAuMTVDNDYuNDczMyAxMi44NyA0Ny4zOCAxNi4xIDQ3LjM4IDE5Ljg0QzQ3LjM4IDIzLjQxIDQ2LjM4ODMgMjYuNDcgNDQuNDA1IDI5LjAyQzQyLjQ3ODMgMzEuNTEzMyAzOS45NTY3IDMzLjIxMzMgMzYuODQgMzQuMTJDMzkuOSAzNC41NzMzIDQyLjE2NjcgMzUuNjIxNyA0My42NCAzNy4yNjVDNDUuMTcgMzguOTA4MyA0Ni4wNzY3IDQxLjM0NSA0Ni4zNiA0NC41NzVMNDcuODkgNjJIMzYuNzU1TDM1LjQ4IDQ2LjE5QzM1LjI1MzMgNDMuNTgzMyAzNC4yOSA0MS43NyAzMi41OSA0MC43NUMzMC44OSAzOS43MyAyOC4xMTMzIDM5LjIyIDI0LjI2IDM5LjIySDExLjg1VjYySDAuOFYxLjY1SDI2LjA0NVpNMjQuODU1IDI5LjUzQzI4LjQyNSAyOS41MyAzMS4xNzMzIDI4Ljc2NSAzMy4xIDI3LjIzNUMzNS4wMjY3IDI1LjcwNSAzNS45OSAyMy40NjY3IDM1Ljk5IDIwLjUyQzM1Ljk5IDE3LjU3MzMgMzUuMDI2NyAxNS4zMDY3IDMzLjEgMTMuNzJDMzEuMTczMyAxMi4wNzY3IDI4LjQyNSAxMS4yNTUgMjQuODU1IDExLjI1NUgxMS44NVYyOS41M0gyNC44NTVaTTczLjExNjQgMS42NUw4OS43NzY0IDQ4LjRMMTA2LjM1MSAxLjY1SDEyMS4zMTFWNjJIMTEwLjI2MVYyMC41Mkw5NS4wNDY0IDYxLjkxNUg4NC41MDY0TDY5LjI5MTQgMjAuNTJWNjJINTguMjQxNFYxLjY1SDczLjExNjRaTTE3NS4zMTYgMS42NVYxMS4yNTVIMTQ1Ljk5MVYyNy43NDVIMTczLjc4NlYzNy4yNjVIMTQ1Ljk5MVY2MkgxMzQuOTQxVjEuNjVIMTc1LjMxNlpNMjI5LjU5OSA2MkwyMjguOTE5IDUyLjgyQzIyNy41NTkgNTUuOTkzMyAyMjUuMjA4IDU4LjU0MzMgMjIxLjg2NCA2MC40N0MyMTguNTc4IDYyLjM5NjcgMjE0Ljg2NiA2My4zNiAyMTAuNzI5IDYzLjM2QzIwNS4xMTkgNjMuMzYgMjAwLjE4OSA2MiAxOTUuOTM5IDU5LjI4QzE5MS42ODkgNTYuNTAzMyAxODguNDAzIDUyLjczNSAxODYuMDc5IDQ3Ljk3NUMxODMuODEzIDQzLjIxNSAxODIuNjc5IDM3Ljg2IDE4Mi42NzkgMzEuOTFDMTgyLjY3OSAyNS45NiAxODMuODQxIDIwLjU3NjcgMTg2LjE2NCAxNS43NkMxODguNDg4IDEwLjk0MzMgMTkxLjgwMyA3LjE3NSAxOTYuMTA5IDQuNDU1QzIwMC40MTYgMS42NzgzMyAyMDUuNDU5IDAuMjg5OTk5IDIxMS4yMzkgMC4yODk5OTlDMjE3Ljg2OSAwLjI4OTk5OSAyMjMuMzY2IDIuMTMxNjcgMjI3LjcyOSA1LjgxNUMyMzIuMTQ5IDkuNDk4MzMgMjM1LjAzOSAxNC41NyAyMzYuMzk5IDIxLjAzTDIyNC45MjQgMjEuNjI1QzIyNC4wMTggMTcuODg1IDIyMi4zNzQgMTQuOTk1IDIxOS45OTQgMTIuOTU1QzIxNy42NzEgMTAuOTE1IDIxNC42OTYgOS44OTUgMjExLjA2OSA5Ljg5NUMyMDUuNDU5IDkuODk1IDIwMS4yMzggMTEuOTM1IDE5OC40MDQgMTYuMDE1QzE5NS41NzEgMjAuMDk1IDE5NC4xNTQgMjUuMzkzMyAxOTQuMTU0IDMxLjkxQzE5NC4xNTQgMzguMzcgMTk1LjU3MSA0My42NCAxOTguNDA0IDQ3LjcyQzIwMS4yOTQgNTEuNzQzMyAyMDUuNTE2IDUzLjc1NSAyMTEuMDY5IDUzLjc1NUMyMTUuMjYzIDUzLjc1NSAyMTguNjA2IDUyLjQ4IDIyMS4wOTkgNDkuOTNDMjIzLjU5MyA0Ny4zMjMzIDIyNS4wOTQgNDMuODk1IDIyNS42MDQgMzkuNjQ1SDIxMC45ODRWMzAuODlIMjM2LjY1NFY2MkgyMjkuNTk5WiIgZmlsbD0id2hpdGUiLz4KPC9zdmc+Cg==)]({purchase_link})"
            updated_content += f"\n\n{step_file}\n\n{button_markdown}"

    with open(readme_path, "w") as file:
        file.write(updated_content)


if __name__ == "__main__":
    update_readme()

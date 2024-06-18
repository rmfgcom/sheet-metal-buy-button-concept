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
    designs_url = "https://api.rmfg.com/designs?public=true"
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

    # Define the marker for the RMFG section
    rmfg_marker = "<!-- RMFG -->"

    # Check if the marker exists in the content
    if rmfg_marker not in content:
        content += f"\n\n{rmfg_marker}\n"

    # Split the content at the marker
    before_marker, after_marker = content.split(rmfg_marker, 1)

    updated_content = before_marker + rmfg_marker
    step_files = [f for f in os.listdir(repo_path) if f.endswith(".step")]

    for step_file in step_files:
        file_url = f"https://{github_token}@raw.githubusercontent.com/reasonrobotics/github-step-button/main/{step_file}"
        purchase_link = get_purchase_link(file_url)
        if purchase_link:  # Only add the button if the link is not empty
            button_markdown = f'<a href="{purchase_link}"><img src="https://www.rmfg.com/have-it-made.svg" alt="Purchase" height="40px"></a>'
            step_file_marker = f"\n\n{step_file}\n\n"
            if step_file_marker in after_marker:
                # Replace the existing button
                before_step_file, after_step_file = after_marker.split(
                    step_file_marker, 1
                )
                after_marker = (
                    before_step_file
                    + step_file_marker
                    + button_markdown
                    + after_step_file.split("\n\n", 1)[1]
                )
            else:
                # Add a new button
                updated_content += f"\n\n{step_file}\n\n{button_markdown}"

    # Append the rest of the content after the marker
    updated_content += after_marker

    with open(readme_path, "w") as file:
        file.write(updated_content)


if __name__ == "__main__":
    update_readme()

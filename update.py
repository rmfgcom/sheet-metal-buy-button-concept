import os
import requests

repo_path = os.getenv("GITHUB_WORKSPACE", ".")
readme_path = os.path.join(repo_path, "README.md")


def get_purchase_link(file_url):
    print(file_url)
    # response = requests.post(
    #     "https://api.rmfg.com/design", json={"file_url": file_url}
    # )
    # return response.json().get("purchase_link")


def update_readme():
    with open(readme_path, "r") as file:
        content = file.read()

    updated_content = content
    step_files = [f for f in os.listdir(repo_path) if f.endswith(".step")]

    for step_file in step_files:
        # file_url = f"https://github.com/yourusername/yourrepo/raw/main/{step_file}"
        purchase_link = get_purchase_link(file_url)
        button_markdown = f"[![Purchase](https://img.shields.io/badge/Purchase-STEP%20file-green)]({purchase_link})"
        updated_content += f"\n\n{step_file}\n\n{button_markdown}"

    with open(readme_path, "w") as file:
        file.write(updated_content)


if __name__ == "__main__":
    update_readme()

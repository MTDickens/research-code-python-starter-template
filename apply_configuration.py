"""A file for initializing the repository.

This file should be deleted after initial setup.

Please do not run this file if you are user "MTDickens" and have just cloned the
repository for the sole purpose of contributing to the repository itself.

This file is only meant for users who have cloned the repository as a template for their
own work.
"""

import json
import re
import shutil
import subprocess
from pathlib import Path

REPO_ROOT = Path(__file__).resolve().parent


def _multi_replace(substitutions: dict[str, str], text: str) -> str:
    # Use re to replace everything in one pass, avoiding issues with the user's
    # new values getting matched to my old values.
    rep = dict((re.escape(k), v) for k, v in substitutions.items())
    pattern = re.compile("|".join(rep.keys()))
    return pattern.sub(lambda m: rep[re.escape(m.group(0))], text)


def _replace_all_occurences(
    substitutions: dict[str, str],
    repo_root: Path,
    exclude: set[Path] | None = None,
) -> None:
    if exclude is None:
        exclude = set()
    # Get files in this repository (e.g., exclude venv/).
    known_files: set[Path] = set()
    proc = subprocess.run(
        ["git", "ls-files"],
        cwd=repo_root,
        encoding="utf-8",
        stdout=subprocess.PIPE,
        check=True,
    )
    for line in proc.stdout.split("\n"):
        if line:
            known_files.add((repo_root / line).resolve())
    known_files -= exclude
    for file_path in known_files:
        if file_path.is_dir():
            continue
        with file_path.open("r", encoding="utf-8") as fp:
            file_contents = fp.read()
        updated_contents = _multi_replace(substitutions, file_contents)
        if updated_contents != file_contents:
            with file_path.open("w", encoding="utf-8") as file:
                file.write(updated_contents)


def _main() -> None:
    # Parse the config.
    repo_root = REPO_ROOT
    config_file = repo_root / "config.json"
    assert config_file.exists(), "Missing config file"
    with open(config_file, encoding="utf-8") as fp:
        config = json.load(fp)

    # Validate the config.
    assert "developer" in config, "Missing developer name in config file"
    developer = config["developer"]
    github_username = config["github-username"]
    assert " " not in github_username, "Malformed GitHub username"
    package_name = config["your-package-name"]
    assert " " not in package_name, "Package names cannot contain spaces (you want to `import package_name`)"
    assert "-" not in package_name, "Package names cannot dashes (you want to `import package_name`)"
    python_version = config["python-version"]
    assert python_version.startswith("3"), "Only Python 3 is supported"
    assert python_version.startswith("3."), "Missing dot in Python version (example: 3.10)"
    python_subversion = python_version.split(".")[1]
    assert python_subversion.isdigit()

    # Get the repository name from this directory.
    repo_name = repo_root.name

    # Delete the existing git files if they are from the starter repo.
    git_repo = repo_root / ".git"
    if git_repo.exists():
        git_config_file = git_repo / "config"
        with open(git_config_file, encoding="utf-8") as fp:
            git_config_contents = fp.read()
        if "git@github.com:MTDickens/research-code-python-starter-template" in git_config_contents:
            shutil.rmtree(git_repo)
        elif "https://github.com/MTDickens/research-code-python-starter-template" in git_config_contents:
            shutil.rmtree(git_repo)

    # Initialize the repo anew.
    subprocess.run(["git", "init"], cwd=repo_root, check=True, capture_output=True)
    # Rename branch to main if not already on it
    current_branch = subprocess.run(
        ["git", "symbolic-ref", "--short", "HEAD"],
        cwd=repo_root,
        check=True,
        capture_output=True,
        encoding="utf-8",
    ).stdout.strip()
    if current_branch != "main":
        subprocess.run(["git", "branch", "-M", "main"], cwd=repo_root, check=True, capture_output=True)
    subprocess.run(["git", "add", "."], cwd=repo_root, check=True, capture_output=True)

    # Check if the remote already exists (if this script is being run twice).
    # This can happen if the user makes a mistake in their GitHub username.
    ret = subprocess.run(
        ["git", "remote", "get-url", "origin"],
        cwd=repo_root,
        check=False,
        capture_output=True,
    )
    # Remote already exists, so set the URL.
    if ret.returncode == 0:
        remote_command = "set-url"
    # Remote doesn't exist, so add the URL.
    else:
        remote_command = "add"
    github_url = f"git@github.com:{github_username}/{repo_name}.git"
    subprocess.run(
        [
            "git",
            "remote",
            remote_command,
            "origin",
            github_url,
        ],
        cwd=repo_root,
        check=True,
        capture_output=True,
    )

    # Replace all occurrences of default names.
    substitutions = {
        "Tom Silver": developer,
        "tomsilver": github_username,
        "python-starter": repo_name,
        "python_starter": package_name,
        "3.10": f"3.{python_subversion}",
        "310": f"3{python_subversion}",
    }
    _replace_all_occurences(
        substitutions,
        repo_root=repo_root,
        exclude={
            repo_root / "apply_configuration.py",
            config_file,
            repo_root / "uv.lock",
        },
    )

    # Rename the package repo.
    (repo_root / "src" / "python_starter").rename(repo_root / "src" / package_name)

    # Report succcess.
    print("Configuration applied successfully.")


if __name__ == "__main__":
    _main()

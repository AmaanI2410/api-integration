import requests
import json
import os

CACHE_FILE = "cache.json"
BASE_URL = "https://api.github.com/users/octocat/repos"  # Replace 'octocat' with any GitHub username


def load_cache():
    if os.path.exists(CACHE_FILE):
        try:
            with open(CACHE_FILE, "r") as f:
                return json.load(f)
        except json.JSONDecodeError:
            return {}
    return {}


def save_cache(data):
    with open(CACHE_FILE, "w") as f:
        json.dump(data, f, indent=4)


def fetch_data():
    try:
        response = requests.get(BASE_URL, timeout=5)
        response.raise_for_status()
        return response.json()
    except requests.exceptions.Timeout:
        print("Error: Request timed out.")
    except requests.exceptions.ConnectionError:
        print("Error: Check your internet connection.")
    except requests.exceptions.HTTPError as e:
        print(f"HTTP Error: {e}")
    except ValueError:
        print("Error: Invalid JSON received.")
    return None


def initialize_cache():
    cache = load_cache()
    if "repos" not in cache:
        print("Fetching GitHub repositories...")
        repos = fetch_data()
        if repos:
            cache["repos"] = repos
            save_cache(cache)
    return cache


def list_repos(cache):
    repos = cache.get("repos", [])
    print("\nTotal repositories:", len(repos))
    print("1. List all repositories")
    print("2. Filter by language")

    choice = input("Enter option: ")

    if choice == "1":
        for repo in repos[:10]:
            print(f"{repo['id']}. {repo['name']}")
    elif choice == "2":
        lang = input("Enter programming language: ").capitalize()
        filtered = [r for r in repos if r["language"] == lang]
        print(f"\nFiltered repositories for language = {lang}")
        for repo in filtered:
            print(f"{repo['id']}. {repo['name']}")
    else:
        print("Invalid choice.")


def view_repo_by_id(cache):
    repo_id = input("Enter repository ID: ")
    repos = cache.get("repos", [])
    match = next((r for r in repos if str(r["id"]) == repo_id), None)
    if not match:
        print("Repository not found.")
        return
    print("\nRepository Details:")
    print(json.dumps(match, indent=4))


def main():
    cache = initialize_cache()

    while True:
        print("\n====== GitHub API Menu ======")
        print("1. List Repositories")
        print("2. View Repository By ID")
        print("3. Exit")

        choice = input("Enter choice: ")

        if choice == "1":
            list_repos(cache)
        elif choice == "2":
            view_repo_by_id(cache)
        elif choice == "3":
            print("Exiting...")
            break
        else:
            print("Invalid input.")


if __name__ == "__main__":
    main()

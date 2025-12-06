import requests
import json
import os

CACHE_FILE = "cache.json"
GITHUB_USER = "Zomato"  # Replace with any GitHub username
BASE_URL = f"https://api.github.com/users/{GITHUB_USER}/repos"


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
        response = requests.get(BASE_URL, timeout=10)
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
    total = min(100, len(repos))
    print(f"\nTotal Repositories: {len(repos)} (Showing first {total})\n")
    
    print("1. List all repositories")
    print("2. Filter by programming language")

    choice = input("Enter option: ")

    if choice == "1":
        for idx, repo in enumerate(repos[:total], start=1):
            print(f"{idx}. {repo['name']} ({repo['language']})")
    elif choice == "2":
        lang = input("Enter programming language: ").capitalize()
        filtered = [r for r in repos if r["language"] and r["language"].capitalize() == lang]
        print(f"\nFiltered Repositories for language = {lang}")
        for idx, repo in enumerate(filtered[:total], start=1):
            print(f"{idx}. {repo['name']} ({repo['language']})")
    else:
        print("Invalid choice.")


def view_repo_by_number(cache):
    repos = cache.get("repos", [])
    total = min(100, len(repos))
    repo_number = input(f"Enter repository number (1-{total}): ")
    
    if not repo_number.isdigit() or not (1 <= int(repo_number) <= total):
        print("Invalid repository number.")
        return
    
    selected_repo = repos[int(repo_number) - 1]
    print("\nRepository Details:")
    print(json.dumps(selected_repo, indent=4))


def main():
    cache = initialize_cache()

    while True:
        print("\n====== GitHub API Menu ======")
        print("1. List Repositories")
        print("2. View Repository By Number")
        print("3. Exit")

        choice = input("Enter choice: ")

        if choice == "1":
            list_repos(cache)
        elif choice == "2":
            view_repo_by_number(cache)
        elif choice == "3":
            print("Exiting...")
            break
        else:
            print("Invalid input.")


if __name__ == "__main__":
    main()

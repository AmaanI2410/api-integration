import requests
import json
import os

CACHE_FILE = "cache.json"
BASE_URL = "https://jsonplaceholder.typicode.com"


# Load cache
def load_cache():
    if os.path.exists(CACHE_FILE):
        try:
            with open(CACHE_FILE, "r") as f:
                return json.load(f)
        except json.JSONDecodeError:
            return {}
    return {}


# Save cache
def save_cache(data):
    with open(CACHE_FILE, "w") as f:
        json.dump(data, f, indent=4)


# API fetch with error handling
def fetch_data(endpoint):
    url = f"{BASE_URL}/{endpoint}"
    try:
        response = requests.get(url, timeout=5)
        response.raise_for_status()
        return response.json()

    except requests.exceptions.Timeout:
        print("❌ Error: Request timed out.")
    except requests.exceptions.ConnectionError:
        print("❌ Error: Check your internet connection.")
    except requests.exceptions.HTTPError as e:
        print(f"❌ HTTP Error: {e}")
    except ValueError:
        print("❌ Error: Invalid JSON received.")

    return None


# Initialize data and cache it
def initialize_cache():
    cache = load_cache()

    if "posts" not in cache:
        print("📥 Fetching posts...")
        posts = fetch_data("posts")
        if posts:
            cache["posts"] = posts

    if "users" not in cache:
        print("📥 Fetching users...")
        users = fetch_data("users")
        if users:
            cache["users"] = users

    save_cache(cache)
    return cache


# List posts + filter option
def list_posts(cache):
    posts = cache.get("posts", [])

    print("\n📌 Total Posts:", len(posts))
    print("1️⃣  List all posts")
    print("2️⃣  Filter by userId")

    choice = input("➡️  Enter option: ")

    if choice == "1":
        for p in posts[:10]:
            print(f"{p['id']}. {p['title']}")

    elif choice == "2":
        user_id = input("Enter userId: ")
        filtered = [p for p in posts if str(p["userId"]) == user_id]

        print(f"\n🎯 Filtered Results for userId={user_id}")
        for p in filtered:
            print(f"{p['id']}. {p['title']}")

    else:
        print("❌ Invalid choice.")


# Show full post by ID
def view_post_by_id(cache):
    post_id = input("Enter post ID: ")

    posts = cache.get("posts", [])

    match = next((p for p in posts if str(p["id"]) == post_id), None)

    if not match:
        print("❌ Post not found.")
        return

    print("\n📝 POST DETAILS")
    print(json.dumps(match, indent=4))


# CLI Menu
def main():
    cache = initialize_cache()

    while True:
        print("\n========== API Menu ==========")
        print("1. List Posts")
        print("2. View Post By ID")
        print("3. Exit")

        choice = input("➡️  Enter choice: ")

        if choice == "1":
            list_posts(cache)
        elif choice == "2":
            view_post_by_id(cache)
        elif choice == "3":
            print("👋 Exiting...")
            break
        else:
            print("❌ Invalid input!")


if __name__ == "__main__":
    main()

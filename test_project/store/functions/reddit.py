import requests


def get_reddit_posts(subreddit="python", limit=5):
    url = f"https://www.reddit.com/r/{subreddit}/hot.json?limit={limit}"
    headers = {
        "User-Agent": "django-ecommerce-app/1.0"
    }

    response = requests.get(url, headers=headers, timeout=10)
    response.raise_for_status()

    data = response.json()
    posts = []

    for item in data["data"]["children"]:
        post_data = item["data"]
        posts.append({
            "title": post_data.get("title"),
            "author": post_data.get("author"),
            "score": post_data.get("score"),
            "url": f"https://www.reddit.com{post_data.get('permalink')}",
        })

    return posts
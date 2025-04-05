from serpapi import GoogleSearch
import os
from dotenv import load_dotenv

load_dotenv()
SERP_API_KEY = os.getenv("SERP_API")

def search_shopping_items(title, description):
    query = f"{title} {description}"

    params = {
        "engine": "google",
        "q": query,
        "tbm": "shop",  # Target the shopping tab
        "api_key": SERP_API_KEY
    }

    search = GoogleSearch(params)
    results = search.get_dict()

    shopping_results = results.get("shopping_results", [])

    items = []
    for item in shopping_results:
        items.append({
            "title": item.get("title"),
            "price": item.get("price"),
            "source": item.get("source"),
            "link": item.get("link"),
            "thumbnail": item.get("thumbnail")
        })

    return items

# Example usage
if __name__ == "__main__":
    title = "Vintage Wall Clock"
    description = "Wooden antique-style wall clock with roman numerals"

    items = search_shopping_items(title, description)

    for i, item in enumerate(items, 1):
        print(f"\nItem {i}")
        print(f"Title: {item['title']}")
        print(f"Price: {item['price']}")
        print(f"Source: {item['source']}")
        print(f"Link: {item['link']}")
        print(f"Thumbnail: {item['thumbnail']}")

import requests
import os
import base64
import json
from dotenv import load_dotenv

load_dotenv()

IMGBB_API_KEY = os.getenv("IMGBB_API_KEY")
SERPAPI_KEY = os.getenv("SERPAPI_KEY")

# Local image path
image_path = "guitar.JPG"

#Read and encode the image
with open(image_path, "rb") as file:
    image_data = base64.b64encode(file.read()).decode("utf-8")

#Upload to ImgBB
url = "https://api.imgbb.com/1/upload"
payload = {
    "key": IMGBB_API_KEY,
    "image": image_data,
}
response = requests.post(url, data=payload)

if response.status_code == 200:
    image_url = response.json()["data"]["url"]
    print(f"Uploaded to ImgBB: {image_url}")
else:
    print("Upload failed:", response.text)

#Use SerpApi to reverse search
params = {
    "engine": "google_reverse_image",
    "image_url": image_url,
    "api_key": SERPAPI_KEY,
}

serpapi_url = "https://serpapi.com/search"
search_response = requests.get(serpapi_url, params=params)
search_data = search_response.json()


items = False
i = 0
while not items:
    result = search_data.get("image_results", [])[i] if search_data.get("image_results") else None
    if not result:
        print("No image results found")
        exit()
    new_title = result.get("title","")
    print(f"Detected item title: {new_title}")

    #Search on Google Shopping
    shopping_params = {
        "engine": "google_shopping",
        "q": new_title,
        "api_key": SERPAPI_KEY,
    }

    shopping_res = requests.get("https://serpapi.com/search", params=shopping_params)
    shopping_data = shopping_res.json()

    #Extract shopping results with price
    items = shopping_data.get("shopping_results", [])

    
    i += 1



print("\nMatching Shopping Results:")
print(f"Number of items found: {len(items)}")
for item in items[:5]:  # Top 5 results
    title = item.get("title", "No title")
    price = item.get("extracted_price", "No price")
    link = item.get("product_link", "No link")
    print(f"- {title}\n  {price}\n  {link}\n")
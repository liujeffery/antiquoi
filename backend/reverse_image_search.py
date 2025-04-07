import requests
import os
import base64
import json
from dotenv import load_dotenv

load_dotenv()

IMGBB_API_KEY = os.getenv("IMGBB_API_KEY")
SERPAPI_KEY = os.getenv("SERPAPI_KEY")

def upload_image(image_path):
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
        return image_url
    else:
        print("Upload failed:", response.text)
        return None

def get_title_from_image(image_url, result_num):
    #Use SerpApi to reverse search
    params = {
        "engine": "google_reverse_image",
        "image_url": image_url,
        "api_key": SERPAPI_KEY,
    }

    serpapi_url = "https://serpapi.com/search"
    search_response = requests.get(serpapi_url, params=params)
    search_data = search_response.json()
    result = search_data.get("image_results", [])[result_num-1] if search_data.get("image_results") else None
    if not result:
        print("No image results found")
        return None
    new_title = result.get("title","")
    print(f"Detected item title: {new_title}")
    return new_title

def search_w_rev_results(image_url):
    have_results = False
    items = None
    i = 1
    while not have_results:
        new_title = get_title_from_image(image_url, i)
        #Search on Google Shopping
        shopping_params = {
            "engine": "google_shopping",
            "q": new_title,
            "api_key": SERPAPI_KEY,
        }

        shopping_res = requests.get("https://serpapi.com/search", params=shopping_params)
        shopping_data = shopping_res.json()

        if shopping_data.get("shopping_results"):
            have_results = True
            items = shopping_data.get("shopping_results", [])
        else:
            if i < 40:
                i+=1
            else: 
                return 0

    print("\nMatching Shopping Results:")
    print(f"Number of items found: {len(items)}")
    prices = []
    for item in items[:5]:  # Top 5 results only
        title = item.get("title", "No title")
        price = item.get("extracted_price", "No price")
        prices.append(price)
        link = item.get("product_link", "No link")
        print(f"- {title}\n  {price}\n  {link}\n")
    avg =sum(prices) / len(prices)
    print(f"Average price: {avg}")
    return avg
    

# Local image path
image_path = "./backend/uploads/clock.jpg"
image_url = upload_image(image_path)
avg = search_w_rev_results(image_url)

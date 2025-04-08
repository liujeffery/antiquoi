import os
import requests
import base64
from dotenv import load_dotenv
from flask import Flask, request, jsonify
from flask_cors import CORS

# Flask app setup
app = Flask(__name__)
CORS(app)
load_dotenv()

IMGBB_API_KEY = os.getenv("IMGBB_API_KEY")
SERPAPI_KEY = os.getenv("SERPAPI_KEY")

def upload_image(image_path):
    with open(image_path, "rb") as file:
        image_data = base64.b64encode(file.read()).decode("utf-8")

    payload = {
        "key": IMGBB_API_KEY,
        "image": image_data,
    }
    response = requests.post("https://api.imgbb.com/1/upload", data=payload)

    if response.status_code == 200:
        image_url = response.json()["data"]["url"]
        print(f"Uploaded to ImgBB: {image_url}")
        return image_url
    else:
        print("Upload failed:", response.text)
        return None

def get_title_from_image(image_url, result_num):
    params = {
        "engine": "google_reverse_image",
        "image_url": image_url,
        "api_key": SERPAPI_KEY,
    }
    search_response = requests.get("https://serpapi.com/search", params=params)
    search_data = search_response.json()
    result = search_data.get("image_results", [])[result_num-1] if search_data.get("image_results") else None

    if not result:
        print("No image results found")
        return None

    return result.get("title", "")

def search_w_rev_results(image_url):
    have_results = False
    items = None
    i = 1

    while not have_results:
        new_title = get_title_from_image(image_url, i)
        if not new_title:
            return 0

        shopping_params = {
            "engine": "google_shopping",
            "q": new_title,
            "api_key": SERPAPI_KEY,
        }
        shopping_res = requests.get("https://serpapi.com/search", params=shopping_params)
        shopping_data = shopping_res.json()

        if shopping_data.get("shopping_results"):
            have_results = True
            items = shopping_data["shopping_results"]
        else:
            i += 1
            if i > 40:
                return 0

    prices = [item.get("extracted_price") for item in items[:5] if item.get("extracted_price")]

    if not prices:
        return 0

    avg = sum(prices) / len(prices)
    return avg

@app.route('/webhook', methods=['POST'])
def reverse_image_webhook():
    try:
        data = request.get_json()
        image_path = data.get("image_path")

        if not image_path or not os.path.exists(image_path):
            return jsonify({"error": "Invalid image path"}), 400

        image_url = upload_image(image_path)
        if not image_url:
            return jsonify({"error": "Image upload failed"}), 500

        avg_price = search_w_rev_results(image_url)
        return jsonify({"average_price": avg_price}), 200

    except Exception as e:
        print(f"Error in reverse_image_search webhook: {e}")
        return jsonify({"error": str(e)}), 500

if __name__ == "__main__":
    app.run(port=5300)

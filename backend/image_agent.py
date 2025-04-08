import os
from PIL import Image
from dotenv import load_dotenv
from flask import Flask, request, jsonify
from flask_cors import CORS
from google import genai

app = Flask(__name__)
CORS(app)  # Allow cross-origin requests

@app.route('/webhook', methods=['POST'])
def analyze_image_webhook():

    load_dotenv()
    gem_key = os.getenv('GEM_API')
    client = genai.Client(api_key=gem_key)
    model = "gemini-2.0-flash"

    try:
        data = request.get_json()
        image_path = data.get("image_path")
        image = Image.open(image_path)

        prompt = (
            "What is the item in this image, and how much is it worth? "
            "Please give your answer in a .json format with the following fields:\n"
            "Item: <item name>\n"
            "Description: <description>\n"
            "Max price: <max price, integer>\n"
            "Min price: <min price, integer>\n"
            "Condition: <condition of one of: new, used like new, used good, or used fair>"
        )

        response = client.models.generate_content(model=model, contents=[prompt, image])

        return response.text, 200

    except Exception as e:
        print(f"Error in image_agent webhook: {e}")
        return jsonify({'error': str(e)}), 500


if __name__ == '__main__':
    app.run(port=5100)

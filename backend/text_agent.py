import os
from openai import OpenAI
from dotenv import load_dotenv
from flask import Flask, request, jsonify
from flask_cors import CORS

# Flask app setup
app = Flask(__name__)
CORS(app)
load_dotenv()

# OpenRouter (DeepSeek) client setup
dps_key = os.getenv('DPS_API')
client = OpenAI(
    base_url="https://openrouter.ai/api/v1",
    api_key=dps_key,
)

@app.route('/webhook', methods=['POST'])
def analyze_text_webhook():
    try:
        data = request.get_json()
        description = data.get('description')

        if not description:
            return jsonify({'error': 'No description provided'}), 400

        prompt = (
            "Given the following description of an item, please give a response about what the item is, "
            "a description of the item, and a price range. Please give your answer in a .json format "
            "with the following fields: Item: <item here> \n Description: <description here> \n "
            "Max price: <max price, integer> \n Min price: <min price, integer> \n "
            "Condition: <condition of one of new, used like new, used good, or used fair>. \n\n"
            f"Description: {description}"
        )

        response = client.chat.completions.create(
            model="deepseek/deepseek-r1:free",
            messages=[{"role": "user", "content": prompt}]
        )

        return response.choices[0].message.content, 200

    except Exception as e:
        print(f"Error in text_agent webhook: {e}")
        return jsonify({'error': str(e)}), 500


if __name__ == '__main__':
    app.run(port=5200)

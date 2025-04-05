from flask import Flask, request
from flask_cors import CORS
from dotenv import load_dotenv
import os
from google import genai
from google.genai import types
import PIL.Image
import requests
import json
from openai import OpenAI

app = Flask(__name__)
CORS(app)  # Allow cross-origin requests from your mobile app

@app.route('/submit', methods=['POST'])
def submit():
    title = request.form.get('title')
    description = request.form.get('description')
    image = request.files.get('image')  # This will be the uploaded image

    if image:
        image.save(f"./uploads/{image.filename}")
    
    print(f"Title: {title}")
    print(f"Description: {description}")

    gem_key = os.getenv('GEM_API')
    image = PIL.Image.open('./uploads/clock.jpg')
    client = genai.Client(api_key=gem_key)
    response = client.models.generate_content(
        model="gemini-2.0-flash", contents=["What is the item in this image, and how much is it worth? Please give your answer in the following form: Item: <item here> \n Description: <description here> \n Max price: <max price> \n Min price <min price>.", image]
    )
    
    print(response.text)

    dps_key = os.getenv('DPS_API')

    client = OpenAI(
        base_url="https://openrouter.ai/api/v1",
        api_key=dps_key,
    )

    completion = client.chat.completions.create(
        model="deepseek/deepseek-r1:free",
        messages=[
            {
            "role": "user",
            "content": "Given the following description of an item, please give a response about what the item is, a description of the item, and a price range. Please give your answer in the following form: Item: <item here> \n Description: <description here> \n Max price: <max price> \n Min price <min price>. " + description
            }
        ]
    )

    print(completion.choices[0].message.content)

    return {'status': 'success'}, 200



if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5000, debug=True)
import os
from google import genai
from PIL import Image
from dotenv import load_dotenv

load_dotenv()

def analyze_image(image_path: str) -> str:
    gem_key = os.getenv('GEM_API')
    client = genai.Client(api_key=gem_key)

    model = "gemini-2.0-flash"

    image = Image.open(image_path)
    prompt = ("What is the item in this image, and how much is it worth? Please give your answer in a .json format"
              " with the following fields: Item: <item here> \n Description: <description here> \n Max price: <max price. integer> \n Min price <min price, integer> \n "
              "Condition: <condtion of one of new, used like new, used good, or used fair>.")

    response = client.models.generate_content(model=model, contents=[prompt, image])
    return response.text

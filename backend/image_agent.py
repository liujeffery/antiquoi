import os
from google import genai
from PIL import Image
from dotenv import load_dotenv

class ImageAgent(KnowledgeSource):
    def __init__(self):
        self.opinion = ""

    def get_expert_opinion(self):
        return self.opinion

    def analyze_image(image_path: str) -> str:
        load_dotenv()
        gem_key = os.getenv('GEM_API')
        client = genai.Client(api_key=gem_key)

        model = "gemini-2.0-flash"

        image = Image.open(image_path)
        prompt = ("What is the item in this image, and how much is it worth? Please give your answer in "
                  "the following form: Item: <item here> \n Description: <description here> \n Max price: <max price> \n Min price <min price> \n Condition: <condtion of either new, used like new, used good, or used fair>.")

        response = client.models.generate_content(model=model, contents=[prompt, image])
        self.opinion = response.text

import os
from google import genai
from PIL import Image
from dotenv import load_dotenv
import knowledge_source

class image_agent(knowledge_source):
    load_dotenv()

    def __init__(self):
            self.gem_key = os.getenv('GEM_API')
            self.client = genai.Client(api_key=self.gem_key)
            self.model = "gemini-2.0-flash"

    def execute(self, image_path: str) -> str:

        image = Image.open(image_path)
        prompt = ("What is the item in this image, and how much is it worth? Please give your answer in a .json format"
                " with the following fields: Item: <item here> \n Description: <description here> \n Max price: <max price. integer> \n Min price <min price, integer> \n "
                "Condition: <condtion of one of new, used like new, used good, or used fair>.")

        response = self.client.models.generate_content(model=self.model, contents=[prompt, image])
        return response.text

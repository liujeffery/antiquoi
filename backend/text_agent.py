import os
from openai import OpenAI
from dotenv import load_dotenv

load_dotenv()

def analyze_description(description: str) -> str:
    dps_key = os.getenv('DPS_API')
    client = OpenAI(
        base_url="https://openrouter.ai/api/v1",
        api_key=dps_key,
    )

    prompt = ("Given the following description of an item, please give a response about what the item is, "
              "a description of the item, and a price range. Please give your answer in a .json format"
              " with the following fields: Item: <item here> \n Description: <description here> \n Max price: <max price. integer> \n Min price <min price, integer> \n "
              "Condition: <condtion of one of new, used like new, used good, or used fair>. "
              + description)

    response = client.chat.completions.create(
        model="deepseek/deepseek-r1:free",
        messages=[{"role": "user", "content": prompt}]
    )

    return response.choices[0].message.content
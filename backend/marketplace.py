import os
from openai import OpenAI
from dotenv import load_dotenv

load_dotenv()

def generate_marketplace_text(description: str, name: str, price: str, condition: str) -> str:
    dps_key = os.getenv('DPS_API')
    client = OpenAI(
        base_url="https://openrouter.ai/api/v1",
        api_key=dps_key,
    )

    prompt = ("Given the following description of an item, please generate a description that helps selling this item on Facebook marketplace"
              "Please give your answer in the following form: "
              "Suggested description: <description here>"
             + description)

    response = client.chat.completions.create(
        model="deepseek/deepseek-r1:free",
        messages=[{"role": "user", "content": prompt}]
    )

    return "Title: "+name+"\nPrice: "+price+"\n"+"Category: Antiques & Collectibles\nCondition: "+condition+"\n"+response.choices[0].message.content
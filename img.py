import os
from openai import AzureOpenAI
import json
import requests
from dotenv import load_dotenv
from text_generate import *
import streamlit as st

load_dotenv()
client = AzureOpenAI(
    api_version="2024-05-01-preview",
    azure_endpoint="https://shikhar.openai.azure.com/",
    api_key=os.getenv("img_key")
)


def gen_img():

    with open("prompt.txt", "r") as f:
        a = f.read()
    
    prompt = f'''Based on the {a}, generate two vertically aligned, simple images in a clear and organized layout. 
    The images should visually represent the concept with basic elements, avoiding unnecessary detail or complexity. 
    Ensure both images are easy to understand and educational, with no controversial or sensitive content.'''
    
    for i in range(2):  # Loop to generate two images
        result = client.images.generate(
            model="dalle3",  # the name of your DALL-E 3 deployment
            prompt=prompt,
            n=1  # Generate one image per request
        )

        # Fetch the URL of the generated image
        image_url = json.loads(result.model_dump_json())['data'][0]['url']
        image_response = requests.get(image_url)

        if image_response.status_code == 200:
            # Save images with different names
            with open(f"genimg_{i + 1}.png", "wb") as image_file:
                image_file.write(image_response.content)
    st.image("genimg_1.png")

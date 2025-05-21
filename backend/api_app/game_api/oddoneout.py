import os
import json
import random
import openai
import requests
from dotenv import load_dotenv

# Load environment variables
load_dotenv()
openai.api_key = os.getenv("OPENAI_API_KEY")
GETIMG_API_KEY = os.getenv("GETIMG_API_KEY")

if not openai.api_key or not GETIMG_API_KEY:
    raise Exception("API keys missing in environment variables")

def generate_image_openai(prompt: str) -> str:
    image_prompt = f"""
Generate an image based on the following prompt: "{prompt}". 
Ensure the response is a clear and visually appealing representation of the word or concept described. 
The image should be suitable for use in a grid-based odd-one-out game.
"""

    try:
        response = openai.chat.completions.create(
            model="gpt-3.5-turbo",
            messages=[{"role": "user", "content": image_prompt}],
            temperature=0.5,
            max_tokens=100
        )
        content = response.choices[0].message.content.strip()
        url_match = next((token for token in content.split() if token.startswith("http")), None)
        if not url_match:
            raise ValueError("No image URL found in OpenAI response.")
        return url_match
    except Exception as e:
        raise RuntimeError(f"OpenAI image generation failed: {e}")

def generate_image_fallback(prompt: str) -> str:
    url = "https://api.getimg.ai/v1/flux-schnell/text-to-image"
    headers = {
        "accept": "application/json",
        "content-type": "application/json",
        "Authorization": f"Bearer {GETIMG_API_KEY}"
    }
    data = {
        "prompt": prompt,
        "width": 1024,
        "height": 1024,
        "steps": 4,
        "seed": 0,
        "output_format": "jpeg",
        "response_format": "url"
    }

    response = requests.post(url, headers=headers, json=data)
    if response.status_code != 200:
        raise RuntimeError("Getimg.ai image generation failed")

    return response.json()["url"]

def generate_image(prompt: str) -> str:
    try:
        return generate_image_openai(prompt)
    except Exception as e:
        print("OpenAI failed, trying fallback:", e)
        return generate_image_fallback(prompt)

def odd_one_out_game(word: str) -> dict:
    try:
        grid_size = 4
        grid_count = grid_size * grid_size

        base_image = generate_image(word)
        odd_image = generate_image(f"{word} variations")

        images = [{"src": base_image, "isOdd": False} for _ in range(grid_count)]

        odd_index = random.randint(0, grid_count - 1)
        images[odd_index] = {"src": odd_image, "isOdd": True}

        return {
            "gameType": "odd_one_out",
            "topic": word,
            "images": images,
            "oddIndex": odd_index
        }

    except Exception as e:
        raise Exception(f"Failed to generate odd one out game: {e}")

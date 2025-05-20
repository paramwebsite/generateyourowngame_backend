import json
import os
import random
import requests
import openai
from dotenv import load_dotenv
#from api_app.services.image_generate import generate_image

# Set your API keys from environment variables comment added to commit
load_dotenv()
openai.api_key = os.getenv("OPENAI_API_KEY")
GETIMG_API_KEY = os.getenv("GETIMG_API_KEY")
if not openai.api_key:
    raise Exception("OPENAI_API_KEY not set in environment variables.")
if not GETIMG_API_KEY:
    raise Exception("GETIMG_API_KEY not set in environment variables.")

def generate_image(prompt_str: str) -> str:
    """
    Generate an image using the GETIMG API based on the prompt string.
    Returns the generated image URL.
    """
    url = "https://api.getimg.ai/v1/flux-schnell/text-to-image"
    headers = {
        "Accept": "application/json",
        "Content-Type": "application/json",
        "Authorization": f"Bearer {GETIMG_API_KEY}",
    }
    payload = {
        "prompt": f"Generate a high-quality image of a {prompt_str}",
        "width": 1024,
        "height": 1024,
        "steps": 4,
        "seed": 0,
        "output_format": "jpeg",
        "response_format": "url",
    }
    try:
        response = requests.post(url, headers=headers, json=payload)
        response.raise_for_status()
        data = response.json()
        image_url = data.get("url")
        if not image_url:
            raise Exception("No image URL returned by GETIMG API.")
        return image_url
    except Exception as e:
        raise Exception(f"Error generating image for '{prompt_str}': {e}")

def connectpuzzle(word: str) -> dict:
    """
    Given a word, uses OpenAI's ChatCompletion API to:
      1. Generate two distinct lists of 4 unique objects/characters.
      2. Generate logical pairs from those lists.
      3. Attach an image URL to each item using the GETIMG API.
    
    Returns a dictionary with leftItems, rightItems, and pairs.
    """
    # Step 1: Generate lists of items based on the word.
    prompt1 = (
        f'''Generate two distinct lists of 4 unique objects or characters each, based on the word "{word}". 
        Each list should contain unique items, and items in one list should not appear in the other. '
        Ensure the items are logically pairable. Provide output in this JSON format:
        {{
          "leftItems": [
            {{ "id": 1, "name": "Catnip" }},
            {{ "id": 2, "name": "Kitten" }},
            {{ "id": 3, "name": "Scratching post" }},
            {{ "id": 4, "name": "Cat bed" }}
          ],
          "rightItems": [
            {{ "id": 5, "name": "Dog" }},
            {{ "id": 6, "name": "Fish" }},
            {{ "id": 7, "name": "Bird" }},
            {{ "id": 8, "name": "Mouse" }}
          ]
        }}'''
    )
    try:
        openai_response1 = openai.chat.completions.create(
            model="gpt-3.5-turbo",
            messages=[{"role": "user", "content": prompt1}],
            temperature=0.7,
        )
    except Exception as e:
        raise Exception(f"OpenAI API call for list generation failed: {e}")

    content1 = openai_response1.choices[0].message.content.strip()
    try:
        generatedData = json.loads(content1)
    except Exception as e:
        raise Exception(f"Failed to parse generated list JSON: {e}")

    left_items = generatedData.get("leftItems")
    right_items = generatedData.get("rightItems")
    if not left_items or not right_items:
        raise Exception("Generated lists are empty or malformed.")

    # Step 2: Generate pairs dynamically using OpenAI.
    left_names = [item["name"] for item in left_items]
    right_names = [item["name"] for item in right_items]

    prompt2 = (
        f'''Given the following two lists of items, generate logical pairs based on their relationships:
        Left items: {json.dumps(left_names)}
        Right items: {json.dumps(right_names)}
        Provide output in this format:
        {{
          "pairs": [
            {{ "leftItem": "Catnip", "rightItem": "Mouse" }},
            {{ "leftItem": "Kitten", "rightItem": "Dog" }}
         ]
        }}'''
    )
    try:
        openai_response2 = openai.chat.completions.create(
            model="gpt-3.5-turbo",
            messages=[{"role": "user", "content": prompt2}],
            temperature=0.7,
        )
    except Exception as e:
        raise Exception(f"OpenAI API call for pair generation failed: {e}")

    content2 = openai_response2.choices[0].message.content.strip()
    try:
        pairs_data = json.loads(content2)
    except Exception as e:
        raise Exception(f"Failed to parse pairs JSON: {e}")

    pairs = pairs_data.get("pairs")
    if pairs is None:
        raise Exception("Pairs not found in the generated data.")

    # Step 3: Attach images to each item.
    leftItemsWithImages = []
    for item in left_items:
        try:
            image = generate_image(item["name"])
        except Exception as e:
            image = None  # Optionally, set a default image URL
        item_copy = item.copy()
        item_copy["image"] = image
        leftItemsWithImages.append(item_copy)

    rightItemsWithImages = []
    for item in right_items:
        try:
            image = generate_image(item["name"])
        except Exception as e:
            image = None
        item_copy = item.copy()
        item_copy["image"] = image
        rightItemsWithImages.append(item_copy)

    result = {
        "leftItems": leftItemsWithImages,
        "rightItems": rightItemsWithImages,
        "pairs": pairs,
    }
    return result
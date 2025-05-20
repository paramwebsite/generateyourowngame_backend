import os
import json
import requests
from dotenv import load_dotenv

load_dotenv()
def generate_image(prompt: str) -> dict:
    """
    Generates an image based on the prompt using the Getimg API.

    Args:
        prompt (str): The text prompt for image generation.

    Returns:
        dict: A dictionary containing the generated image URL(s).

    Raises:
        Exception: If the API key is not set, the API call fails,
                   or the response cannot be parsed.
    """
    # Retrieve the API key from environment variables
    api_key = os.getenv("GETIMG_API_KEY")
    if not api_key:
        raise Exception("GETIMG_API_KEY not set in environment variables.")

    # Define the API endpoint and headers
    url = "https://api.getimg.ai/v1/flux-schnell/text-to-image"
    headers = {
        "Accept": "application/json",
        "Content-Type": "application/json",
        "Authorization": f"Bearer {api_key}"
    }

    # Define the payload for the POST request
    payload = {
        "prompt": prompt,
        "width": 1024,
        "height": 1024,
        "steps": 4,
        "seed": 0,
        "output_format": "jpeg",
        "response_format": "url"
    }

    # Send the POST request to the image generation API
    try:
        response = requests.post(url, headers=headers, json=payload)
        response.raise_for_status()  # Raise an exception for HTTP errors
    except requests.RequestException as e:
        raise Exception("Error fetching data from image generation API: " + str(e))

    # Parse the JSON response
    try:
        json_response = response.json()
    except json.JSONDecodeError as e:
        raise Exception("Error parsing JSON response: " + str(e))

    # Extract the image URL(s) from the response.
    # Adjust the key if the API response structure is different.
    images = json_response.get("url")
    if images is None:
        raise Exception("No image URL found in the API response.")

    return {"images": images}

# Example usage:
# if __name__ == "__main__":
#     test_prompt = "A beautiful sunset over a mountain range"
#     try:
#         result = generate_image(test_prompt)
#         print("Image generation result:", result)
#     except Exception as error:
#         print("Error:", error)
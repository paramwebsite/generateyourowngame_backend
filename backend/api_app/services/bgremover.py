# api_app/services/background_remover.py

from rembg import remove
from PIL import Image
import requests
from io import BytesIO
import os

def remove_background(image_url: str, identifier: str = "image") -> dict:
    """
    Downloads the image from a URL, removes the background, saves, and returns the path or URL.

    Args:
        image_url (str): The URL of the image to process.
        identifier (str): Unique label for saving output.

    Returns:
        dict: A dictionary with the cleaned image URL or local path.
    """
    response = requests.get(image_url)
    image = Image.open(BytesIO(response.content))

    output = remove(image)
    if output.mode == "RGBA":
        output = output.convert("RGB")

    save_path = f"media/bg_removed_{identifier}.jpg"
    os.makedirs("media", exist_ok=True)
    output.save(save_path)

    return {"imageUrl": f"/media/bg_removed_{identifier}.jpg"}

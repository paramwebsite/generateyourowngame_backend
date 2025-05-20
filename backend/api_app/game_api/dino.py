# api_app/services/game_asset_service.py

from api_app.services.image_generate import generate_image
from api_app.services.bgremover import remove_background

def dino(word: str) -> dict:
    """
    Generates player and obstacle images based on the input word,
    and removes the backgrounds.

    Args:
        word (str): The input word to generate character and obstacle from.

    Returns:
        dict: A dictionary containing URLs to the player and obstacle images.
    """
    # Prompt for player and obstacle
    player_prompt = (
        f"{word} character in motion, facing the right side, with a white background. "
        "The character must have vibrant and distinct colors, avoiding white tones in the character's appearance, "
        "with a dynamic pose and visible movement elements (e.g., flowing hair or clothing). "
        "Remember the animal face should be facing right only."
    )

    obstacle_prompt = (
        f"An obstacle conceptually inspired by the word \"{word}\", with a white background. "
        "The design should visually represent the essence or challenges associated with the word "
        f"\"{word}\" and be oriented facing 90 degrees to the left or right."
    )

    # Generate both images
    player_raw = generate_image(player_prompt)["images"]
    obstacle_raw = generate_image(obstacle_prompt)["images"]

    # Remove background
    player_clean = remove_background(player_raw, identifier="player")
    obstacle_clean = remove_background(obstacle_raw, identifier="obstacle")

    return {
        "playerImage": player_clean["imageUrl"],
        "obstacleImage": obstacle_clean["imageUrl"]
    }

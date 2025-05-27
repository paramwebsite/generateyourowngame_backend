from api_app.services.image_generate import generate_image  # Your existing image generator
import random

def flip_memory_game(word: str) -> dict:
    """
    Generates image pairs for a flip memory game based on a given word.

    Args:
        word (str): The topic word used to generate themed images.

    Returns:
        dict: Game data including shuffled image cards with matching pairs.
    """
    try:
        image_urls = []

        # Generate 6 unique images
        for i in range(6):
            prompt = f"Generate {word} image {i + 1}"
            result = generate_image(prompt)
            image_urls.append(result["images"])

        # Duplicate each image to create pairs and shuffle
        cards = [{"src": url, "id": f"{i}_a"} for i, url in enumerate(image_urls)] + \
                [{"src": url, "id": f"{i}_b"} for i, url in enumerate(image_urls)]
        random.shuffle(cards)

        return {
            "gameType": "flip_memory",
            "topic": word,
            "cards": cards
        }

    except Exception as e:
        raise Exception(f"Failed to generate flip memory game images: {e}")

from api_app.services.image_generate import generate_image 

def arrange_picture_game(word: str) -> dict:
    """
    Generates an image for an 'Arrange the Picture' game based on a word/topic.

    Args:
        word (str): The central word or concept for image generation.

    Returns:
        dict: Game data including the generated image URL.
    """
    try:
        prompt = (
            f"Create a square, vibrant illustration of {word} plant as the central focus. "
            "Ensure clarity, balance, and visual appeal . ensure creating image of the plant {word}. nothing written on the image"
        )

        result = generate_image(prompt)
        return {
            "gameType": "arrange_picture",
            "topic": word,
            "image": result["images"]
        }

    except Exception as e:
        raise Exception(f"Failed to generate arrange picture game image: {e}")

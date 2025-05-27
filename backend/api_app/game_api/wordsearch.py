import os
import openai
from dotenv import load_dotenv

load_dotenv()
openai.api_key = os.getenv("OPENAI_API_KEY")

def generate_word_search_names(word: str) -> dict:
    """
    Generates a list of 5 name-like words related to the given topic using OpenAI.

    Args:
        word (str): The base topic for generating related names.

    Returns:
        dict: A dictionary with a list of generated words.
    """
    if not word or not isinstance(word, str):
        raise ValueError("Invalid input. Please provide a valid word.")

    prompt = f"""
    Generate 5 random words related to the topic "{word}". 
    The words should:
    1. Be relevant to the topic.
    2. Each word should be about 5 letters in length.
    3. Avoid special characters or numbers.
    Provide the output as a comma-separated list, e.g., "alice, emily, david, brian, clara".
    """

    try:
        response = openai.chat.completions.create(
                model="gpt-4o-mini-2024-07-18",
                messages=[{"role": "user", 
                        "content": prompt}],
                max_tokens=100,
                temperature=0.7,
            )
        content = response.choices[0].message.content
        words = [w.strip().lower() for w in content.split(",") if w.strip()]
        return { "words": words }
    except Exception as e:
        raise Exception(f"Failed to generate word search list: {e}")

import os
import openai
from dotenv import load_dotenv

load_dotenv()
openai.api_key = os.getenv("OPENAI_API_KEY")

def validate_word_associations(entries: list) -> dict:
    """
    Validates a list of word-category pairs to determine if the word belongs to the category.

    Args:
        entries (list): A list of dictionaries, each with 'word' and 'category' keys.

    Returns:
        dict: A dictionary containing the validated entries with an added 'valid' boolean key.
    """
    if not isinstance(entries, list):
        raise ValueError("Invalid input format. Expected a list of entries.")

    validated_results = []

    for entry in entries:
        word = entry.get("word")
        category = entry.get("category")

        if not word or not category:
            continue  # Skip invalid entries

        prompt = f'Is the word "{word}" a valid example of the category "{category}"? Please respond with "yes" or "no".'

        try:
            response = openai.chat.completions.create(
                model="gpt-4o-mini-2024-07-18",
                messages=[{"role": "user", 
                        "content": prompt}],
                max_tokens=100,
                temperature=0.7,
            )
            reply = response.choices[0].message.content.strip().lower()
            is_valid = "yes" in reply
            validated_results.append({ **entry, "valid": is_valid })
        except Exception as e:
            print(f"Error validating word '{word}': {e}")
            validated_results.append({ **entry, "valid": False })

    return { "results": validated_results }

import json
import os
import re
import openai
from dotenv import load_dotenv

# Load environment variables
load_dotenv()
openai.api_key = os.getenv("OPENAI_API_KEY")
if not openai.api_key:
    raise Exception("OPENAI_API_KEY not set in environment variables.")

def word_hint_game(word: str) -> dict:
    """
    Generates a list of 5 words with hints related to the given topic.
    Returns a dictionary containing the game type, topic, and word-hint pairs.
    """
    prompt = f'''Generate a list of 5 words related to the topic "{word}".
Each word should have a short, clear hint or definition.
Return the data in JSON array format like this:
[
  {{ "word": "addition", "hint": "The process of adding numbers" }},
  {{ "word": "meeting", "hint": "An event where people come together" }}
]'''

    try:
        response = openai.chat.completions.create(
            model="gpt-4o-mini-2024-07-18",
            messages=[{"role": "user", "content": prompt}],
            temperature=0.7,
            max_tokens=300
        )
        content = response.choices[0].message.content.strip()

        # Extract the JSON array using regex (robust handling of extra data)
        json_match = re.search(r'\[\s*{.*?}\s*]', content, re.DOTALL)
        if not json_match:
            raise ValueError("No valid JSON array found in OpenAI response.")
        
        word_list = json.loads(json_match.group(0))

    except Exception as e:
        raise Exception(f"Error generating word hint game: {e}")

    return {
        "gameType": "wordhint",
        "topic": word,
        "words": word_list
    }

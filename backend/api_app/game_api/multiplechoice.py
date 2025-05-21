import json
import os
import openai
from dotenv import load_dotenv

# Load .env variables
load_dotenv()
openai.api_key = os.getenv("OPENAI_API_KEY")
if not openai.api_key:
    raise Exception("OPENAI_API_KEY not set in environment variables.")

def multiple_choice_game(word: str) -> dict:
    """
    Given a topic word, generate 3 multiple-choice questions with four options and a correct answer.
    Returns a dictionary containing the game type, topic, and questions list.
    """
    prompt = f'''Generate three multiple-choice questions about the topic "{word}". 
Each question should have four answer options and indicate which option is correct.
Please respond in JSON format only, like this:
[
  {{
    "id": 1,
    "question": "What is the largest organ in the human body?",
    "options": [
      {{ "id": "a", "text": "Heart" }},
      {{ "id": "b", "text": "Skin" }},
      {{ "id": "c", "text": "Liver" }},
      {{ "id": "d", "text": "Lungs" }}
    ],
    "answer": "b"
  }}
]
'''

    try:
        response = openai.chat.completions.create(
            model="gpt-4o-mini-2024-07-18",
            messages=[{"role": "user", "content": prompt}],
            temperature=0.7,
            max_tokens=500
        )
        content = response.choices[0].message.content.strip()
        
        # Clean up malformed JSON if needed
        if not content.startswith("["):
            content = "[" + content.split("[", 1)[-1]
        
        questions = json.loads(content)
    except Exception as e:
        raise Exception(f"Error generating multiple choice questions: {e}")

    return {
        "gameType": "multiplechoice",
        "topic": word,
        "questions": questions
    }

import json
import os
import openai
from dotenv import load_dotenv

# Load environment variables from .env
load_dotenv()
openai.api_key = os.getenv("OPENAI_API_KEY")
if not openai.api_key:
    raise Exception("OPENAI_API_KEY not set in environment variables.")

def true_false_game(word: str) -> dict:
    """
    Given a word (topic), generate a set of true or false questions using OpenAI API.
    Returns a dictionary containing the questions with id, question text, and true/false answer.
    """
    prompt = (
        f'''Generate a bunch(5-6 Questions) of true or false questions related to the topic "{word}". 
Each question should be simple and factual. Provide the questions in JSON format, where each question includes:
"id", "question", and "answer" (true or false).

Example:
[
  {{"id": 1, "question": "The sky is blue.", "answer": true}},
  {{"id": 2, "question": "Cats can fly.", "answer": false}}
]
'''
    )

    try:
        response = openai.chat.completions.create(
            model="gpt-3.5-turbo",
            messages=[{"role": "user", "content": prompt}],
            temperature=0.7,
            max_tokens=300,
        )
        content = response.choices[0].message.content.strip()
        questions = json.loads(content)
    except Exception as e:
        raise Exception(f"Error fetching data from OpenAI: {e}")

    return {
        "gameType": "true_false",
        "topic": word,
        "questions": questions
    }
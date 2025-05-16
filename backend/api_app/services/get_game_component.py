import json
import random
import os
import openai
from dotenv import load_dotenv
from pydantic import BaseModel, ValidationError

# Set your OpenAI API key from the environment variable
load_dotenv()
api_key = os.getenv('OPENAI_API_KEY')
if not api_key:
    raise Exception("OPENAI_API_KEY not set in environment")
openai.api_key = api_key

# Predefined data structure
data_structure = {
    "food": {
        "food": ["food"],
    },
    "humanNames": {
        "namegame": ["WordAssociationGame", "wordSearchforfood"],
    },
    "organisation": {
        "organisation": ["decode", "arrangemain"]
    },
    "living": {
        "animal": ["dino", "connectpuzzle"],
        "plants": ["arrangemain", "seedcatcher"],
        "micro_organisms": ["truefalse", "oddoneout"],
        "humans": ["multiplechoice"],
    },
    "nonLiving": {
        "natural_object": ["cardgame"],
        "man_made": ["unscatteredpuzzle"],
        "elements_and_compounds": ["multiplechoice"],
    },
    "both_living_and_nonliving": {
        "ecosystem": ["arrangemain", "ecosystem"],
        "hybrid_concepts": ["multiplechoice"],
    },
    "neither_living_nor_nonliving": {
        "emotion": ["unscatteredpuzzle"],
        "ideas_and_concepts": ["arrangemain"],
        "mathematical_concepts": ["truefalse"],
    },
}

def classify_word(prompt: str) -> dict:
    """
    Given an input word (prompt), calls the OpenAI ChatCompletion API to classify
    it into a category and subcategory, and selects a game path based on a predefined data structure.
    
    Args:
        prompt (str): The input word.
    
    Returns:
        dict: A dictionary with 'category', 'subcategory', and 'path'.
    """


    # Build the prompt message including special rules
    prompt_message = (
        f'''Given the word "{prompt}", classify it into categories and subcategories based on a complex data structure and suggest a suitable game path in the below mentioned format (remember only return the data in output format nothing extra). Here is the data structure:
        {json.dumps(data_structure, indent=2)}
        Special rule: 1. If the input word is "param", classify it into the "organisation" category, regardless of the other categories. For the "organisation" category, the path should switch between "decode" or "arrangemain" dynamically.
        2. If the input word belongs to another category, follow the standard classification process."
        3. For example:"
           - If the input word is "dog", the expected output might be:
           {{
             "category": "living",
             "subcategory": "animal",
             "path": "dino"
           }}
          - If the input word is "param", the expected output might be:
          {{
             "category": "organisation"
             "subcategory": "organisation",
             "path": "decode"
           }}
           - If "param" is used again, the subcategory might dynamically switch to "arrangemain", resulting in:
           {{
             "category": "organisation"
             "subcategory": "organisation",
            "path": "arrangemain"
           }}'''
    )
    
    try:
        class Word_Class(BaseModel):
            category: str
            subcategory: str
            path: str


        # Call OpenAI's ChatCompletion API
        try:
            response = openai.chat.completions.create(
                model="gpt-3.5-turbo",
                messages=[{"role": "user", 
                        "content": prompt_message}],
                temperature=0.5,
            )
        except Exception as api_err:
            raise Exception(f"OpenAI API call failed: {api_err}")
        
        try:
            content_string = response.choices[0].message.content.strip()
        except (IndexError, AttributeError) as extract_err:
            raise Exception(f"Failed to extract content from API response: {extract_err}")

        # print("API Response:", response)
        # print("Content string:", content_string)


        start_index = content_string.find("{")
        end_index = content_string.rfind("}")
        if start_index == -1 or end_index == -1:
            raise ValueError("No valid JSON block found in the provided content.")
        
        # Extract the JSON substring
        json_str = content_string[start_index:end_index + 1]
        
        # Parse the JSON string into a dictionary
        try:
            parsed_data = json.loads(json_str)
        except json.JSONDecodeError as json_err:
            raise Exception(f"Error decoding JSON: {json_err}")
        
        # Validate and parse the dictionary using the Pydantic model
        try:
            parsed_obj = Word_Class(**parsed_data)
        except ValidationError as val_err:
            raise Exception(f"Pydantic validation error: {val_err}")

        # Use the parsed object's attributes directly.
        category = parsed_obj.category
        subcategory = parsed_obj.subcategory
        if not category or not subcategory:
            raise Exception("Response JSON is missing 'category' or 'subcategory'.")

        if category not in data_structure or subcategory not in data_structure[category]:
            raise Exception("Invalid category or subcategory.")

        # Select a random game path from the available options
        try:
            paths = data_structure[category][subcategory]
            if not paths:
                raise Exception("No game paths available for this category/subcategory.")
            selected_path = random.choice(paths)
        except Exception as choice_err:
            raise Exception(f"Error selecting a game path: {choice_err}")

        result = {
            "category": category,
            "subcategory": subcategory,
            "path": selected_path
        }

        return result

    except Exception as e:
        raise Exception(f"Error in classification: {e}")

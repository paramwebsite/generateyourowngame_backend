# from django.shortcuts import render

# # Create your views here.
# import json
# from .services.wordfilter import filter_harmful_word
# from .services.get_game_component import classify_word
# #from .game_api.puzzle import connect_puzzle
# from api_app.game_api.puzzle import connect_puzzle
# from api_app.game_api.dino import dino
# from django.http import JsonResponse, HttpResponseNotAllowed
# from django.views.decorators.csrf import csrf_exempt

# GAME_FUNCTIONS = {
#     "puzzle": connect_puzzle,
#     "dino": dino,
#     # add more mappings like "snake": connect_snake, etc.
# }

# @csrf_exempt  # For development; use proper CSRF protection in production.

# def process_word(request):
#     if request.method == 'POST':
#         try:
#             data = json.loads(request.body)
#         except json.JSONDecodeError:
#             return JsonResponse({'error': 'Invalid JSON'}, status=400)
        
#         """
#         checkpoint 1
#         word get
#         word count
#         word filter
#         """
#         word = data.get('word', '')
#         # validate word input
#         if not word or len(word.split()) > 3:
#             return JsonResponse({"success": False,'error': 'Please provide 1-3 words.'}, status=400)

#         # Filter harmful words
#         category = filter_harmful_word(word)
#         if category != "not harmful":
#             # log_to_csv(word, category)
#             return JsonResponse({"success": False,'error': 'The word is harmful.'}, status=400)
        
#         print("checkpoint 1 clear")

#         """
#         checkpoint 2
#         get game component 
#         """
#         word_class=classify_word(word)
#         response_data = word_class

#         print("checkpoint 2 clear")

#         return JsonResponse(response_data)
    
#     else:
#         return JsonResponse({'error': 'Invalid HTTP method, only POST allowed'}, status=405)


# @csrf_exempt 
# def connectpuzzle(request):
#     if request.method != "POST":
#         return HttpResponseNotAllowed(["POST"])
    
#     try:
#         body = json.loads(request.body)
#     except Exception as e:
#         return JsonResponse({"error": f"Invalid JSON: {e}"}, status=400)
    
#     word = body.get("word")

#     if not word:
#         return JsonResponse({"error": "No word provided"}, status=400)
    
#     try:
#         result = connect_puzzle(word)
#         return JsonResponse(result)
#     except Exception as e:
#         return JsonResponse({"error": str(e)}, status=500)



from django.http import JsonResponse, HttpResponseNotAllowed
from django.views.decorators.csrf import csrf_exempt
import json
import random

from django.shortcuts import render
from .services.wordfilter import filter_harmful_word
from .services.get_game_component import classify_word, data_structure

from api_app.game_api.puzzle import connectpuzzle
from api_app.game_api.dino import dino
from api_app.game_api.truefalse import true_false_game
from api_app.game_api.multiplechoice import multiple_choice_game
from api_app.game_api.oddoneout import odd_one_out_game
from api_app.game_api.flipword import flip_memory_game
from api_app.game_api.arrange_picture import arrange_picture_game
from api_app.game_api.wordsearch import generate_word_search_names
from api_app.game_api.word_association import validate_word_associations

GAME_FUNCTIONS = {
    "connectpuzzle": connectpuzzle,
    "dino": dino,
    "truefalse": true_false_game,
    "multiplechoice": multiple_choice_game,
    "oddoneout": odd_one_out_game,
    "cardgame": flip_memory_game,
    "arrangemain": arrange_picture_game,
    "wordsearch": generate_word_search_names,
    "wordassociationgame":validate_word_associations,
    # add other game mappings here
}

# @csrf_exempt
# def process_and_connect_game(request):
#     if request.method != "POST":
#         return HttpResponseNotAllowed(["POST"])

#     try:
#         data = json.loads(request.body)
#     except json.JSONDecodeError:
#         return JsonResponse({'error': 'Invalid JSON'}, status=400)

#     word = data.get('word', '')
#     print("word", word)

#     # Validate word presence and length
#     if not word or len(word.split()) > 3:
#         return JsonResponse({"success": False, 'error': 'Please provide 1-3 words.'}, status=400)
#     print("word length pass")

#     # Filter harmful words
#     category = filter_harmful_word(word)
#     if category != "not harmful":
#         return JsonResponse({"success": False, 'error': 'The word is harmful.'}, status=400)
#     else:
#         print("word filter pass")

#     # Classify the word to get the game path and other info
#     classification_result = classify_word(word)
#     print("classification:", classification_result)

#     selected_path = classification_result.get("path")
#     print("path:", selected_path)
#     if not selected_path:
#         return JsonResponse({"success": False, 'error': 'No game path found for the word.'}, status=400)


#     game_func = GAME_FUNCTIONS.get(selected_path.lower())
#     if not game_func:
#         return JsonResponse({"success": False, 'error': f"No game logic found for path '{selected_path}'."}, status=400)
    

#     # SPECIAL CASE: wordassociationgame
#     if selected_path.lower() == "wordassociationgame":
#         prompt = word  # You may use the input word as prompt
#         return JsonResponse({
#             "success": True,
#             "classification": classification_result,
#             "prompt": prompt,
#             "game_type": "delayed"  # optional hint for frontend
#         })

#     # NORMAL CASE: other games
#     try:
#         game_result = game_func(word)
#     except Exception as e:
#         return JsonResponse({"success": False, 'error': f"Game processing error: {str(e)}"}, status=500)
#     print("game func called")

#     # Return combined response
#     response_data = {
#         "success": True,
#         "classification": classification_result,
#         "game_data": game_result,
#     }

#     return JsonResponse(response_data)

@csrf_exempt
def process_and_connect_game(request):
    if request.method != "POST":
        return HttpResponseNotAllowed(["POST"])

    # 1. Parse JSON
    try:
        payload = json.loads(request.body)
    except json.JSONDecodeError:
        return JsonResponse({"error": "Invalid JSON"}, status=400)

    word = payload.get("word", "").strip()
    if not word or len(word.split()) > 3:
        return JsonResponse({"success": False, "error": "Please provide 1-3 words."}, status=400)

    # 2. Harmful-word filter
    if filter_harmful_word(word) != "not harmful":
        return JsonResponse({"success": False, "error": "The word is harmful."}, status=400)

    # 3. Classify (category, subcategory, initial path)
    try:
        classification = classify_word(word)
    except Exception as e:
        return JsonResponse({"success": False, "error": f"Classification error: {e}"}, status=500)

    category    = classification["category"]
    subcategory = classification["subcategory"]
    chosen_path = classification["path"]

    # 4. No-repeat logic in the view itself
    last_path = request.session.get("last_game_path")
    if last_path is not None:
        if last_path == chosen_path:
            # get all possible paths for this cat/subcat
            options = data_structure[category][subcategory]
            # filter out the last one
            alternatives = [p for p in options if p != last_path]
            if alternatives:
                chosen_path = random.choice(alternatives)
                classification["path"] = chosen_path
            # else: if no alternative, we just stick with chosen_path

    # store for next time
    request.session["last_game_path"] = chosen_path

    # 5. Handle word-association as a special “delayed” case
    if chosen_path.lower() == "wordassociationgame":
        return JsonResponse({
            "success": True,
            "classification": classification,
            "prompt": word,
            "game_type": "delayed"
        })

    # 6. Route to the appropriate game function
    game_func = GAME_FUNCTIONS.get(chosen_path.lower())
    if not game_func:
        return JsonResponse(
            {"success": False, "error": f"No game logic for path '{chosen_path}'."},
            status=400
        )

    try:
        game_data = game_func(word)
    except Exception as e:
        return JsonResponse({"success": False, "error": f"Game error: {e}"}, status=500)

    # 7. Return combined response
    return JsonResponse({
        "success": True,
        "classification": classification,
        "game_data": game_data
    })

@csrf_exempt
def validate_word_association_view(request):
    if request.method != "POST":
        return HttpResponseNotAllowed(["POST"])

    try:
        data = json.loads(request.body)
        entries = data.get("entries")
        if not entries:
            return JsonResponse({"error": "Missing 'entries' in request"}, status=400)

        result = validate_word_associations(entries)
        all_valid = all(item["valid"] for item in result["results"])
        result["status"] = "correct" if all_valid else "incorrect"
        return JsonResponse(result)

    except Exception as e:
        return JsonResponse({"error": str(e)}, status=500)
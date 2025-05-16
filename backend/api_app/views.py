from django.shortcuts import render

# Create your views here.
import json
from .services.wordfilter import filter_harmful_word
from .services.get_game_component import classify_word
#from .game_api.puzzle import connect_puzzle
from api_app.game_api.puzzle import connect_puzzle
from django.http import JsonResponse, HttpResponseNotAllowed
from django.views.decorators.csrf import csrf_exempt



@csrf_exempt  # For development; use proper CSRF protection in production.

def process_word(request):
    if request.method == 'POST':
        try:
            data = json.loads(request.body)
        except json.JSONDecodeError:
            return JsonResponse({'error': 'Invalid JSON'}, status=400)
        
        """
        checkpoint 1
        word get
        word count
        word filter
        """
        word = data.get('word', '')
        # validate word input
        if not word or len(word.split()) > 3:
            return JsonResponse({"success": False,'error': 'Please provide 1-3 words.'}, status=400)

        # Filter harmful words
        category = filter_harmful_word(word)
        if category != "not harmful":
            # log_to_csv(word, category)
            return JsonResponse({"success": False,'error': 'The word is harmful.'}, status=400)
        
        print("checkpoint 1 clear")

        """
        checkpoint 2
        get game component 
        """
        word_class=classify_word(word)
        response_data = word_class

        print("checkpoint 2 clear")

        return JsonResponse(response_data)
    
    else:
        return JsonResponse({'error': 'Invalid HTTP method, only POST allowed'}, status=405)


@csrf_exempt 
def connectpuzzle(request):
    if request.method != "POST":
        return HttpResponseNotAllowed(["POST"])
    
    try:
        body = json.loads(request.body)
    except Exception as e:
        return JsonResponse({"error": f"Invalid JSON: {e}"}, status=400)
    
    word = body.get("word")
    if not word:
        return JsonResponse({"error": "No word provided"}, status=400)
    
    try:
        result = connect_puzzle(word)
        return JsonResponse(result)
    except Exception as e:
        return JsonResponse({"error": str(e)}, status=500)

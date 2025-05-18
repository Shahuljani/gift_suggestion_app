import google.generativeai as genai
from django.shortcuts import render
from django.http import JsonResponse
from django.views.decorators.csrf import ensure_csrf_cookie
from django.views.decorators.http import require_POST
import json
import os
import logging

# Configure logging
logging.basicConfig(level=logging.DEBUG)
logger = logging.getLogger(__name__)

# Configure Gemini API
genai.configure(api_key=os.getenv('GEMINI_API_KEY', 'AIzaSyDXCYS1f-9128udpilhmJXkG-I0ypzm3cA'))  # Replace with your key

@ensure_csrf_cookie
def index(request):
    return render(request, 'index.html')

@require_POST
def generate_suggestions(request):
    try:
        data = json.loads(request.body)
        prompt = data.get('prompt', '')
        if not prompt:
            return JsonResponse({'error': 'Prompt is required'}, status=400)

        model = genai.GenerativeModel('gemini-1.5-flash')
        response = model.generate_content(
            f"Provide a list of creative and thoughtful gift suggestions based on the following prompt: '{prompt}'. Return the suggestions as a bulleted list."
        )
        
        # Log the raw response for debugging
        logger.debug(f"Raw API response: {response.text}")

        # Parse the response
        suggestions = []
        if response.text:
            lines = response.text.split('\n')
            for line in lines:
                # Handle lines starting with various bullet characters or plain text
                cleaned_line = line.strip().lstrip('-*• ').strip()
                if cleaned_line:  # Only include non-empty lines
                    suggestions.append(cleaned_line)
        else:
            logger.warning("Empty response from Gemini API")
            return JsonResponse({'error': 'No suggestions received from API'}, status=500)

        # Ensure suggestions are not empty
        if not suggestions:
            logger.warning("No valid suggestions parsed from response")
            return JsonResponse({'error': 'No valid suggestions found'}, status=500)

        logger.debug(f"Parsed suggestions: {suggestions}")
        return JsonResponse({'suggestions': suggestions})
    except Exception as e:
        logger.error(f"Error generating suggestions: {str(e)}")
        return JsonResponse({'error': str(e)}, status=500)
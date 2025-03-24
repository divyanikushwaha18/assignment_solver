from django.http import JsonResponse
from rest_framework.decorators import api_view, parser_classes
from rest_framework.parsers import MultiPartParser
from .services.request_handler import RequestHandler
import logging

logger = logging.getLogger(__name__)

@api_view(['POST'])
@parser_classes([MultiPartParser])
def api_endpoint(request):
    """
    Main API endpoint to handle assignment questions.
    """
    try:
        question = request.POST.get('question')
        file = request.FILES.get('file')
        
        if not question:
            return JsonResponse({"error": "No question provided"}, status=400)
        
        logger.info(f"Received question: {question}")
        if file:
            logger.info(f"Received file: {file.name}, size: {file.size} bytes")
        
        handler = RequestHandler()
        result = handler.process_request(question, file)
        
        return JsonResponse(result)
    
    except Exception as e:
        logger.error(f"Error processing request: {str(e)}")
        return JsonResponse({"error": f"An error occurred: {str(e)}"}, status=500)
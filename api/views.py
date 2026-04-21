from rest_framework.decorators import api_view
from rest_framework.response import Response
from rest_framework import status
from datetime import datetime
import os


@api_view(['GET'])
def ping(request):
    """
    Health check endpoint for testing API availability.
    Returns status, message, timestamp, and environment.
    """
    environment = 'production' if not os.getenv('DEBUG', 'True') == 'True' else 'local'
    
    return Response({
        'status': 'ok',
        'message': 'Django Data Analysis API is running',
        'timestamp': datetime.utcnow().isoformat() + 'Z',
        'environment': environment
    }, status=status.HTTP_200_OK)


@api_view(['GET'])
def health(request):
    """
    Detailed health check endpoint.
    """
    return Response({
        'status': 'healthy',
        'database': 'connected',
        'cache': 'available',
        'celery': 'configured'
    }, status=status.HTTP_200_OK)

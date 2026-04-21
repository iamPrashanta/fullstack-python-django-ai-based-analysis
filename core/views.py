
from rest_framework.decorators import api_view, permission_classes
from rest_framework.permissions import AllowAny, IsAuthenticated, IsAdminUser
from rest_framework.response import Response
from django.db import connection
from django.conf import settings
import time

@api_view(['GET'])
@permission_classes([AllowAny])
def health_check(request):
    """
    Simple health check endpoint for load balancers.
    """
    return Response({"status": "ok", "service": "django-backend"})

@api_view(['GET'])
@permission_classes([IsAdminUser])
def test_db_connection(request):
    """
    Test database connection.
    Restricted to admins.
    """
    start_time = time.time()
    try:
        with connection.cursor() as cursor:
            cursor.execute("SELECT 1")
            one = cursor.fetchone()[0]
        duration = time.time() - start_time
        return Response({
            "status": "connected",
            "result": one,
            "duration_seconds": duration,
            "database": settings.DATABASES['default']['NAME']
        })
    except Exception as e:
        return Response({"status": "error", "error": str(e)}, status=500)

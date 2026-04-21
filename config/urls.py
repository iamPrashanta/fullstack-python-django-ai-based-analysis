
from django.urls import path, include
from core.views import health_check, test_db_connection

urlpatterns = [
    path('api/health/',      health_check,       name='health-check'),
    path('api/test-db/',     test_db_connection,  name='test-db'),
    path('api/exhibitors/',  include('apps.exhibitors.urls')),
    path('api/analytics/',   include('apps.analytics.urls')),
    path('api/ml/',          include('apps.ml_models.urls')),
]

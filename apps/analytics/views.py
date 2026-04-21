
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework.permissions import IsAuthenticated
from .services import AnalyticsService

class DashboardStatsView(APIView):
    # permission_classes = [IsAuthenticated]

    def get(self, request):
        stats = AnalyticsService.get_dashboard_stats(request.user)
        return Response(stats)

class TransactionVolumeView(APIView):
    def get(self, request):
        volume_data = AnalyticsService.get_transaction_volume()
        return Response(volume_data)

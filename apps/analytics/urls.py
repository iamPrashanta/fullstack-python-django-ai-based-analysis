
from django.urls import path
from .views import DashboardStatsView, TransactionVolumeView

urlpatterns = [
    path('dashboard/', DashboardStatsView.as_view(), name='dashboard-stats'),
    path('volume/', TransactionVolumeView.as_view(), name='transaction-volume'),
]

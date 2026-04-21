from django.urls import path
from .views import company_list, company_detail

urlpatterns = [
    path('companies/',      company_list,   name='company-list'),
    path('companies/<int:pk>/', company_detail, name='company-detail'),
]
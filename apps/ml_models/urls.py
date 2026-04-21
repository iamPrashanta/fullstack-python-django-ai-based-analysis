
# Placeholder for ML URLs if needed, e.g. triggering training
from django.urls import path
from rest_framework.decorators import api_view
from rest_framework.response import Response
from .tasks import train_model_task

@api_view(['POST'])
def trigger_training(request):
    model_name = request.data.get('model_name')
    train_model_task.delay(model_name, "s3://data/train.csv", {})
    return Response({"status": "Training started"})

urlpatterns = [
    path('train/', trigger_training, name='trigger-training'),
]

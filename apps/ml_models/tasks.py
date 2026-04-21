
from celery import shared_task
from .models import MLModelRegistry
import time

@shared_task(queue='training_queue')
def train_model_task(model_name, dataset_path, params):
    """
    Offline training task.
    """
    print(f"Starting training for {model_name} with params {params}")
    
    # Simulate training
    time.sleep(10)
    
    # Simulate saving artifact
    new_version = f"v{int(time.time())}"
    s3_path = f"models/{model_name}/{new_version}.pkl"
    
    # Register new model version
    MLModelRegistry.objects.create(
        name=model_name,
        version=new_version,
        s3_path=s3_path,
        metrics={"accuracy": 0.95},
        parameters=params,
        is_active=False # Manual promotion required
    )
    
    return f"Training completed for {model_name} {new_version}"

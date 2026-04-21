from celery import shared_task
import time


@shared_task
def example_task(duration=5):
    """
    Example Celery task for testing queue functionality.
    Simulates a long-running data analysis task.
    """
    time.sleep(duration)
    return f"Task completed after {duration} seconds"


@shared_task
def analyze_data(data):
    """
    Placeholder for data analysis tasks using scikit-learn.
    This can be expanded to perform actual ML operations.
    """
    # Example: You can add scikit-learn operations here
    # from sklearn.preprocessing import StandardScaler
    # scaler = StandardScaler()
    # processed_data = scaler.fit_transform(data)
    
    return {
        'status': 'completed',
        'message': 'Data analysis task completed',
        'data_size': len(data) if hasattr(data, '__len__') else 0
    }

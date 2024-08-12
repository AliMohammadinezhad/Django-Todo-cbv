from celery import shared_task

from .models import Todo


@shared_task
def delete_completed_tasks():
    completed_todos = Todo.objects.filter(status=True)
    for task in completed_todos:
        task.delete()

from tracker.models import Task

def set_suggested():
    tasks = Task.objects.filter(are_suggestions_enabled=True).prefetch_related('practice_set')
    for task in tasks.iterator():
        task.set_is_suggested()
        task.send_email_suggestion()

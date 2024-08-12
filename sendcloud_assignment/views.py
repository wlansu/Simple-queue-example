from sendcloud.celery import app as celery_app


def get_scheduled_task_by_id(timer_uuid: str) -> dict:
    """Use the internal celery inspect API to get the scheduled task with the specified id.

    Note: This is quite slow and if we need to scale we should probably use a DB to store the task info.
    Note: This only returns scheduled tasks, not tasks that are currently running or have already run.
    """
    i = celery_app.control.inspect()  # type: ignore
    celery_id = next(iter(i.scheduled()))
    scheduled_tasks = i.scheduled()[celery_id]
    for task in scheduled_tasks:
        if task["request"]["id"] == timer_uuid:
            return task
    return {}

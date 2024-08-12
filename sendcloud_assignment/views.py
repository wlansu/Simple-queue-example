import datetime

from ninja import Schema
from pydantic import UUID4

from sendcloud.celery import app as celery_app


class TaskResult(Schema):
    id: UUID4
    eta: datetime.datetime


known_celery_tasks: dict[UUID4, TaskResult] = {}


def get_scheduled_task_by_id(timer_uuid: UUID4) -> TaskResult | None:
    """Use the internal celery inspect API to get the scheduled task with the specified id.

    Implements a fairly naive cache to avoid hitting the celery API too often.

    Note: This is quite slow and if we need to scale we should probably use a DB to store the task info.
    Note: This only returns scheduled tasks, not tasks that are currently running or have already run.
    """
    global known_celery_tasks
    if timer_uuid in known_celery_tasks:
        return known_celery_tasks[timer_uuid]

    known_celery_tasks = {}

    i = celery_app.control.inspect()  # type: ignore
    assert i is not None
    celery_id = next(iter(i.scheduled()))
    scheduled_tasks = i.scheduled()[celery_id]
    found = None
    for task in scheduled_tasks:
        task_result = TaskResult(id=UUID4(task["request"]["id"]), eta=task["eta"])
        known_celery_tasks[task_result.id] = task_result
        if task_result.id == timer_uuid:
            found = task_result
    return found


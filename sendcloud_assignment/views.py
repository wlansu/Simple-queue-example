import datetime
from itertools import chain

from ninja import Schema
from pydantic import UUID4

from sendcloud.celery import app as celery_app


class TaskResult(Schema):
    eta: datetime.datetime


class CeleryManager:
    def __init__(self) -> None:
        self.tasks_cache: dict[UUID4, TaskResult] = {}
        self.missing_tasks: set[UUID4] = set()

    def get_scheduled_task_by_id(self, timer_uuid: UUID4) -> TaskResult | None:
        """Use the internal celery inspect API to get the scheduled task with the specified id.

        Note: This is quite slow and if we need to scale we should probably use a DB to store the task info.
        Note: This only returns scheduled tasks, not tasks that are currently running or have already run.
        """
        if timer_uuid in self.missing_tasks:
            return None

        if timer_uuid not in self.tasks_cache:
            # Fill the cache
            all_hosts_all_tasks: dict[str, list[dict]] = celery_app.control.inspect().scheduled()
            all_hosts_tasks = chain.from_iterable(all_hosts_all_tasks.values())

            self.tasks_cache = {
                UUID4(task["request"]["id"]): TaskResult(eta=task["eta"])
                for task in all_hosts_tasks
            }

        if timer_uuid in self.tasks_cache:
            return self.tasks_cache[timer_uuid]

        self.missing_tasks.add(timer_uuid)
        return None


celery_manager = CeleryManager()

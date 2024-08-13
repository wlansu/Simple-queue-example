from django.http import Http404
from ninja import NinjaAPI, Schema

import logging
import datetime

from pydantic import AnyHttpUrl, Field, UUID4

from sendcloud_assignment.views import celery_manager
from sendcloud_assignment.tasks import set_timer_task

logger = logging.getLogger(__name__)

api = NinjaAPI(version="0.1.0")


class SetTimerSchema(Schema):
    hours: int = Field(..., ge=0)
    minutes: int = Field(..., ge=0)
    seconds: int = Field(..., ge=0)
    url: AnyHttpUrl


class GetTimerResponse(Schema):
    time_left: float


class SetTimerResponse(GetTimerResponse):
    timer_uuid: UUID4


@api.post("/timer", response=SetTimerResponse)
def set_timer(request, data: SetTimerSchema) -> SetTimerResponse:
    """Create a Celery task that will call a url after the specified time."""
    seconds = datetime.timedelta(
        hours=data.hours, minutes=data.minutes, seconds=data.seconds
    ).total_seconds()
    logger.debug(f"Attempting to send task to Celery. {seconds=}, {data.url=}")
    result = set_timer_task.apply_async((str(data.url),), countdown=seconds)  # type: ignore
    logger.info(f"Sent task to Celery. {seconds=}, {data.url=}, {result.id=}")
    return SetTimerResponse(timer_uuid=UUID4(result.id), time_left=seconds)


@api.get("/timer/{timer_uuid}/", response=GetTimerResponse)
def get_timer(request, timer_uuid: str) -> GetTimerResponse:
    """Get the time left for the timer with the specified id."""
    result = celery_manager.get_scheduled_task_by_id(UUID4(timer_uuid))
    if not result:
        raise Http404

    now = datetime.datetime.now(datetime.timezone.utc)
    # There is no need to convert the result.eta to utc as the datetime module accounts for the timezone differences.
    time_left = (result.eta - now).total_seconds()  # type: ignore

    # It's possible that the task has already been executed, in which case the time left will be negative.
    if time_left < 0:
        time_left = 0
    return GetTimerResponse(time_left=time_left)

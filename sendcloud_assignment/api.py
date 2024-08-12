from ninja import NinjaAPI, Schema

import datetime

from pydantic import AnyHttpUrl, Field

from sendcloud_assignment.views import get_scheduled_task_by_id

api = NinjaAPI(version="0.1.0")


class SetTimerSchema(Schema):
    hours: int = Field(..., ge=0)
    minutes: int = Field(..., ge=0)
    seconds: int = Field(..., ge=0)
    url: AnyHttpUrl


class GetTimerResponse(Schema):
    time_left: float


class SetTimerResponse(GetTimerResponse):
    timer_uuid: str


@api.post("/timer", response=SetTimerResponse)
def set_timer(request, data: SetTimerSchema):
    """Create a Celery task that will call a url after the specified time."""
    from sendcloud_assignment.tasks import set_timer_task

    # Convert hours, minutes and seconds to seconds and combine them
    hours = data.hours * 3600
    minutes = data.minutes * 60
    seconds = hours + minutes + data.seconds
    url = str(data.url)
    result = set_timer_task.apply_async((url,), countdown=seconds)  # type: ignore
    return {"timer_uuid": result.id, "time_left": seconds}


@api.get("/timer/{timer_uuid}/", response=GetTimerResponse)
def get_timer(request, timer_uuid: str):
    """Get the time left for the timer with the specified id."""
    result = get_scheduled_task_by_id(timer_uuid)
    time_left = 0
    if result:
        now = datetime.datetime.now(datetime.timezone.utc)
        eta = datetime.datetime.fromisoformat(result["eta"]).astimezone(
            datetime.timezone.utc
        )
        time_left = (eta - now).total_seconds()  # type: ignore
    return {"time_left": time_left}

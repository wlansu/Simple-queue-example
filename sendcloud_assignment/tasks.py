import httpx
from celery.app import shared_task


@shared_task()
def set_timer_task(url: str) -> None:
    """Call the url."""
    httpx.get(url)

import httpx
from celery.app import shared_task
from pydantic import AnyHttpUrl

import logging

from sendcloud_assignment import constants

logger = logging.getLogger(__name__)


@shared_task(
    autoretry_for=constants.RETRY_EXCEPTIONS,
    retry_kwargs={
        "max_retries": constants.RETRY_COUNT,
        "countdown": constants.RETRY_DELAY,
    },
)
def set_timer_task(url: str) -> None:
    """Call the url.

    Retry in case it raises a predetermined Exception. On any other exception we don't retry.
    """
    response = httpx.get(url, timeout=1)
    # Log the result regardless of success
    logger.info(f"Succesfully completed task: {response=}")
    response.raise_for_status()
